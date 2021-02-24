from ..SingletonMeta import SingletonMeta


class AbstractFileDataCollector(metaclass=SingletonMeta):
    def collect(self, path, name):
        raise Exception("!!! tihs methoud is not implemented !!!")

    def isMyType(self, name):
        raise Exception("!!! tihs methoud is not implemented !!!")


class PngJpegDataCollector(AbstractFileDataCollector):
    def __init__(self):
        self.validExt = ['png', 'jpeg']

    def collect(self, path, name):
        extra = {}
        extra['ext'] = name.split('.')[-1]
        return extra

    def isMyType(self, name: str):
        if name.endswith(tuple(self.validExt)):
            return True
        return False


class DICOMDataCollector(AbstractFileDataCollector):
    def __init__(self):
        self.validExt = ['dcm']
        self.validPrefix = ['I']

    def collect(self, path, name):
        extra = {}
        extra['ext'] = 'dcm'
        return extra

    def isMyType(self, name: str):
        if name.endswith(tuple(self.validExt)) or name.startswith(tuple(self.validPrefix)):
            return True
        return False
