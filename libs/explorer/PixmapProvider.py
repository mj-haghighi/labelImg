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
        pixarr = dicom.pixel_array
        pixarr = (pixarr / pixarr.max()) * 255
        
        # Qt dosent suport gray scaled image, so we have to set gray image to 3 channels.
        gimg = np.zeros((*pixarr.shape, 3), dtype=np.uint8)
        gimg[:, :, 0] = pixarr
        gimg[:, :, 1] = pixarr
        gimg[:, :, 2] = pixarr

        height, width, channel = gimg.shape
        bytesPerLine = 3 * width
        qImg = QImage(gimg.data, width, height,
                      bytesPerLine, QImage.Format_RGB888)
        return QPixmap.fromImage(qImg)
