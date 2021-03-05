from ..SingletonMeta import SingletonMeta
from .AbstractRepository import AbstractRepository
from typing import List, Dict
from ..imageDataModel import ImageDataModel


class ImageDataRepository(AbstractRepository, metaclass=SingletonMeta):
    """ Repository for 'ImageDataModel's
    """
    def __init__(self):
        super().__init__()
        self._idToItems = {}

    @property
    def items(self) -> List[ImageDataModel]:
        return super().items

    @property
    def idToItems(self) -> Dict[str, List[ImageDataModel]]:
        """ id to items map
        """
        return self._idToItems

    def clear(self):
        super().clear()
        self._idToItems = {}

    def AddItem(self, item: ImageDataModel):
        super().AddItem(item)
        if 'id' in item.extra.keys():
            item.extra['id'] = 0

        if item.extra['id'] not in self.idToItems.keys():
            self.idToItems[item.extra['id']] = []
        
        self.idToItems[item.extra['id']].append(item)