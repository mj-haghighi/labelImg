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
