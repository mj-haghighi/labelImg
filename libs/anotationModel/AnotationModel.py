from ..anotationShapesModel import AbstractAnotationShapeModel, RectangleModel


class AnotationModel:
    """ Anotation class
    """

    def __init__(self, shape: AbstractAnotationShapeModel, lable: str = None):
        self.lable = lable
        self.shape = shape
        self._shapeModels = [RectangleModel]

    def toDict(self):
        """ Convert Anotation information to python dictionary
        """
        return {
            'lable': self.lable,
            'shape': self.shape.__class__.__name__,
            'coordinates': self.shape.toDict()
        }

    @staticmethod
    def fromDict(dict_):
        """ Convert python dictionary information to AnotationModel object
        """
        shapeModel = None
        for sm in self._shapeModels:
            if sm.__class__.__name__ == dict_['shape']:
                shapeModel = sm
                break
        if shapeModel is None:
            raise Exception("!!! 'shape' not supported !!!")

        return AnotationModel(
            lable=dict_['lable'],
            shape=shapeModel.fromDict(dict_['coordinates'])
        )
