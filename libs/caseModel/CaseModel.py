from typing import List, Dict
from ..imageDataModel import ImageDataModel
from ..anotatedImageModel import AnotatedImageModel
from ..anotationModel import AnotationModel
from ..imageDataModel import ImageDataModel
from ..anotationReadersWriters import AbstractAnotationReader, JsonAnotationReader, JsonAnotationWriter, AbstractAnotationWriter

class CaseModel:
    """ Case entity, that has multiple image
    """

    def __init__(self, name):
        self.name = name
        self._imagePathToAnotatedImage = {}

    @property
    def anotatedImages(self) -> List[AnotatedImageModel]:
        emptyImgsPath = []
        for ai in self.imagePathToAnotatedImage.values():
            if not ai.anotations:
                emptyImgsPath.append(ai.imagePath)
        for p in emptyImgsPath:
            del self._imagePathToAnotatedImage[p]
        return self._imagePathToAnotatedImage.values()

    @property
    def imagePathToAnotatedImage(self) -> Dict[str, AnotatedImageModel]:
        return self._imagePathToAnotatedImage

    def getAnotatedImage(self, imagePath: str) -> AnotatedImageModel:
        if imagePath in self.imagePathToAnotatedImage.keys():
            return self.imagePathToAnotatedImage[imagePath]
        return None

    def addAnotation(self, imagePath: str, imageId: int, anotationModel: AnotationModel):
        if imagePath not in self.imagePathToAnotatedImage.keys():
            self.imagePathToAnotatedImage[imagePath] = AnotatedImageModel(
                anotations=[anotationModel],
                imagePath=imagePath,
                imageId=imageId
            )
        else:
            self.imagePathToAnotatedImage[imagePath].anotations.append(anotationModel)

    @staticmethod
    def read(
        anotationsFilePath: str,
        reader: AbstractAnotationReader = JsonAnotationReader()
    ) -> 'CaseModel':
        """ Read informations from  anotations file using reader
            inputs:
                anotationsFilePath: path of anotation file
                reader: reader module
            return:
                'CaseModel'
        """

        dataDict = reader.read(anotationsFilePath)

        c = CaseModel(
            name=dataDict['name'])

        for data in dataDict['annotated images']:
            anotatedImage = AnotatedImageModel.fromDict(data)
            for anotation in anotatedImage.anotations:
                c.addAnotation(
                    imagePath=anotatedImage.imagePath,
                    imageId=anotatedImage.imageId,
                    anotationModel=anotation)
        return c

    def write(
        self,
        outputPathWithoutExtention,
        writer: AbstractAnotationWriter = JsonAnotationWriter(),
    ):
        """ Write information in anotations file using writer
            inputs:
                outputPathWithoutExtention: path of anotation file,
                writer: writer module
        """
        
        dataDict = {
            'name': self.name,
            'annotated images': [anot.toDict() for anot in self.anotatedImages]
        }
        writer.write(dataDict=dataDict, outputPathWithoutExtention=outputPathWithoutExtention)
