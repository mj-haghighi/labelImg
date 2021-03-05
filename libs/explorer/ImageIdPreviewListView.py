import re
from typing import List, Callable
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QFileSystemModel, QDockWidget, QListView, QListWidget, QListWidgetItem, QWidget, QLabel, QVBoxLayout, QLayout
from .ImagePreviewModel import ImagePreviewModel, ImageDataModel
from ..mixins import AbstractExplorerViewMixin
from ..imageViewItem import ImagePreviewItem


class ImageIdPreviewListView(QListWidget, AbstractExplorerViewMixin):
    def __init__(
        self,
        parent=None,
        itemWidgetComponent=ImagePreviewItem,
        onClicked: Callable[[ImagePreviewItem], None] = lambda *argv: None,
        onDoubleClicked: Callable[[ImagePreviewItem], None] = lambda *argv: None,
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
        return iw

    def loadContent(self, imagesDataModel: List[ImageDataModel]):
        """ Load View content
        """
        for dModel in imagesDataModel:
            dModel.displayText = dModel.extra['id'] 
        self._organizeLayout(imagesDataModel)

    def _organizeLayout(self, imageDataItems: List[ImageDataModel]):
        self.clear()
        for i, imageDataItem in enumerate(imageDataItems):
            iw = self.itemWidgetComponent(imageDataItem=imageDataItem, indx=i)
            item = QListWidgetItem()
            item.setSizeHint(iw.sizeHint())

            self.addItem(item)
            self.setItemWidget(item, iw)
