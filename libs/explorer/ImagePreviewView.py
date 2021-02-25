import re
from typing import List
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QFileSystemModel, QDockWidget, QListView, QListWidget, QListWidgetItem, QWidget, QLabel, QVBoxLayout, QLayout
from .ImagePreviewModel import ImagePreviewModel, ImageDataItem
from ..mixins import AbstractExplorerViewMixin


class ImagePreviewItem(QWidget):
    def __init__(
        self,
        imageDataItem: ImageDataItem
    ):
        super().__init__()

        self.data = imageDataItem
        self._organizeLayout()

    def _organizeLayout(self):
        pixmap = QPixmap.fromImage(self.data.qImage)
        pixmap = pixmap.scaledToHeight(200)
        preview = QLabel()
        preview.setPixmap(pixmap)
        preview.setFixedSize(pixmap.size())

        name = QLabel(self.data.name)
        name.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(preview)
        layout.addWidget(name)
        layout.addStretch()
        layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(layout)


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
                                 onClicked(*self._translateIndex(item)))
        self.itemDoubleClicked.connect(lambda index:
                                       onDoubleClicked(*self._translateIndex(item)))
        self._configStyle()
        self._model = model

    def _configStyle(self):
        self.setFlow(QListView.LeftToRight)
        self.setWrapping(True)

    def _translateIndex(self, index):
        item = index
        iw = self.itemWidget(item)
        return iw.data.name, iw.data.path

    def loadContent(self, dirPath):
        """ Load View content
        """
        self.viewModel.scanDirectory(
            path=dirPath,
            onScanDirectoryEnd=lambda imageDataItems:
                self._organizeLayout(imageDataItems))

    @property
    def viewModel(self):
        return self._model

    def _organizeLayout(self, imageDataItems: List[ImageDataItem]):
        self.clear()
        for imageDataItem in imageDataItems:

            iw = self.itemWidgetComponent(imageDataItem=imageDataItem)
            item = QListWidgetItem()
            item.setSizeHint(iw.sizeHint())

            self.addItem(item)
            self.setItemWidget(item, iw)
