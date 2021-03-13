import os
from ..imageDataCollector import PngJpegDataCollector, DICOMDataCollector
from ..imageProviders import PngJpegQImageProvider, DICOMQImageProvider
from ..imageViewItem import ImagePreviewItem

class ImageDataModel:
    def __init__(self, root: str, path: str, name: str):
        self.name = name
        self.extra = {}
        self.qImage = None
        self._root = root.replace('\\', '/') # prevent bug in windows style path
        self._path = path.replace('\\', '/') # prevent bug in windows style path
        self._displayText = None
        self._dataCollectors = [PngJpegDataCollector(), DICOMDataCollector()]
        self._collectExtraData()

        self._qImageProviders = [PngJpegQImageProvider(), DICOMQImageProvider()]
        self._provideQImage()
        self._view = None

    @property
    def path(self):
        """ global path
        """
        return self._path

    @property
    def localPath(self):
        """ local path
        """
        if self.root is None:
            raise Exception("!!! root is None !!!")
        return self._path.replace(self.root, '.')

    @property
    def root(self):
        """ root of path
        """
        return self._root

    @property
    def view(self)->ImagePreviewItem:
        return self._view
   
    @view.setter
    def view(self, v: ImagePreviewItem):
        self._view = v

    @property     
    def displayText(self) -> str:
        if self._displayText is None:
            return self.name
        return self._displayText
    
    @displayText.setter
    def displayText(self, dt: str):
        self._displayText = dt

    def toDict(self):
        res = self.extra.copy()
        res['name'] = self.name
        res['path'] = self.localPath
        res['shape'] = [self.qImage.height(), self.qImage.width(),
                        1 if self.qImage.isGrayscale() else 3]
        return res
        
    def _collectExtraData(self):
        for dc in self._dataCollectors:
            if dc.isMyType(self.name, path=self.path):
                self.extra = dc.collect(self.path, self.name)
                break

    def _provideQImage(self):
        for qp in self._qImageProviders:
            if qp.isMyType(self.name, self.path):
                self.qImage = qp.QImage(self.path)
                break;

    def copy(self) -> 'ImageDataModel':
        """ Make copy of it self
        """
        idi = ImageDataModel(
            path=self.path,
            name=self.name,
            root=self.root)

        return idi
