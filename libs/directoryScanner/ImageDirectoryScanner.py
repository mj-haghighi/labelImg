import os
from typing import List
from .DICOMDirectoryScanner import DICOMDirectoryScanner
from .PngJpegDirectoryScanner import PngJpegDirectoryScanner
from .AbstractImageDirectoryScanner import AbstractImageDirectoryScanner
from ..SingletonMeta import SingletonMeta


class ImageDirectoryScanner(AbstractImageDirectoryScanner):
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

        for fname in os.listdir(folderPath):
            fPath = os.path.join(folderPath, fname)
            fpath = os.path.abspath(fPath)
            for scanner in self.scanners:
                if scanner.isMyType(name=fname, path=fPath):
                    result.append(fPath)
            result = sorted(result)
        return result
