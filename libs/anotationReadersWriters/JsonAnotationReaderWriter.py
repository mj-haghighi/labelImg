import json
from typing import Dict
from pathlib import Path
from ..SingletonMeta import SingletonMeta
from ..constants import DEFAULT_ENCODING


ENCODE_METHOD = DEFAULT_ENCODING


class AbstractAnotationWriter(metaclass=SingletonMeta):

    @property
    def suffix(self):
        raise Exception("!!! this method is not implemented !!!")

    def write(self, dataDict, outputPathWithoutExtention):
        """ write anotation in specified format
        """
        raise Exception("!!! this method is not implemented !!!")


class AbstractAnotationReader(metaclass=SingletonMeta):

    def read(self, anotationFilePath) -> Dict:
        """ Read anotation file in specified format
        """
        raise Exception("!!! this method is not implemented !!!")


class JsonAnotationWriter(AbstractAnotationWriter):
    """ write anotation in json format
    """

    @property
    def suffix(self):
        return 'json'

    def write(
        self,
        dataDict,
        outputPathWithoutExtention,
    ):
        Path(outputPathWithoutExtention +
             '.' + self.suffix).write_text(json.dumps(dataDict), ENCODE_METHOD)


class JsonAnotationReader(AbstractAnotationReader):
    """ Read anotation filr in json format
    """

    def read(
        self,
        anotationFilePath
    ) -> Dict:

        with open(anotationFilePath, "r") as file:
            rawData = file.read()

        dataDict = json.loads(rawData)

        return dataDict
