class AbstractFileTypecheckingMixin:

    def isMyType(self, name: str):
        raise Exception("this methoud is not implemented")


class PngJpegTypeCheckingMixin(AbstractFileTypecheckingMixin):

    def __init__(self):
        self.validExt = ['png', 'jpeg', 'jpg']

    def isMyType(self, name: str):
        if name.endswith(tuple(self.validExt)):
            return True
        return False


class DICOMTypeCheckingMixin(AbstractFileTypecheckingMixin):

    def __init__(self):
        self.validExt = ['dcm']
        self.validPrefix = ['I']

    def isMyType(self, name: str):
        if name.endswith(tuple(self.validExt)) or name.startswith(tuple(self.validPrefix)):
            return True
        return False
