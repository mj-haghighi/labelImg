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


