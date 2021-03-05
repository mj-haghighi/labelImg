from .AbstractDirectoryScanner import AbstractDirectoryScanner
from ..mixins import DICOMTypeCheckingMixin
from ..SingletonMeta import SingletonMeta


class DICOMDirectoryScanner(
    AbstractDirectoryScanner,
    DICOMTypeCheckingMixin,
    metaclass=SingletonMeta
):
    pass