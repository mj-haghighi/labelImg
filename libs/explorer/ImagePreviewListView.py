import re
from typing import List
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QFileSystemModel, QDockWidget, QListView, QListWidget, QListWidgetItem, QWidget, QLabel, QVBoxLayout, QLayout
from ..imageDataModel import ImageDataModel
from ..mixins import AbstractExplorerViewMixin
from ..imageViewItem import ImagePreviewItem

class ImagePreviewListView(QListWidget, AbstractExplorerViewMixin):
    def __init__(
        self,
        parent=None,
        itemWidgetComponent=ImagePreviewItem,
        onClicked=lambda *argv: None,
        onDoubleClicked=lambda *argv: None,
    ):
        super().__init__()
        self.parent = parent
        self.itemWidgetComponent = itemWidgetComponent
        self.itemClicked.connect(lambda item:
                                 onClicked(self._translateIndex(item)))
        self.itemDoubleClicked.connect(lambda item:
                                       onDoubleClicked(self._translateIndex(item)))
        self._configStyle()
        self._items = []

    @property
    def items(self) -> List[ImagePreviewItem]:
        return self._items

    def _configStyle(self):
        self.setFlow(QListView.LeftToRight)
        self.setWrapping(True)

    def _translateIndex(self, index):
        item = index
        iw = self.itemWidget(item)
        return iw

    def loadContent(self, imagesDataModel: List[ImageDataModel]):
        """ Load View content
        """
        self._organizeLayout(imagesDataModel)

    def _organizeLayout(self, imagesDataModel: List[ImageDataModel]):
        self.clear()
        self._items = []
        for i, imageDataModel in enumerate(imagesDataModel):
            iw = self.itemWidgetComponent(imageDataModel, indx=i)
            self.items.append(iw)
            item = QListWidgetItem()
            item.setSizeHint(iw.sizeHint())
            self.addItem(item)
            self.setItemWidget(item, iw)
