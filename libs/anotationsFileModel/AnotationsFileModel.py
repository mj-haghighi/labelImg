from typing import List
from ..anotationReadersWriters import JsonAnotationReader, JsonAnotationWriter, AbstractAnotationReader, AbstractAnotationWriter
from ..anotationModel import AnotationModel
from ..imageDataItem import ImageDataItem


class AnotationsFileModel:
    """ Manage what information write in anotations file
    """

    def __init__(
        self,
        anotations: List[AnotationModel] = [],
        isVerified=False,
        imageFilePath=None
    ):
        self._anotations = anotations
        self._isVerified = isVerified
        self._imageFilePath = imageFilePath

    def setVerfication(self, isVerfied):
        self._isVerfied = isVerfied

    @property
    def imageFilePath(self):
        return self._imageFilePath

    @property
    def anotations(self) -> List[AnotationModel]:
        return self._anotations

    @property
    def isVerfied(self):
        return self._isVerfied

    @staticmethod
    def read(
        anotationsFilePath: str,
        reader: AbstractAnotationReader = JsonAnotationReader()
    ) -> 'AnotationsFileModel':
        """ Read informations from  anotations file using reader
            inputs: 
                anotationsFilePath: path of anotation file
            return:
                Tuple[isVerfied, imageFilePath, List[Anotation]]
        """

        dataDict = reader.read(anotationsFilePath)

        return AnotationsFileModel(
            anotations=[
                AnotationModel.fromDict(anot) for anot in dataDict['anotations']],
            isVerified=dataDict['isVerified'],
            imageFilePath=dataDict['image']['path'])

    def write(
        self,
        outFilePath,
        imageDataItem: ImageDataItem,
        writer: AbstractAnotationWriter = JsonAnotationWriter(),
    ):
        """ Write information in anotations file using writer
        """
        dataDict = {
            'isVerified': self.isVerfied,
            'image': imageDataItem.toDict(),
            'anotations': [anot.toDict() for anot in self.anotations]
        }
        writer.write(dataDict=dataDict, outputPath=outFilePath)
