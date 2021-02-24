
from PyQt5.QtWidgets import QTreeView
from PyQt5.QtCore import QModelIndex
from functools import partial
from .Mixins import AbstractExplorerViewMixin
from .FileSystemModel import FileSystemModel


class TreeView(QTreeView, AbstractExplorerViewMixin):
    def __init__(
        self,
        parent=None,
        onExpanded=lambda *argv: None,
        onClicked=lambda *argv: None,
        onDoubleClicked=lambda *argv: None,
        model=FileSystemModel()
    ):
        super().__init__()
        self.parent = parent
        self._configStyle()
        self.setModel(model)
        self.expanded.connect(lambda index:
                              onExpanded(*self._translateIndex(index)))
        self.clicked.connect(lambda index:
                             onClicked(*self._translateIndex(index)))
        self.doubleClicked.connect(lambda index:
                                   onDoubleClicked(*self._translateIndex(index)))


    @property
    def viewModel(self):
        return self.model()

    def _configStyle(self):
        self.setAnimated(True)
        self.setIndentation(20)
        self.setSortingEnabled(True)

    def _translateIndex(self, index):
        indexItem = self.viewModel.index(index.row(), 0, index.parent())
        fileName = self.viewModel.fileName(indexItem)
        filePath = self.viewModel.filePath(indexItem)
        return fileName, filePath

    def loadContent(self, dirPath):
        self.viewModel.scanDirectory(
            path=dirPath,
            onScanDirectoryEnd=lambda pathIndex: self.setRootIndex(pathIndex))
