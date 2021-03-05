
class AbstractRepository:
    """ Abstract Repository for other repository classes
    """

    def __init__(self):
        self._items = []

    @property
    def items():
        return self._items

    def AddItem(self, item):
        """ Add item to repository
        """
        self._items.append(item)

    def clear(self):
        self._items = []

    @property
    def itemCount(self) -> int:
        """ count of current items
        """
        return len(self.items)
