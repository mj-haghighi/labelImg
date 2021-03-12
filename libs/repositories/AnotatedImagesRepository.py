from typing import List, Dict
from ..imageDataModel import ImageDataModel
from ..anotationModel import AnotationModel
from ..SingletonMeta import SingletonMeta

class AnotatedImagesRepository(metaclass=SingletonMeta):
    """ Anotations Repository
    """
    
    def __init__(self):
        self._imageDataModelToAnotations = {}

    @property
    def imageDataModelToAnotations(self) -> Dict[ImageDataModel, List[AnotationModel]]:
        return self._imageDataModelToAnotations

    
    def setAnotations(self, image: ImageDataModel, anotations: List[AnotationModel]):
        self.imageDataModelToAnotations[image] = anotations

    def addAnotation(self, image: ImageDataModel, anotation: AnotationModel):
        if image not in self.imageDataModelToAnotations.keys():
            self.imageDataModelToAnotations[image] = []
        self.imageDataModelToAnotations[image].append(anotation)

    def clear(self):
        self._imageDataModelToAnotations = {}