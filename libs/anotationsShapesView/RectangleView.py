import sys
from libs.utils import distance
from .AbstractAnotationShapesView import AbstractAnotationShapesView
from ..anotationShapesModel import RectangleModel, AbstractAnotationShapeModel


class RectangleView(AbstractAnotationShapesView):
    def __init__(self):
        super().__init__()
        self._model = RectangleModel()
    
    @property
    def model(self) -> AbstractAnotationShapeModel:
        return self._model