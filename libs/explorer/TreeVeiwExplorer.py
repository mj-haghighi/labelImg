from PyQt5.QtWidgets import QFileSystemModel
from PyQt5.QtWidgets import QTreeView
from PyQt5.QtCore import QModelIndex
from functools import partial


class TreeView(QTreeView):
    def __init__(
        self,
        parent=None,
        onExpanded=lambda *argv: None,
        onClicked=lambda *argv: None,
        onDoubleClicked=lambda *argv: None,
        model=QFileSystemModel()
    ):
        super().__init__()
        self.parent = parent
        self.model_ = model
        self.setModel(model)
        self._configStyle()
        self.expanded.connect(lambda index:
                              onExpanded(*self._translateIndex(index)))
        self.clicked.connect(lambda index:
                             onClicked(*self._translateIndex(index)))
        self.doubleClicked.connect(lambda index:
                                   onDoubleClicked(*self._translateIndex(index)))

    def _configStyle(self):
        self.setAnimated(True)
        self.setIndentation(20)
        self.setSortingEnabled(True)

    def _translateIndex(self, index):
        indexItem = self.model().index(index.row(), 0, index.parent())
        fileName = self.model().fileName(indexItem)
        filePath = self.model().filePath(indexItem)
        return fileName, filePath

    def setRootPath(self, path=''):
        pathIndex = self.model().setRootPath(path)
        self.setRootIndex(pathIndex)
