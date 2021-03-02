import pydicom
from ..SingletonMeta import SingletonMeta
from ..mixins import PngJpegTypeCheckingMixin, DICOMTypeCheckingMixin

class AbstractFileDataCollector(metaclass=SingletonMeta):
    def collect(self, path, name):
        raise Exception("!!! this methoud is not implemented !!!")


class PngJpegDataCollector(AbstractFileDataCollector, PngJpegTypeCheckingMixin):
    def __init__(self):
        PngJpegTypeCheckingMixin.__init__(self)

    def collect(self, path, name):
        extra = {}
        extra['ext'] = name.split('.')[-1]
        extra['id'] = 0
        return extra


class DICOMDataCollector(AbstractFileDataCollector, DICOMTypeCheckingMixin):
    def __init__(self):
        DICOMTypeCheckingMixin.__init__(self)

    def collect(self, path, name):
        extra = {}
        extra['ext'] = 'dcm'
        dc = pydicom.dcmread(path)
        extra['id'] = dc.SeriesNumber
        return extra
