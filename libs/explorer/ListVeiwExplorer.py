from PyQt5.QtWidgets import QFileSystemModel, QDockWidget
from PyQt5.QtWidgets import QListView
from PyQt5.QtCore import QModelIndex


class ListView(QListView):
    def __init__(
        self,
        parent=None,
        onClicked=lambda *argv: None,
        onDoubleClicked=lambda *argv: None,
        model=QFileSystemModel(),
    ):
        super().__init__()
        self.parent = parent
        self.setModel(model)
        self.clicked.connect(lambda index:
                             onClicked(*self._translateIndex(index)))
        self.doubleClicked.connect(lambda index:
                                   onDoubleClicked(*self._translateIndex(index)))
        self._configStyle()

    def _configStyle(self):
        self.setFlow(QListView.LeftToRight)
        self.setWrapping(True)        

    def _translateIndex(self, index):
        indexItem = self.model().index(index.row(), 0, index.parent())
        fileName = self.model().fileName(indexItem)
        filePath = self.model().filePath(indexItem)
        return fileName, filePath

    def setRootPath(self, path=''):
        pathIndex = self.model().setRootPath(path)
        self.setRootIndex(pathIndex)
