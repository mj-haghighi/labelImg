import pydicom, numpy as np
from PyQt5.QtGui import QImage, QPixmap, QImageReader
from ..mixins import PngJpegTypeCheckingMixin, DICOMTypeCheckingMixin
from ..SingletonMeta import SingletonMeta


class AbstractQImageProvider(metaclass=SingletonMeta):

    def QImage(self, filePath):
        raise Exception("!!! this methoud is not implemented !!!")


class PngJpegQImageProvider(AbstractQImageProvider, PngJpegTypeCheckingMixin):

    def __init__(self):
        AbstractQImageProvider.__init__(self)
        PngJpegTypeCheckingMixin.__init__(self)

    def QImage(self, filePath):
        reader = QImageReader(filePath)
        reader.setAutoTransform(True)
        imageData = reader.read()
        if isinstance(imageData, QImage):
            qImg = imageData
        else:
            qImg = QImage.fromData(imageData)
        
        return qImg


class DICOMQImageProvider(AbstractQImageProvider, DICOMTypeCheckingMixin):

    def __init__(self):
        AbstractQImageProvider.__init__(self)
        DICOMTypeCheckingMixin.__init__(self)

    def QImage(self, filePath):
        dicom = pydicom.read_file(filePath)
        pixarr = dicom.pixel_array
        pixarr = (pixarr / pixarr.max()) * 255
        
        # Qt doesn't support grayscale image, so we have to set gray image to 3 channels.
        gimg = np.zeros((*pixarr.shape, 3), dtype=np.uint8)
        gimg[:, :, 0] = pixarr
        gimg[:, :, 1] = pixarr
        gimg[:, :, 2] = pixarr

        height, width, channel = gimg.shape
        bytesPerLine = 3 * width
        qImg = QImage(gimg.data, width, height,
                      bytesPerLine, QImage.Format_RGB888)
        return qImg
