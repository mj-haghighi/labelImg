from .AbstractImageDirectoryScanner import AbstractImageDirectoryScanner
from ..mixins import DICOMTypeCheckingMixin
from ..SingletonMeta import SingletonMeta


class DICOMDirectoryScanner(
    AbstractImageDirectoryScanner,
    DICOMTypeCheckingMixin,
    metaclass=SingletonMeta
):
    pass