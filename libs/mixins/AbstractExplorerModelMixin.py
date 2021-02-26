from typing import List, Callable

class AbstractExplorerModelMixin:

    @property
    def dataItemsList(self) -> List:
        """ return list of data items
        """
        raise Exception("!!! this methud not implemented !!!")

    @dataItemsList.setter
    def dataItemsList(self, data: List):
        """ return list of data items
        """
        raise Exception("!!! this methud not implemented !!!")

    def scanDirectory(self, path='', onScanDirectoryEnd: Callable = lambda *argv: None):
        """ scan directory for files and folders
        """
        raise Exception("!!! this methud not implemented !!!")