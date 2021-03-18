import re
from typing import List
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QFileSystemModel, QDockWidget, QListView, QListWidget, QListWidgetItem, QWidget, QLabel, QVBoxLayout, QLayout
from ..imageDataModel import ImageDataModel
from ..mixins import AbstractExplorerViewMixin
from ..imageViewItem import ImagePreviewItem

class ImagePreviewListView(QWidget, AbstractExplorerViewMixin):
    def __init__(
        self,
        parent=None,
        itemWidgetComponent=ImagePreviewItem,
        onClicked=lambda *argv: None,
        onDoubleClicked=lambda *argv: None,
        onScroll=lambda *argv: None
    ):
        super().__init__()
        self.parent = parent
        self.itemWidgetComponent = itemWidgetComponent
        self.__onScroll = onScroll
        self.__listView = QListWidget(parent=self)
        self.__listView.itemClicked.connect(lambda item:onClicked(self._translateIndex(item)))
        self.__listView.itemDoubleClicked.connect(lambda item:onDoubleClicked(self._translateIndex(item)))
        self.__status = QLabel()
        self.__scrollStep = 1
        self._configStyle()
        self._items = []

    @property
    def items(self) -> List[ImagePreviewItem]:
        return self._items

    def _configStyle(self):
        layout = QVBoxLayout()
        layout.addWidget(self.__status)
        layout.addWidget(self.__listView)
        self.setLayout(layout)
        self.__listView.setFlow(QListView.LeftToRight)
        self.__listView.setWrapping(True)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        y = (delta and delta // abs(delta))
        self.__scrollStep +=1
        if not self.__scrollStep % 20 == 0:
            return
        self.__scrollStep = 1
        self.__onScroll(y > 0)

    def item(self, indx):
        """ return item with index 'indx'
        """ 
        return self.__listView.item(indx)

    def _translateIndex(self, index):
        item = index
        iw = self.__listView.itemWidget(item)
        return iw

    def loadContent(self, imagesDataModel: List[ImageDataModel]):
        """ Load View content
        """
        self._organizeLayout(imagesDataModel)

    def setStatusText(self, text: str):
        self.__status.setText(text)

    def _organizeLayout(self, imagesDataModel: List[ImageDataModel]):
        self.__listView.clear()
        self.__status.setText('')
        self._items = []

        for i, imageDataModel in enumerate(imagesDataModel):
            iw = self.itemWidgetComponent(imageDataModel, indx=i)
            self.items.append(iw)
            item = QListWidgetItem()
            item.setSizeHint(iw.sizeHint())

            self.__listView.addItem(item)
            self.__listView.setItemWidget(item, iw)
