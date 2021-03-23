import re
from typing import List, Callable
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QFileSystemModel, QDockWidget, QListView, QListWidget, QListWidgetItem, QWidget, QLabel, QVBoxLayout, QLayout
from ..imageDataModel import ImageDataModel
from ..mixins import AbstractExplorerViewMixin
from ..imageViewItem import ImagePreviewItem


class ImageIdPreviewListView(QWidget, AbstractExplorerViewMixin):
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
        
        self.__listView = QListWidget(parent=self)
        self.__listView.itemClicked.connect(lambda item: onClicked(self._translateIndex(item)))
        self.__listView.itemDoubleClicked.connect(lambda item: onDoubleClicked(self._translateIndex(item)))
        self.__status = QLabel()

        self._configStyle()
        self.__items = []

    @property
    def items(self) -> List[ImagePreviewItem]:
        return self.__items

    def _configStyle(self):
        layout = QVBoxLayout()
        layout.addWidget(self.__status)
        layout.addWidget(self.__listView)
        self.setLayout(layout)
        
        self.__listView.setFlow(QListView.LeftToRight)
        self.__listView.setWrapping(True)

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
        for dModel in imagesDataModel:
            dModel.displayText = 'ID: {}'.format(dModel.extra['id']) 
        self._organizeLayout(imagesDataModel)

    def setStatusText(self, text: str):
        self.__status.setText(text)

    def clear(self):
        self.__listView.clear()
        self.__status.setText('')
        self.__items = []


    def _organizeLayout(self, imagesDataModel: List[ImageDataModel]):
        self.clear()
        for i, imageDataItem in enumerate(imagesDataModel):
            iw = self.itemWidgetComponent(imageDataItem, indx=i)
            self.items.append(iw)
            item = QListWidgetItem()
            item.setSizeHint(iw.sizeHint())

            self.__listView.addItem(item)
            self.__listView.setItemWidget(item, iw)
