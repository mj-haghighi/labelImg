import pydicom
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from .ImagePreviewModel import ImageDataItem
from .Mixins import PngJpegTypeCheckingMixin, DICOMTypeCheckingMixin, AbstractFileTypecheckingMixin
from ..SingletonMeta import SingletonMeta


class AbstractPixmapProvider(metaclass=SingletonMeta):

    def pixmap(self, filePath):
        raise Exception("!!! this methoud is not implemented !!!")


class PngJpegPixmapProvider(AbstractPixmapProvider, PngJpegTypeCheckingMixin):

    def __init__(self):
        AbstractPixmapProvider.__init__(self)
        PngJpegTypeCheckingMixin.__init__(self)

    def pixmap(self, filePath):
        pmap = QPixmap(filePath)
        return pmap


class DICOMPixmapProvider(AbstractPixmapProvider, DICOMTypeCheckingMixin):

    def __init__(self):
        AbstractPixmapProvider.__init__(self)
        DICOMTypeCheckingMixin.__init__(self)

    def pixmap(self, filePath):
        dicom = pydicom.read_file(filePath)
        np_pixel_array = dicom.pixel_array
        img = np.zeros((*np_pixel_array.shape, 3), dtype=np.uint8)
        np_pixel_array = (np_pixel_array / np_pixel_array.max()) * 255
        img[:, :, 0] = np_pixel_array.astype(int)
        img[:, :, 1] = np_pixel_array.astype(int)
        img[:, :, 2] = np_pixel_array.astype(int)

        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qImg = QImage(img.data, width, height,
                      bytesPerLine, QImage.Format_RGB888)
        return QPixmap.fromImage(qImg)
