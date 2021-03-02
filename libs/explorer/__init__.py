from typing import List, Dict
from PyQt5.QtWidgets import QDockWidget, QHBoxLayout, QListWidget, QWidget, QSplitter
from PyQt5.QtCore import Qt
from .TreeVeiwExplorer import TreeView
from .ListVeiwExplorer import ListView
from .ImagePreviewView import ImagePreviewView 
from ..imageDataItem import ImageDataItem

class ExplorerDoc(QDockWidget):

    def __init__(
        self,
        parent  = None,
        name    = '&Explorer',
        onImageItemClick = lambda argv: None
    ):
        super().__init__()
        self.treeView = TreeView(parent=self, onDoubleClicked=self.onTreeViewDoubleClicked)#, onExpand=)
        self.IdlistView = ImagePreviewView(parent=self, onClicked=lambda imageDataItem: self.loadRelatedImageDataItems(imageDataItem))#, onClick=)
        self.listView = ImagePreviewView(parent=self, onClicked=onImageItemClick)#, onClick=)
        self.setParent(parent)
        self.setWindowTitle(name)
        self._organizeLayout()
        self._IdToImageDataItem = {}
        

    @property
    def IdToImageDataItem(self) -> Dict[int, List[ImageDataItem]]:
        return  self._IdToImageDataItem
    
    @property
    def allowedExt(self):
        return ['jpeg', 'png']
    
    @property
    def imageDataItems(self):
        return self.listView.viewModel.dataItemsList

    def _organizeLayout(self):
        splitter = QSplitter(Qt.Horizontal)
        nestedSplitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.treeView)
        splitter.addWidget(nestedSplitter)
        nestedSplitter.addWidget(self.IdlistView)
        nestedSplitter.addWidget(self.listView)
        nestedSplitter.setSizes([500, 500])
        splitter.setSizes([250, 750])

        self.setWidget(splitter)

    def loadContent(self, path):
        self.treeView.loadContent(dirPath=path)
        self.IdlistView.viewModel.scanDirectory(path, onScanDirectoryEnd=lambda imageDataItems: self.segmentImagesBaseOnIds(imageDataItems))
        self.IdlistView.viewModel.dataItemsList = [self.IdToImageDataItem[ID][0] for ID in self.IdToImageDataItem.keys()] 
        self.IdlistView._organizeLayout(self.IdlistView.viewModel.dataItemsList)


    def loadRelatedImageDataItems(self, imageDataItem):
        self.listView.viewModel.dataItemsList = self.IdToImageDataItem[imageDataItem.extra['id']]
        self.listView._organizeLayout(self.listView.viewModel.dataItemsList)

    def segmentImagesBaseOnIds(self, imageDataItems: List[ImageDataItem]):
        self._IdToImageDataItem = {}
        for imgData in imageDataItems:
            if not ('id' in imgData.extra.keys()):
                imgData.extra['id'] = 0  # set default id
            if not (imgData.extra['id'] in self.IdToImageDataItem.keys()):
                self.IdToImageDataItem[imgData.extra['id']] = []
            self.IdToImageDataItem[imgData.extra['id']].append(imgData)

    def onTreeViewDoubleClicked(self, filename, filepath):
        if filename.split('.')[-1].lower() in self.allowedExt:
            return
        
        self.IdlistView.clear()
        self.listView.clear()
        self.IdlistView.viewModel.scanDirectory(filepath, onScanDirectoryEnd=lambda imageDataItems: self.segmentImagesBaseOnIds(imageDataItems))
        self.IdlistView.viewModel.dataItemsList = [self.IdToImageDataItem[ID][0] for ID in self.IdToImageDataItem.keys()] 
        self.IdlistView._organizeLayout(self.IdlistView.viewModel.dataItemsList)
