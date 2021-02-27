from ..anotationModel import AnotationModel
from ..anotationsShapesView import RectangleView, AbstractAnotationShapesView


class AnotationView:
    labelFontSize = 8

    def __init__(self, shapeView: AbstractAnotationShapesView = RectangleView(), paintLabel=False):
        self.shapeView = shapeView
        self.model = AnotationModel(shape=shapeView.model)
        self.paintLabel = paintLabel
        
    @property
    def selected(self):
        return self.shapeView.selected

    @selected.setter
    def selected(self, s):
        self.shapeView.selected = s

    def paint(self, painter):
        self.shapeView.paint(painter)
        if self.paintLabel:
            min_x = sys.maxsize
            min_y = sys.maxsize
            min_y_label = int(1.25 * self.labelFontSize)
            for point in self.model.points:
                min_x = min(min_x, point.x())
                min_y = min(min_y, point.y())
            if min_x != sys.maxsize and min_y != sys.maxsize:
                font = QFont()
                font.setPointSize(self.labelFontSize)
                font.setBold(True)
                painter.setFont(font)
                if(self.model.lable == None):
                    self.label = ""
                if(min_y < min_y_label):
                    min_y += min_y_label
                painter.drawText(min_x, min_y, self.model.label)

    def copy(self):
        """ make a copy of anotation view
        """
        anotation = AnotationView()
        anotation.model.lable = self.model.lable
        anotation.shapeView.model.points = [
            p for p in self.shapeView.model.points]
        anotation.shapeView.fill = self.shapeView.fill
        anotation.shapeView.selected = self.shapeView.selected
        anotation.shapeView._closed = self.shapeView._closed
        anotation.paintLabel = self.paintLabel
        return anotation
