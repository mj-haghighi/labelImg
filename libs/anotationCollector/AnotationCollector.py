import os
import json
from typing import List, Dict
from ..ustr import ustr
from ..SingletonMeta import SingletonMeta
from ..mixins import AbstractFileTypecheckingMixin, JsonTypeCheckingMixin


class AbstractAnotationCollector(AbstractFileTypecheckingMixin, metaclass=SingletonMeta):
    """ Collect annotations in base dirs recursively
    """

    def collect(self, folderPath: str) -> List[str]:
        """ Collect annotations in base dirs recursively
        """
        anotationsPath = []
        for root, dirs, files in os.walk(folderPath, topdown=True):
            for file in files:
                if self.isMyType(file.lower()):
                    relativePath = os.path.join(root, file)
                    path = ustr(os.path.abspath(relativePath))
                    anotationsPath.append(path)
        return anotationsPath


class JsonAnotationCollector(AbstractAnotationCollector, JsonTypeCheckingMixin):
    """ Collect annotations of json format in base dirs recursively
    """
    pass
