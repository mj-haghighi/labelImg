from typing import List, Callable


class AbstractExplorerViewMixin:

    def _configStyle(self):
        raise Exception("!!! this methud not implemented !!!")

    def _translateIndex(self, index):
        raise Exception("!!! this methud not implemented !!!")

    def loadContent(self, dirPath):
        """ load content of dirPath, files and folders
        """
        raise Exception("!!! this methud not implemented !!!")

    @property
    def viewModel(self):
        """ return model of view
        """
        raise Exception("!!! this methud not implemented !!!")


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


class AbstractFileTypecheckingMixin:

    def isMyType(self, name: str):
        raise Exception("this methoud is not implemented")


class PngJpegTypeCheckingMixin(AbstractFileTypecheckingMixin):

    def __init__(self):
        self.validExt = ['png', 'jpeg', 'jpg']

    def isMyType(self, name: str):
        if name.endswith(tuple(self.validExt)):
            return True
        return False


class DICOMTypeCheckingMixin(AbstractFileTypecheckingMixin):

    def __init__(self):
        self.validExt = ['dcm']
        self.validPrefix = ['I']

    def isMyType(self, name: str):
        if name.endswith(tuple(self.validExt)) or name.startswith(tuple(self.validPrefix)):
            return True
        return False
