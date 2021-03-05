from .AbstractImageDirectoryScanner import AbstractImageDirectoryScanner
from ..mixins import PngJpegTypeCheckingMixin
from ..SingletonMeta import SingletonMeta


class PngJpegDirectoryScanner(
    AbstractImageDirectoryScanner,
    PngJpegTypeCheckingMixin,
    metaclass=SingletonMeta
):
    pass
