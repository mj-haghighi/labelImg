import re
from typing import List
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QFileSystemModel, QDockWidget, QListView, QListWidget, QListWidgetItem, QWidget, QLabel, QVBoxLayout, QLayout
from .ImagePreviewModel import ImagePreviewModel, ImageDataModel
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

    def _configStyle(self):
        self.setFlow(QListView.LeftToRight)
        self.setWrapping(True)

    def _translateIndex(self, index):
        item = index
        iw = self.itemWidget(item)
        return iw.data

    def loadContent(self, imagesDataModel: List[ImageDataModel]):
        """ Load View content
        """
        self._organizeLayout(imagesDataModel)

    def _organizeLayout(self, imagesDataModel: List[ImageDataModel]):
        self.clear()
        for i, imageDataItem in enumerate(imagesDataModel):
            iw = self.itemWidgetComponent(imageDataModel, indx=i)
            item = QListWidgetItem()
            item.setSizeHint(iw.sizeHint())
            self.addItem(item)
            self.setItemWidget(item, iw)
