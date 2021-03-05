from .AbstractDirectoryScanner import AbstractDirectoryScanner
from ..mixins import PngJpegTypeCheckingMixin
from ..SingletonMeta import SingletonMeta


class PngJpegDirectoryScanner(
    AbstractDirectoryScanner,
    PngJpegTypeCheckingMixin,
    metaclass=SingletonMeta
):
    pass
