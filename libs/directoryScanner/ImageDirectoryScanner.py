from typing import List
from .AbstractDirectoryScanner import AbstractDirectoryScanner
from .DICOMDirectoryScanner import DICOMDirectoryScanner
from .PngJpegDirectoryScanner import PngJpegDirectoryScanner
from ..SingletonMeta import SingletonMeta


class ImageDirectoryScanner(AbstractDirectoryScanner, metaclass=SingletonMeta):
    """ Directory scanner to looking for valid images
    """

    def __init__(self):
        self.scanners = [
            PngJpegDirectoryScanner(), DICOMDirectoryScanner()]

    def scan(self, folderPath: str) -> List[str]:
        """ Scan 'folderpath' and looking for valid images types
            input:
                folderPath: folder path
            return:
                images path in folder
        """
        if os.path.isfile(folderPath):
            return []

        result = []

        for fname in os.listdir(path):
            fPath = os.path.join(path, fname)
            for scanner in self.scanners:
                if scanner.isMyType(name=fname, path=fPath):
                    result.append(fPath)

        return result
