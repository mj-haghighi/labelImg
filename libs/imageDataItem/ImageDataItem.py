from ..fileDataCollector import PngJpegDataCollector, DICOMDataCollector
from ..imageProviders import PngJpegQImageProvider, DICOMQImageProvider
from ..imageViewItem import ImagePreviewItem

class ImageDataItem:
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.qImage = None
        self.extra = {}
        self._displayText = None
        self._dataCollectors = [PngJpegDataCollector(), DICOMDataCollector()]
        self._collectExtraData()

        self._qImageProviders = [PngJpegQImageProvider(), DICOMQImageProvider()]
        self._provideQImage()
        self._view = None

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
        res['path'] = self.path
        res['shape'] = [self.qImage.height(), self.qImage.width(),
                        1 if self.qImage.isGrayscale() else 3]
        return res
        
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

    def copy(self) -> 'ImageDataItem':
        """ Make copy of it self
        """
        idi = ImageDataItem(self.path, self.name)
        return idi