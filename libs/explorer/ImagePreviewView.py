import re
from typing import List
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QFileSystemModel, QDockWidget, QListView, QListWidget, QListWidgetItem, QWidget, QLabel, QVBoxLayout, QLayout
from .ImagePreviewModel import ImagePreviewModel, ImageDataItem
from ..mixins import AbstractExplorerViewMixin
from ..imageViewItem import ImagePreviewItem


class ImagePreviewView(QListWidget, AbstractExplorerViewMixin):
    def __init__(
        self,
        parent=None,
        itemWidgetComponent=ImagePreviewItem,
        onClicked=lambda *argv: None,
        onDoubleClicked=lambda *argv: None,
        model=ImagePreviewModel()
    ):
        super().__init__()
        self.parent = parent
        self.itemWidgetComponent = itemWidgetComponent
        self.itemClicked.connect(lambda item:
                                 onClicked(self._translateIndex(item)))
        self.itemDoubleClicked.connect(lambda item:
                                       onDoubleClicked(self._translateIndex(item)))
        self._configStyle()
        self._model = model

    def _configStyle(self):
        self.setFlow(QListView.LeftToRight)
        self.setWrapping(True)

    def _translateIndex(self, index):
        item = index
        iw = self.itemWidget(item)
        return iw.data

    def loadContent(self, dirPath):
        """ Load View content
        """
        self.viewModel.scanDirectory(
            path=dirPath,
            onScanDirectoryEnd=lambda imageDataItems:
                self._organizeLayout(imageDataItems))

    @property
    def viewModel(self) -> ImagePreviewModel:
        return self._model

    def _organizeLayout(self, imageDataItems: List[ImageDataItem]):
        self.clear()
        for imageDataItem in imageDataItems:

            iw = self.itemWidgetComponent(imageDataItem=imageDataItem)
            item = QListWidgetItem()
            item.setSizeHint(iw.sizeHint())

            self.addItem(item)
            self.setItemWidget(item, iw)
