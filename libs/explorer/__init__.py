from PyQt5.QtWidgets import QDockWidget, QHBoxLayout, QListWidget, QWidget, QSplitter
from PyQt5.QtCore import Qt
from .TreeVeiwExplorer import TreeView
from .ListVeiwExplorer import ListView
from .DirectoryUtils import getExt
from .ImagePreviewView import ImagePreviewView 

class ExplorerDoc(QDockWidget):

    def __init__(
        self,
        parent  = None,
        name    = '&Explorer',
        onImageItemClick = lambda argv: None
    ):
        super().__init__()
        self.treeView = TreeView(parent=self, onDoubleClicked=self.onTreeViewDoubleClicked)#, onExpand=)
        self.listView = ImagePreviewView(parent=self, onClicked=onImageItemClick)#, onClick=)
        self.setParent(parent)
        self.setWindowTitle(name)
        self._organizeLayout()
        
    @property
    def allowedExt(self):
        return ['jpeg', 'png']

    def _organizeLayout(self):
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.treeView)
        splitter.addWidget(self.listView)
        splitter.setSizes([250, 750])
        self.setWidget(splitter)

    def loadContent(self, path):
        self.treeView.loadContent(dirPath=path)
        self.listView.loadContent(dirPath=path)


    def onTreeViewDoubleClicked(self, filename, filepath):
        if getExt(filename).lower() in self.allowedExt:
            return
        self.listView.loadContent(dirPath=filepath)
