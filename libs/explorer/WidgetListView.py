from PyQt5.QtWidgets import QFileSystemModel, QDockWidget
from PyQt5.QtWidgets import QListView, QListWidget, QListWidgetItem, QWidget, QLabel, QVBoxLayout, QLayout
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from typing import List
import re


class ImagePreview(QWidget):
    def __init__(
        self,
        imgPath,
    ):
        super().__init__()
        self.imagePath = imgPath
        self.imageName = re.split(r'\\|/', self.imagePath)[-1]

        self._organizeLayout()

    @property
    def fileName(self):
        return self.imageName
    @property
    def filePath(self):
        return self.imagePath

    def _organizeLayout(self):
        pixmap = QPixmap(self.imagePath)
        pixmap = pixmap.scaledToHeight(200)

        preview = QLabel()
        preview.setPixmap(pixmap)
        preview.setFixedSize(pixmap.size())

        name = QLabel(self.imageName)
        name.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(preview)
        layout.addWidget(name)
        layout.addStretch()
        layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(layout)


class ImagesModel:
    def __init__(
        self,
        paths: List[str]
    ):
        self.paths = paths


class WidgetListView(QListWidget):
    def __init__(
        self,
        parent=None,
        itemWidget=ImagePreview,
        onClicked=lambda *argv: None,
        onDoubleClicked=lambda *argv: None,
    ):
        super().__init__()
        self.parent = parent
        self.itemWidget_ = itemWidget
        self.itemClicked.connect(lambda item:
                                 onClicked(*self._translateItem(item)))
        self.itemDoubleClicked.connect(lambda index:
                                       onDoubleClicked(*self._translateItem(item)))
        self._configStyle()
        self._model = None

    def setModel(self, model):
        self._model = model
        self._organizeLayout()

    def _organizeLayout(self):
        for path in self.model().paths:
            itemWidget_ = self.itemWidget_(imgPath=path)
            item = QListWidgetItem()
            item.setSizeHint(itemWidget_.sizeHint())

            self.addItem(item)
            self.setItemWidget(item, itemWidget_)

    def model(self):
        return self._model

    def _configStyle(self):
        self.setFlow(QListView.LeftToRight)
        self.setWrapping(True)

    def _translateItem(self, item):
        iw = self.itemWidget(item) 
        return iw.fileName, iw.filePath

    def setRootPath(self, path=''):
        pass
