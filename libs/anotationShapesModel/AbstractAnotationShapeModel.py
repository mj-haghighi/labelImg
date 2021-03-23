from typing import List
from PyQt5.QtCore import QPointF

class AbstractAnotationShapeModel:
    """ Abstract class for shapes
    """
    def __init__(
        self,
        points: List[QPointF] = []
    ):
        self._points = points
        
    @property
    def points(self)-> List[QPointF]:
        return self._points

    @points.setter
    def points(self, ps: List[QPointF]):
        self._points = ps

    @property
    def maxAllowedPoints(self):
        raise Exception("!!! this method is not implemented !!!")    

    
    def toDict(self):
        """ convert shape information to python dictionary
        """
        raise Exception("!!! this method is not implemented !!!")

    @staticmethod
    def fromDict(self, dict_):
        raise Exception("!!! this method is not implemented !!!")
    
    def copy(self) -> 'AbstractAnotationShapeModel':
        raise Exception("!!! this method is not implemented !!!")

    def reachMaxPoints(self):
        if len(self.points) >= self.maxAllowedPoints:
            return True
        return False

    def addPoint(self, point):
        if not self.reachMaxPoints():
            self.points.append(point)

    def popPoint(self):
        if self.points:
            return self.points.pop()
        return None
