from PyQt5.QtGui import QPen, QPainterPath
from .PointPropertyMixin import PointViewType
from .ColorPropertyMixin import ColorPropertyMixin
from .PointPropertyMixin import PointPropertyMixin
from ..anotationShapesModel import AbstractAnotationShapeModel
from ..anotationsShapesView.ColorPropertyMixin import ColorPropertyMixin
from ..utils import distance
from . import MOVE_VERTEX, NEAR_VERTEX

class AbstractAnotationShapesView(ColorPropertyMixin, PointPropertyMixin):
    scale = 1.0

    def __init__(self, line_color=None):
        self.fill = False
        self.selected = False

        self._highlightIndex = None
        self._highlightMode = NEAR_VERTEX
        self._highlightSettings = {
            NEAR_VERTEX: (4, PointViewType.P_ROUND),
            MOVE_VERTEX: (1.5, PointViewType.P_SQUARE),
        }

        self._closed = False

        if line_color is not None:
            # Override the class line_color attribute
            # with an object attribute. Currently this
            # is used for drawing the pending line a different color.
            self.line_color = line_color

    @property
    def model(self) -> AbstractAnotationShapeModel:
        raise("!!! this method is not implemented !!!")

    def close(self):
        self._closed = True

    def isClosed(self):
        return self._closed

    def setOpen(self):
        self._closed = False

    def paint(self, painter):
        if self.model.points:
            color = self.select_line_color if self.selected else self.line_color
            pen = QPen(color)
            # Try using integer sizes for smoother drawing(?)
            pen.setWidth(max(1, int(round(2.0 / self.scale))))
            painter.setPen(pen)

            line_path = QPainterPath()
            vrtx_path = QPainterPath()

            line_path.moveTo(self.model.points[0])
            # Uncommenting the following line will draw 2 paths
            # for the 1st vertex, and make it non-filled, which
            # may be desirable.
            #self.drawVertex(vrtx_path, 0)

            for i, p in enumerate(self.model.points):
                line_path.lineTo(p)
                self.drawVertex(vrtx_path, i)
            if self.isClosed():
                line_path.lineTo(self.model.points[0])

            painter.drawPath(line_path)
            painter.drawPath(vrtx_path)
            painter.fillPath(vrtx_path, self.vertex_fill_color)

            # Draw text at the top-left

            if self.fill:
                color = self.select_fill_color if self.selected else self.fill_color
                painter.fillPath(line_path, color)

    def drawVertex(self, path, i):
        d = self.point_size / self.scale
        shape = self.point_type
        point = self.model.points[i]
        if i == self._highlightIndex:
            size, shape = self._highlightSettings[self._highlightMode]
            d *= size
        if self._highlightIndex is not None:
            self.vertex_fill_color = self.hvertex_fill_color
        else:
            self.vertex_fill_color = ColorPropertyMixin.vertex_fill_color
        if shape == PointViewType.P_SQUARE:
            path.addRect(point.x() - d / 2, point.y() - d / 2, d, d)
        elif shape == PointViewType.P_ROUND:
            path.addEllipse(point, d / 2.0, d / 2.0)
        else:
            assert False, "unsupported vertex shape"

    def nearestVertex(self, point, epsilon):
        for i, p in enumerate(self.model.points):
            if distance(p - point) <= epsilon:
                return i
        return None

    def containsPoint(self, point):
        return self.makePath().contains(point)

    def makePath(self):
        path = QPainterPath(self.model.points[0])
        for p in self.model.points[1:]:
            path.lineTo(p)
        return path

    def boundingRect(self):
        return self.makePath().boundingRect()

    def moveBy(self, offset):
        self.model.points = [p + offset for p in self.model.points]

    def moveVertexBy(self, i, offset):
        self.model.points[i] += offset

    def highlightVertex(self, i, action):
        self._highlightIndex = i
        self._highlightMode = action

    def highlightClear(self):
        self._highlightIndex = None
