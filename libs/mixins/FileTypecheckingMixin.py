import pydicom

class AbstractFileTypecheckingMixin:

    def isMyType(self, name: str, path: str = None):
        raise Exception("this methoud is not implemented")


class PngJpegTypeCheckingMixin(AbstractFileTypecheckingMixin):

    def __init__(self):
        self.validExt = ['png', 'jpeg', 'jpg']

    def isMyType(self, name: str, path: str = None):
        if name.endswith(tuple(self.validExt)):
            return True
        return False


class DICOMTypeCheckingMixin(AbstractFileTypecheckingMixin):

    def __init__(self):
        self.validExt = ['dcm']

    def isMyType(self, name: str, path: str):
        if name.endswith(tuple(self.validExt)):
            return True
        try:
            pydicom.dcmread(path)
            return True
        except:
            return False


class XMLTypeCheckingMixin(AbstractFileTypecheckingMixin):

    def __init__(self):
        self.validExt = ['xml']

    def isMyType(self, name: str):
        if name.endswith(tuple(self.validExt)):
            return True
        return False


class JsonTypeCheckingMixin(AbstractFileTypecheckingMixin):

    def __init__(self):
        self.validExt = ['json']

    def isMyType(self, name: str):
        if name.endswith(tuple(self.validExt)):
            return True
        return False
