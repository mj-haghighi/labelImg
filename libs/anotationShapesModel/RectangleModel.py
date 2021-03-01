from .AbstractAnotationShapeModel import AbstractAnotationShapeModel

from PyQt5.QtCore import QPoint
from typing import List


class RectangleModel(AbstractAnotationShapeModel):
    def __init__(
        self,
        points: List[QPoint]= None
    ):
        super().__init__(points= [] if points is None else points)

    @property
    def maxAllowedPoints(self):
        return 4

    def toDict(self):
        """ Convert shape information to python dictionary
        """
        return {
            'x0': self.points[0].x(),
            'y0': self.points[0].y(),
            'x1': self.points[1].x(),
            'y1': self.points[1].y(),
            'x2': self.points[2].x(),
            'y2': self.points[2].y(),
            'x3': self.points[3].x(),
            'y3': self.points[3].y()
        }

    @staticmethod
    def fromDict(dict_):
        """ Convert python dictionary information to RectangleModel object
        """
        points = []
        points.append(QPoint(dict_['x0'], dict_['y0']))
        points.append(QPoint(dict_['x1'], dict_['y1']))
        points.append(QPoint(dict_['x2'], dict_['y2']))
        points.append(QPoint(dict_['x3'], dict_['y3']))
        return RectangleModel(points=points)
