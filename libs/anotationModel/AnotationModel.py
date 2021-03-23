from ..anotationShapesModel import AbstractAnotationShapeModel, RectangleModel


class AnotationModel:
    """ Anotation class
    """
    availableShapeModels = [RectangleModel]

    def __init__(self, shape: AbstractAnotationShapeModel, label: str = None):
        self.label = label
        self.shape = shape

    def copy(self):
        return AnotationModel(
            label=self.label,
            shape=self.shape.copy())

    def toDict(self):
        """ Convert Anotation information to python dictionary
        """
        return {
            'label': self.label,
            'shape': self.shape.__class__.__name__,
            'coordinates': self.shape.toDict()
        }

    @staticmethod
    def fromDict(dict_):
        """ Convert python dictionary information to AnotationModel object
        """
        shapeModel = None
        for sm in AnotationModel.availableShapeModels:
            if sm.__name__ == dict_['shape']:
                shapeModel = sm
                break
        if shapeModel is None:
            raise Exception("!!! 'shape' not supported !!!")

        return AnotationModel(
            label=dict_['label'],
            shape=shapeModel.fromDict(dict_['coordinates'])
        )
