import os
from ..mixins import AbstractFileTypecheckingMixin

class AbstractImageDirectoryScanner(AbstractFileTypecheckingMixin):
    """ Abstract Directory Scanner
    """

    def scan(self, folderPath: str):
        """ Scan 'folderpath' and looking for valid DICOM images
        """
        if os.path.isfile(folderPath):
            return []

        result = []
        for fname in os.listdir(path):
            fPath = os.path.join(path, fname)
            if self.isMyType(name=fname, path=fPath):
                result.append(fPath)

        return result
