from typing import List
from ..anotationReadersWriters import JsonAnotationReader, JsonAnotationWriter, AbstractAnotationReader, AbstractAnotationWriter
from ..anotationModel import AnotationModel
from ..imageDataItem import ImageDataItem


class AnotationsFileModel:
    """ Manage what information write in anotations file
    """

    def __init__(
        self,
        anotations: List[AnotationModel] = None,
        isVerified=False,
        imageFilePath=None
    ):
        self._anotations = [] if anotations is None else anotations
        self._isVerified = isVerified
        self._imageFilePath = imageFilePath

    def setVerfication(self, isVerified):
        self._isVerified = isVerified

    @property
    def imageFilePath(self):
        return self._imageFilePath

    @property
    def anotations(self) -> List[AnotationModel]:
        return self._anotations

    @property
    def isVerified(self):
        return self._isVerified

    @staticmethod
    def read(
        anotationsFilePath: str,
        reader: AbstractAnotationReader = JsonAnotationReader()
    ) -> 'AnotationsFileModel':
        """ Read informations from  anotations file using reader
            inputs: 
                anotationsFilePath: path of anotation file
            return:
                Tuple[isVerified, imageFilePath, List[Anotation]]
        """

        dataDict = reader.read(anotationsFilePath)

        return AnotationsFileModel(
            anotations=[
                AnotationModel.fromDict(anot) for anot in dataDict['anotations']],
            isVerified=dataDict['isVerified'],
            imageFilePath=dataDict['image']['path'])

    def write(
        self,
        outputPathWithoutExtention,
        imageDataItem: ImageDataItem,
        writer: AbstractAnotationWriter = JsonAnotationWriter(),
    ):
        """ Write information in anotations file using writer
        """
        dataDict = {
            'isVerified': self.isVerified,
            'image': imageDataItem.toDict(),
            'anotations': [anot.toDict() for anot in self.anotations]
        }
        writer.write(dataDict=dataDict, outputPathWithoutExtention=outputPathWithoutExtention)
