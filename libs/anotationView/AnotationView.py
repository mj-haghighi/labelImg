from ..anotationModel import AnotationModel
from ..anotationsShapesView import RectangleView, AbstractAnotationShapesView


class AnotationView:
    labelFontSize = 8

    def __init__(self, shapeViewComponent: AbstractAnotationShapesView = RectangleView, paintLabel=False):
        self._shapeView = shapeViewComponent()
        self._model = AnotationModel(shape=self.shapeView.model)
        self.paintLabel = paintLabel

    @property
    def shapeView(self) -> AbstractAnotationShapesView:
        return self._shapeView

    @shapeView.setter
    def shapeView(self, sv: AbstractAnotationShapesView):
        self._shapeView = sv

    @property
    def selected(self):
        return self.shapeView.selected

    @property
    def model(self)->AnotationModel:
        return self._model

    def setModel(self, m: AnotationModel):
        self._model = m
        self.shapeView.setModel(m.shape)

    @selected.setter
    def selected(self, s):
        self.shapeView.selected = s

    def paint(self, painter):
        self.shapeView.paint(painter)
        if self.paintLabel:
            min_x = sys.maxsize
            min_y = sys.maxsize
            min_y_label = int(1.25 * self.labelFontSize)
            for point in self.shapeView.model.points:
                min_x = min(min_x, point.x())
                min_y = min(min_y, point.y())
            if min_x != sys.maxsize and min_y != sys.maxsize:
                font = QFont()
                font.setPointSize(self.labelFontSize)
                font.setBold(True)
                painter.setFont(font)
                if(self.model.label == None):
                    self.model.label = ""
                if(min_y < min_y_label):
                    min_y += min_y_label
                painter.drawText(min_x, min_y, self.model.label)

    def copy(self):
        """ make a copy of anotation view
        """
        anotation = AnotationView()
        anotation.model.label = self.model.label
        anotation.shapeView.model.points = [
            p for p in self.shapeView.model.points]
        anotation.shapeView.fill = self.shapeView.fill
        anotation.shapeView.selected = self.shapeView.selected
        anotation.shapeView._closed = self.shapeView._closed
        anotation.paintLabel = self.paintLabel
        return anotation
