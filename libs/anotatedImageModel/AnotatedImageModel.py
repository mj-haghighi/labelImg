from typing import List, Dict
from ..anotationReadersWriters import JsonAnotationReader, JsonAnotationWriter, AbstractAnotationReader, AbstractAnotationWriter
from ..anotationModel import AnotationModel
from ..imageDataModel import ImageDataModel


class AnotatedImageModel:
    """ Manage what information write in anotations file
    """

    def __init__(
        self,
        anotations: List[AnotationModel],
        imagePath: str,
        imageId: int,
        isVerified=False,
    ):
        self._anotations = anotations
        self._imagePath = imagePath
        self._imageId = imageId 
        self._isVerified = isVerified
    
    def setVerfication(self, isVerified):
        self._isVerified = isVerified

    def clearAnotations(self):
        self._anotations = []

    @property
    def imageId(self):
        return self._imageId

    @property
    def imagePath(self):
        return self._imagePath

    @property
    def anotations(self) -> List[AnotationModel]:
        return self._anotations

    @property
    def isVerified(self):
        return self._isVerified

    def toDict(self):
        return {
            'image path': self.imagePath,
            'image id': self.imageId,
            'is verified': self.isVerified,
            'annotations': [anot.toDict() for anot in self.anotations]
        }

    @staticmethod
    def fromDict(data: Dict) -> 'AnotatedImageModel':
        return AnotatedImageModel(
            anotations=[AnotationModel.fromDict(anot) for anot in data['annotations']],
            imagePath = data['image path'],
            imageId=data['image id'],
            isVerified=data['is verified']
        )