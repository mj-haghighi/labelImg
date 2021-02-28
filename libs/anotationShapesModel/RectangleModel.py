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
            'x1': self.points[0].x,
            'y1': self.points[0].y,
            'x2': self.points[1].x,
            'y2': self.points[1].y
        }

    @staticmethod
    def fromDict(dict_):
        """ Convert python dictionary information to RectangleModel object
        """
        points = []
        points.append(QPoint(dict_['x1'], dict_['y1']))
        points.append(QPoint(dict_['x2'], dict_['y2']))
        return RectangleModel(points=points)
