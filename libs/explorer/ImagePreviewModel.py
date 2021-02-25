import os, re
from typing import List, Callable
from PyQt5.QtGui import QImageReader
from ..utils import natural_sort
from ..mixins import AbstractExplorerModelMixin
from ..fileDataCollector import PngJpegDataCollector, DICOMDataCollector
from ..imageProviders import PngJpegQImageProvider, DICOMQImageProvider

class ImageDataItem:
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.qImage = None
        self.extra = {}

        self._dataCollectors = [PngJpegDataCollector(), DICOMDataCollector()]
        self._collectExtraData()

        self._qImageProviders = [PngJpegQImageProvider(), DICOMQImageProvider()]
        self._provideQImage()

    def _collectExtraData(self):
        for dc in self._dataCollectors:
            if dc.isMyType(self.name):
                self.extra = dc.collect(self.path, self.name)
                break

    def _provideQImage(self):
        for qp in self._qImageProviders:
            if qp.isMyType(self.name):
                self.qImage = qp.QImage(self.path)
                break;

class ImagePreviewModel(AbstractExplorerModelMixin):
    def __init__(self):
        self._imageDataItems = []
        self._dataPaths = None

    @property
    def dataItemsList(self) -> List[ImageDataItem]:
        """ return list of data items
        """
        return self._imageDataItems

    @dataItemsList.setter
    def dataItemsList(self, data: List[ImageDataItem]):
        """ set list of data items
        """
        self._imageDataItems = data
        self._dataPaths = None

    @property
    def dataPaths(self):
        if self._dataPaths is None:
            self._dataPaths = [img.path for img in self._imageDataItems]
            return self._dataPaths
        else:
            return self._dataPaths

    def scanDirectory(self, path='', onScanDirectoryEnd: Callable = lambda *argv: None):
        """ scan directory for files and folders
        """
        if os.path.isfile(path):
            return

        extensions = ['.%s' % fmt.data().decode("ascii").lower()
                      for fmt in QImageReader.supportedImageFormats()] + ['.dcm']
        prefixes = ['I']

        imagesPaths = []

        for f in os.listdir(path):
            filePath = os.path.join(path, f)
            if os.path.isfile(filePath) and (filePath.lower().endswith(tuple(extensions)) or f.startswith(tuple(prefixes))):
                imagesPaths.append(filePath)
        natural_sort(imagesPaths, key=lambda x: x.lower())

        dataItems = []
        for path in imagesPaths:
            name = re.split(r'\\|/', path)[-1]

            dataItems.append(
                ImageDataItem(
                    path=path,
                    name=name
                )
            )
        self.dataItemsList = dataItems
        onScanDirectoryEnd(self.dataItemsList)
