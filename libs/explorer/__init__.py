import os
from typing import List, Dict, Callable
from PyQt5.QtWidgets import QDockWidget, QHBoxLayout, QListWidget, QWidget, QSplitter
from PyQt5.QtCore import Qt
from .TreeVeiwExplorer import TreeView
from .ImageIdPreviewListView import ImageIdPreviewListView
from .ImagePreviewListView import ImagePreviewListView
from ..imageDataModel import ImageDataModel
from ..imageViewItem import ImagePreviewItem
from ..directoryScanner import ImageDirectoryScanner
from ..repositories import ImageDataRepository
from ..utils import baseName


class ExplorerDoc(QDockWidget):

    def __init__(
        self,
        parent=None,
        name='&Explorer',
        onImageItemClick: Callable[[ImagePreviewItem], None] = lambda argv: None,
        onIDPreviewClick: Callable[[ImagePreviewItem], None] = lambda argv: None,
        onFolderDoubleClicked=lambda argv: None
    ):
        super().__init__()
        self.treeView = TreeView(
            parent=self,
            onDoubleClicked=lambda filename, filepath: self.onTreeViewDoubleClicked(
                filename, filepath) or onFolderDoubleClicked((filename, filepath)))
        
        self.IdlistView = ImageIdPreviewListView(
            parent=self,
            onClicked=lambda imageWidget: self.loadRelatedImageDataItems(
                imageWidget) or onIDPreviewClick(imageWidget))
       
        self.listView = ImagePreviewListView(
            parent=self, onClicked=lambda imageWidget: onImageItemClick(imageWidget))

        self.setParent(parent)
        self.setWindowTitle(name)
        self.setObjectName(ExplorerDoc.__name__)
        self.onFolderDoubleClicked = onFolderDoubleClicked
        self._organizeLayout()
        self.imageDataRepository = ImageDataRepository()
        self.scanner = ImageDirectoryScanner()

    def _organizeLayout(self):
        splitter = QSplitter(Qt.Horizontal)
        nestedSplitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.treeView)
        splitter.addWidget(nestedSplitter)
        nestedSplitter.addWidget(self.IdlistView)
        nestedSplitter.addWidget(self.listView)
        nestedSplitter.setSizes([300, 700])
        splitter.setSizes([250, 750])

        self.setWidget(splitter)

    def loadContent(self, folderPath):
        self.treeView.loadContent(dirPath=folderPath)
        imgsPath = self.scanner.scan(folderPath)
        for iPath in imgsPath:
            self.imageDataRepository.AddItem(
                ImageDataModel(
                    path=iPath,
                    name=baseName(iPath)
                )
            )
        self.loadIdListViewContent()

    def loadIdListViewContent(self):
        l = []
        for key in self.imageDataRepository.idToItems.keys():
            idModel = self.imageDataRepository.idToItems[key][0].copy()
            l.append(idModel)
        self.IdlistView.loadContent(l)

    def loadImagePreviewListContent(self, _id):
        self.listView.loadContent(
            self.imageDataRepository.idToItems[_id]
        )

    def loadRelatedImageDataItems(self, widget: ImagePreviewItem):
        _id = widget.data.extra['id']
        self.loadImagePreviewListContent(_id)

    def onTreeViewDoubleClicked(self, folderName, folderPath):
        if os.path.isfile(folderPath):
            return
        
        self.imageDataRepository.clear()
        self.listView.clear()
        self.IdlistView.clear()

        imgsPath = self.scanner.scan(folderPath)
        for iPath in imgsPath:
            self.imageDataRepository.AddItem(
                ImageDataModel(
                    path=iPath,
                    name=baseName(iPath)
                )
            )
        self.loadIdListViewContent()
