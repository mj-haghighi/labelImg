
try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

#from PyQt4.QtOpenGL import *

# from libs.anotationView import Shape
from libs.utils import distance
from libs.anotationView import AnotationView
from libs.anotationModel import AnotationModel
from libs.anotationsShapesView import MOVE_VERTEX, NEAR_VERTEX

CURSOR_DEFAULT = Qt.ArrowCursor
CURSOR_POINT = Qt.PointingHandCursor
CURSOR_DRAW = Qt.CrossCursor
CURSOR_MOVE = Qt.ClosedHandCursor
CURSOR_GRAB = Qt.OpenHandCursor

# class Canvas(QGLWidget):


class Canvas(QWidget):
    zoomRequest = pyqtSignal(int)
    scrollRequest = pyqtSignal(int, int)
    newShape = pyqtSignal()
    selectionChanged = pyqtSignal(bool)
    shapeMoved = pyqtSignal()
    drawingPolygon = pyqtSignal(bool)

    CREATE, EDIT = list(range(2))

    epsilon = 11.0

    def __init__(self, *args, **kwargs):
        super(Canvas, self).__init__(*args, **kwargs)
        # Initialise local state.
        self.mode = self.EDIT
        self.anotationsViews = []
        self._current = None
        # self.line = Shape(line_color=self.drawingLineColor)

        self.selectedAnotationView = None  # save the selected anotationView here
        self.selectedShapeCopy = None
        self.drawingLineColor = QColor(0, 0, 255)
        self.drawingRectColor = QColor(0, 0, 255)
        self.line = AnotationView()
        self.line.shapeView.line_color = self.drawingLineColor
        self.prevPoint = QPointF()
        self.offsets = QPointF(), QPointF()
        self.scale = 1.0
        self.labelFontSize = 8
        self.pixmap = QPixmap()
        self.visible = {}
        self._hideBackround = False
        self.hideBackround = False
        self.hShape = None
        self.hVertex = None
        self._painter = QPainter()
        self._cursor = CURSOR_DEFAULT
        # Menus:
        self.menus = (QMenu(), QMenu())
        # Set widget options.
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.WheelFocus)
        self.verified = False
        self.drawSquare = False

        #initialisation for panning
        self.pan_initial_pos = QPoint()

    @property
    def current(self) -> AnotationView:
        return self._current

    @current.setter
    def current(self, av: AnotationView):
        self._current = av

    def setDrawingColor(self, qColor):
        self.drawingLineColor = qColor
        self.drawingRectColor = qColor

    def enterEvent(self, ev):
        self.overrideCursor(self._cursor)

    def leaveEvent(self, ev):
        self.restoreCursor()

    def focusOutEvent(self, ev):
        self.restoreCursor()

    def isVisible(self, anotationView):
        return self.visible.get(anotationView, True)

    def drawing(self):
        return self.mode == self.CREATE

    def editing(self):
        return self.mode == self.EDIT

    def setEditing(self, value=True):
        self.mode = self.EDIT if value else self.CREATE
        if not value:  # Create
            self.unHighlight()
            self.deSelectShape()
        self.prevPoint = QPointF()
        self.repaint()

    def unHighlight(self):
        if self.hShape:
            self.hShape.shapeView.highlightClear()
        self.hVertex = self.hShape = None

    def selectedVertex(self):
        return self.hVertex is not None

    def mouseMoveEvent(self, ev):
        """Update line with last point and current coordinates."""
        pos = self.transformPos(ev.pos())

        # Update coordinates in status bar if image is opened
        window = self.parent().window()
        if window.filePath is not None:
            self.parent().window().labelCoordinates.setText(
                'X: %d; Y: %d' % (pos.x(), pos.y()))

        # Polygon drawing.
        if self.drawing():
            self.overrideCursor(CURSOR_DRAW)
            if self.current:
                # Display annotation width and height while drawing
                currentWidth = abs(
                    self.current.shapeView.model.points[0].x() - pos.x())
                currentHeight = abs(
                    self.current.shapeView.model.points[0].y() - pos.y())
                self.parent().window().labelCoordinates.setText(
                    'Width: %d, Height: %d / X: %d; Y: %d' % (currentWidth, currentHeight, pos.x(), pos.y()))

                color = self.drawingLineColor
                if self.outOfPixmap(pos):
                    # Don't allow the user to draw outside the pixmap.
                    # Clip the coordinates to 0 or max,
                    # if they are outside the range [0, max]
                    size = self.pixmap.size()
                    clipped_x = min(max(0, pos.x()), size.width())
                    clipped_y = min(max(0, pos.y()), size.height())
                    pos = QPointF(clipped_x, clipped_y)
                elif len(self.current.shapeView.model.points) > 1 and self.closeEnough(pos, self.current.shapeView.model.points[0]):
                    # Attract line to starting point and colorise to alert the
                    # user:
                    pos = self.current.shapeView.model.points[0]
                    color = self.current.shapeView.line_color
                    self.overrideCursor(CURSOR_POINT)
                    self.current.shapeView.highlightVertex(0, NEAR_VERTEX)

                if self.drawSquare:
                    initPos = self.current.shapeView.model.points[0]
                    minX = initPos.x()
                    minY = initPos.y()
                    min_size = min(abs(pos.x() - minX), abs(pos.y() - minY))
                    directionX = -1 if pos.x() - minX < 0 else 1
                    directionY = -1 if pos.y() - minY < 0 else 1
                    self.line.shapeView.model.points[1] = QPointF(
                        minX + directionX * min_size, minY + directionY * min_size)
                else:
                    self.line.shapeView.model.points[1] = pos

                self.line.shapeView.line_color = color
                self.prevPoint = QPointF()
                self.current.shapeView.highlightClear()
            else:
                self.prevPoint = pos
            self.repaint()
            return

        # Polygon copy moving.
        if Qt.RightButton & ev.buttons():
            if self.selectedShapeCopy and self.prevPoint:
                self.overrideCursor(CURSOR_MOVE)
                self.boundedMoveShape(self.selectedShapeCopy, pos)
                self.repaint()
            elif self.selectedAnotationView:
                self.selectedShapeCopy = self.selectedAnotationView.copy()
                self.repaint()
            return

        # Polygon/Vertex moving.
        if Qt.LeftButton & ev.buttons():
            if self.selectedVertex():
                self.boundedMoveVertex(pos)
                self.shapeMoved.emit()
                self.repaint()
            elif self.selectedAnotationView and self.prevPoint:
                self.overrideCursor(CURSOR_MOVE)
                self.boundedMoveShape(self.selectedAnotationView, pos)
                self.shapeMoved.emit()
                self.repaint()
            else:
                #pan
                delta_x = pos.x() - self.pan_initial_pos.x()
                delta_y = pos.y() - self.pan_initial_pos.y()
                self.scrollRequest.emit(delta_x, Qt.Horizontal)
                self.scrollRequest.emit(delta_y, Qt.Vertical)
                self.update()
            return

        # Just hovering over the canvas, 2 posibilities:
        # - Highlight shapes
        # - Highlight vertex
        # Update anotationView/vertex fill and tooltip value accordingly.
        self.setToolTip("Image")
        for anotationView in reversed([s for s in self.anotationsViews if self.isVisible(s)]):
            # Look for a nearby vertex to highlight. If that fails,
            # check if we happen to be inside a anotationView.
            index = anotationView.shapeView.nearestVertex(pos, self.epsilon)
            if index is not None:
                if self.selectedVertex():
                    self.hShape.shapeView.highlightClear()
                self.hVertex, self.hShape = index, anotationView
                anotationView.shapeView.highlightVertex(index, MOVE_VERTEX)
                self.overrideCursor(CURSOR_POINT)
                self.setToolTip("Click & drag to move point")
                self.setStatusTip(self.toolTip())
                self.update()
                break
            elif anotationView.shapeView.containsPoint(pos):
                if self.selectedVertex():
                    self.hShape.shapeView.highlightClear()
                self.hVertex, self.hShape = None, anotationView
                self.setToolTip(
                    "Click & drag to move anotationView '%s'" % anotationView.model.label)
                self.setStatusTip(self.toolTip())
                self.overrideCursor(CURSOR_GRAB)
                self.update()
                break
        else:  # Nothing found, clear highlights, reset state.
            if self.hShape:
                self.hShape.shapeView.highlightClear()
                self.update()
            self.hVertex, self.hShape = None, None
            self.overrideCursor(CURSOR_DEFAULT)

    def mousePressEvent(self, ev):
        pos = self.transformPos(ev.pos())

        if ev.button() == Qt.LeftButton:
            if self.drawing():
                self.handleDrawing(pos)
            else:
                selection = self.selectShapePoint(pos)
                self.prevPoint = pos

                if selection is None:
                    #pan
                    QApplication.setOverrideCursor(QCursor(Qt.OpenHandCursor))
                    self.pan_initial_pos = pos

        elif ev.button() == Qt.RightButton and self.editing():
            self.selectShapePoint(pos)
            self.prevPoint = pos
        self.update()

    def mouseReleaseEvent(self, ev):
        if ev.button() == Qt.RightButton:
            menu = self.menus[bool(self.selectedShapeCopy)]
            self.restoreCursor()
            if not menu.exec_(self.mapToGlobal(ev.pos()))\
               and self.selectedShapeCopy:
                # Cancel the move by deleting the shadow copy.
                self.selectedShapeCopy = None
                self.repaint()
        elif ev.button() == Qt.LeftButton and self.selectedAnotationView:
            if self.selectedVertex():
                self.overrideCursor(CURSOR_POINT)
            else:
                self.overrideCursor(CURSOR_GRAB)
        elif ev.button() == Qt.LeftButton:
            pos = self.transformPos(ev.pos())
            if self.drawing():
                self.handleDrawing(pos)
            else:
                #pan
                QApplication.restoreOverrideCursor()

    def endMove(self, copy=False):
        assert self.selectedAnotationView and self.selectedShapeCopy
        anotationView = self.selectedShapeCopy
        #del anotationView.fill_color
        #del anotationView.line_color
        if copy:
            self.anotationsViews.append(anotationView)
            self.selectedAnotationView.selected = False
            self.selectedAnotationView = anotationView
            self.repaint()
        else:
            self.selectedAnotationView.points = [
                p for p in anotationView.points]
        self.selectedShapeCopy = None

    def hideBackroundShapes(self, value):
        self.hideBackround = value
        if self.selectedAnotationView:
            # Only hide other shapes if there is a current selection.
            # Otherwise the user will not be able to select a anotationView.
            self.setHiding(True)
            self.repaint()

    def handleDrawing(self, pos):
        if self.current and self.current.shapeView.model.reachMaxPoints() is False:
            initPos = self.current.shapeView.model.points[0]
            minX = initPos.x()
            minY = initPos.y()
            targetPos = self.line.shapeView.model.points[1]
            maxX = targetPos.x()
            maxY = targetPos.y()
            self.current.shapeView.model.addPoint(QPointF(maxX, minY))
            self.current.shapeView.model.addPoint(targetPos)
            self.current.shapeView.model.addPoint(QPointF(minX, maxY))
            self.finalise()
        elif not self.outOfPixmap(pos):
            self.current = AnotationView()
            self.current.shapeView.model.addPoint(pos)
            self.line.shapeView.model.points = [pos, pos]
            self.setHiding()
            self.drawingPolygon.emit(True)
            self.update()

    def setHiding(self, enable=True):
        self._hideBackround = self.hideBackround if enable else False

    def canCloseShape(self):
        return self.drawing() and self.current and len(self.current.shapeView.model.points) > 2

    def mouseDoubleClickEvent(self, ev):
        # We need at least 4 points here, since the mousePress handler
        # adds an extra one before this handler is called.
        if self.canCloseShape() and len(self.current.shapeView.model.points) > 3:
            self.current.shapeView.model.popPoint()
            self.finalise()

    def selectShape(self, anotationView):
        self.deSelectShape()
        anotationView.selected = True
        self.selectedAnotationView = anotationView
        self.setHiding()
        self.selectionChanged.emit(True)
        self.update()

    def selectShapePoint(self, point):
        """Select the first anotationView created which contains this point."""
        self.deSelectShape()
        if self.selectedVertex():  # A vertex is marked for selection.
            index, anotationView = self.hVertex, self.hShape
            anotationView.shapeView.highlightVertex(index, MOVE_VERTEX)
            self.selectShape(anotationView)
            return self.hVertex
        for anotationView in reversed(self.anotationsViews):
            if self.isVisible(anotationView) and anotationView.shapeView.containsPoint(point):
                self.selectShape(anotationView)
                self.calculateOffsets(anotationView, point)
                return self.selectedAnotationView
        return None

    def calculateOffsets(self, anotationView, point):
        rect = anotationView.shapeView.boundingRect()
        x1 = rect.x() - point.x()
        y1 = rect.y() - point.y()
        x2 = (rect.x() + rect.width()) - point.x()
        y2 = (rect.y() + rect.height()) - point.y()
        self.offsets = QPointF(x1, y1), QPointF(x2, y2)

    def snapPointToCanvas(self, x, y):
        """
        Moves a point x,y to within the boundaries of the canvas.
        :return: (x,y,snapped) where snapped is True if x or y were changed, False if not.
        """
        if x < 0 or x > self.pixmap.width() or y < 0 or y > self.pixmap.height():
            x = max(x, 0)
            y = max(y, 0)
            x = min(x, self.pixmap.width())
            y = min(y, self.pixmap.height())
            return x, y, True

        return x, y, False

    def boundedMoveVertex(self, pos):
        index, anotationView = self.hVertex, self.hShape
        point = anotationView.shapeView.model.points[index]
        if self.outOfPixmap(pos):
            size = self.pixmap.size()
            clipped_x = min(max(0, pos.x()), size.width())
            clipped_y = min(max(0, pos.y()), size.height())
            pos = QPointF(clipped_x, clipped_y)

        if self.drawSquare:
            opposite_point_index = (index + 2) % 4
            opposite_point = anotationView.shapeView.model.points[opposite_point_index]

            min_size = min(abs(pos.x() - opposite_point.x()),
                           abs(pos.y() - opposite_point.y()))
            directionX = -1 if pos.x() - opposite_point.x() < 0 else 1
            directionY = -1 if pos.y() - opposite_point.y() < 0 else 1
            shiftPos = QPointF(opposite_point.x() + directionX * min_size - point.x(),
                               opposite_point.y() + directionY * min_size - point.y())
        else:
            shiftPos = pos - point

        anotationView.shapeView.moveVertexBy(index, shiftPos)

        lindex = (index + 1) % 4
        rindex = (index + 3) % 4
        lshift = None
        rshift = None
        if index % 2 == 0:
            rshift = QPointF(shiftPos.x(), 0)
            lshift = QPointF(0, shiftPos.y())
        else:
            lshift = QPointF(shiftPos.x(), 0)
            rshift = QPointF(0, shiftPos.y())
        anotationView.shapeView.moveVertexBy(rindex, rshift)
        anotationView.shapeView.moveVertexBy(lindex, lshift)

    def boundedMoveShape(self, anotationView: AnotationView, pos):
        if self.outOfPixmap(pos):
            return False  # No need to move
        o1 = pos + self.offsets[0]
        if self.outOfPixmap(o1):
            pos -= QPointF(min(0, o1.x()), min(0, o1.y()))
        o2 = pos + self.offsets[1]
        if self.outOfPixmap(o2):
            pos += QPointF(min(0, self.pixmap.width() - o2.x()),
                           min(0, self.pixmap.height() - o2.y()))
        # The next line tracks the new position of the cursor
        # relative to the anotationView, but also results in making it
        # a bit "shaky" when nearing the border and allows it to
        # go outside of the anotationView's area for some reason. XXX
        #self.calculateOffsets(self.selectedAnotationView, pos)
        dp = pos - self.prevPoint
        if dp:
            anotationView.shapeView.moveBy(dp)
            self.prevPoint = pos
            return True
        return False

    def deSelectShape(self):
        if self.selectedAnotationView:
            self.selectedAnotationView.selected = False
            self.selectedAnotationView = None
            self.setHiding(False)
            self.selectionChanged.emit(False)
            self.update()

    def deleteSelected(self):
        if self.selectedAnotationView:
            anotationView = self.selectedAnotationView
            self.anotationsViews.remove(self.selectedAnotationView)
            self.selectedAnotationView = None
            self.update()
            return anotationView

    def copySelectedShape(self):
        if self.selectedAnotationView:
            anotationView = self.selectedAnotationView.copy()
            self.deSelectShape()
            self.anotationsViews.append(anotationView)
            anotationView.selected = True
            self.selectedAnotationView = anotationView
            self.boundedShiftShape(anotationView)
            return anotationView

    def boundedShiftShape(self, anotationView):
        # Try to move in one direction, and if it fails in another.
        # Give up if both fail.
        point = anotationView.shapeView.model.points[0]
        offset = QPointF(2.0, 2.0)
        self.calculateOffsets(anotationView, point)
        self.prevPoint = point
        if not self.boundedMoveShape(anotationView, point - offset):
            self.boundedMoveShape(anotationView, point + offset)

    def paintEvent(self, event):
        if not self.pixmap:
            return super(Canvas, self).paintEvent(event)

        p = self._painter
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.HighQualityAntialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)

        p.scale(self.scale, self.scale)
        p.translate(self.offsetToCenter())

        p.drawPixmap(0, 0, self.pixmap)

        # Shape.scale = self.scale
        # Shape.labelFontSize = self.labelFontSize

        for anotationView in self.anotationsViews:
            if (anotationView.selected or not self._hideBackround) and self.isVisible(anotationView):
                anotationView.shapeView.fill = anotationView.selected or anotationView == self.hShape
                anotationView.paint(p)
        if self.current:
            self.current.paint(p)
            # self.line.paint(p)
            self.line.paint(p)
        if self.selectedShapeCopy:
            self.selectedShapeCopy.paint(p)

        # Paint rect
        if self.current is not None and len(self.line.shapeView.model.points) == 2:
            leftTop = self.line.shapeView.model.points[0]
            rightBottom = self.line.shapeView.model.points[1]
            rectWidth = rightBottom.x() - leftTop.x()
            rectHeight = rightBottom.y() - leftTop.y()
            p.setPen(self.drawingRectColor)
            brush = QBrush(Qt.BDiagPattern)
            p.setBrush(brush)
            p.drawRect(leftTop.x(), leftTop.y(), rectWidth, rectHeight)

        if self.drawing() and not self.prevPoint.isNull() and not self.outOfPixmap(self.prevPoint):
            p.setPen(QColor(0, 0, 0))
            p.drawLine(self.prevPoint.x(), 0,
                       self.prevPoint.x(), self.pixmap.height())
            p.drawLine(0, self.prevPoint.y(),
                       self.pixmap.width(), self.prevPoint.y())

        self.setAutoFillBackground(True)
        if self.verified:
            pal = self.palette()
            pal.setColor(self.backgroundRole(), QColor(184, 239, 38, 128))
            self.setPalette(pal)
        else:
            pal = self.palette()
            pal.setColor(self.backgroundRole(), QColor(232, 232, 232, 255))
            self.setPalette(pal)

        p.end()

    def transformPos(self, point):
        """Convert from widget-logical coordinates to painter-logical coordinates."""
        return point / self.scale - self.offsetToCenter()

    def offsetToCenter(self):
        s = self.scale
        area = super(Canvas, self).size()
        w, h = self.pixmap.width() * s, self.pixmap.height() * s
        aw, ah = area.width(), area.height()
        x = (aw - w) / (2 * s) if aw > w else 0
        y = (ah - h) / (2 * s) if ah > h else 0
        return QPointF(x, y)

    def outOfPixmap(self, p):
        w, h = self.pixmap.width(), self.pixmap.height()
        return not (0 <= p.x() <= w and 0 <= p.y() <= h)

    def finalise(self):
        assert self.current
        if self.current.shapeView.model.points[0] == self.current.shapeView.model.points[-1]:
            self.current = None
            self.drawingPolygon.emit(False)
            self.update()
            return

        self.current.shapeView.close()
        self.anotationsViews.append(self.current)
        self.current = None
        self.setHiding(False)
        self.newShape.emit()
        self.update()

    def closeEnough(self, p1, p2):
        #d = distance(p1 - p2)
        #m = (p1-p2).manhattanLength()
        # print "d %.2f, m %d, %.2f" % (d, m, d - m)
        return distance(p1 - p2) < self.epsilon

    # These two, along with a call to adjustSize are required for the
    # scroll area.
    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        if self.pixmap:
            return self.scale * self.pixmap.size()
        return super(Canvas, self).minimumSizeHint()

    def wheelEvent(self, ev):
        qt_version = 4 if hasattr(ev, "delta") else 5
        if qt_version == 4:
            if ev.orientation() == Qt.Vertical:
                v_delta = ev.delta()
                h_delta = 0
            else:
                h_delta = ev.delta()
                v_delta = 0
        else:
            delta = ev.angleDelta()
            h_delta = delta.x()
            v_delta = delta.y()

        mods = ev.modifiers()
        if Qt.ControlModifier == int(mods) and v_delta:
            self.zoomRequest.emit(v_delta)
        else:
            v_delta and self.scrollRequest.emit(v_delta, Qt.Vertical)
            h_delta and self.scrollRequest.emit(h_delta, Qt.Horizontal)
        ev.accept()

    def keyPressEvent(self, ev):
        key = ev.key()
        if key == Qt.Key_Escape and self.current:
            print('ESC press')
            self.current = None
            self.drawingPolygon.emit(False)
            self.update()
        elif key == Qt.Key_Return and self.canCloseShape():
            self.finalise()
        elif key == Qt.Key_Left and self.selectedAnotationView:
            self.moveOnePixel('Left')
        elif key == Qt.Key_Right and self.selectedAnotationView:
            self.moveOnePixel('Right')
        elif key == Qt.Key_Up and self.selectedAnotationView:
            self.moveOnePixel('Up')
        elif key == Qt.Key_Down and self.selectedAnotationView:
            self.moveOnePixel('Down')

    def moveOnePixel(self, direction):
        # print(self.selectedAnotationView.points)
        dx = 0
        dy = 0
        if direction == 'Left' and not self.moveOutOfBound(QPointF(-1.0, 0)):
            # print("move Left one pixel")
            dx = -1
            dy = 0
        elif direction == 'Right' and not self.moveOutOfBound(QPointF(1.0, 0)):
            # print("move Right one pixel")
            dx = 1
            dy = 0
        elif direction == 'Up' and not self.moveOutOfBound(QPointF(0, -1.0)):
            # print("move Up one pixel")
            dx = 0
            dy = -1
        elif direction == 'Down' and not self.moveOutOfBound(QPointF(0, 1.0)):
            # print("move Down one pixel")
            dx = 0
            dy = 1

        for point in self.selectedAnotationView.shapeView.model.points:
            point += QPointF(dx, dy)

        self.shapeMoved.emit()
        self.repaint()

    def moveOutOfBound(self, step):
        points = [
            p1+p2 for p1, p2 in zip(self.selectedAnotationView.shapeView.model.points, [step]*4)]
        return True in map(self.outOfPixmap, points)

    def setLastLabel(self, text, line_color=None, fill_color=None):
        assert text
        self.anotationsViews[-1].model.label = text
        if line_color:
            self.anotationsViews[-1].shapeView.line_color = line_color

        if fill_color:
            self.anotationsViews[-1].shapeView.fill_color = fill_color

        return self.anotationsViews[-1]

    def undoLastLine(self):
        assert self.anotationsViews
        self.current = self.anotationsViews.pop()
        self.current.shapeView.setOpen()
        self.line.shapeView.model.points = [
            self.current.shapeView.model.points[-1], self.current.shapeView.model.points[0]]
        self.drawingPolygon.emit(True)

    def resetAllLines(self):
        assert self.anotationsViews
        self.current = self.anotationsViews.pop()
        self.current.shapeView.setOpen()
        self.line.shapeView.model.points = [
            self.current.shapeView.model.points[-1], self.current.shapeView.model.points[0]]
        self.drawingPolygon.emit(True)
        self.current = None
        self.drawingPolygon.emit(False)
        self.update()

    def loadPixmap(self, pixmap):
        self.pixmap = pixmap
        self.anotationsViews = []
        self.repaint()

    def loadShapes(self, shapes):
        self.anotationsViews = list(shapes)
        self.current = None
        self.repaint()

    def setShapeVisible(self, anotationView, value):
        self.visible[anotationView] = value
        self.repaint()

    def currentCursor(self):
        cursor = QApplication.overrideCursor()
        if cursor is not None:
            cursor = cursor.shape()
        return cursor

    def overrideCursor(self, cursor):
        self._cursor = cursor
        if self.currentCursor() is None:
            QApplication.setOverrideCursor(cursor)
        else:
            QApplication.changeOverrideCursor(cursor)

    def restoreCursor(self):
        QApplication.restoreOverrideCursor()

    def resetState(self):
        self.restoreCursor()
        self.pixmap = None
        self.update()

    def setDrawingShapeToSquare(self, status):
        self.drawSquare = status
