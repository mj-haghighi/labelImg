from typing import Callable
from PyQt5.QtWidgets import QFileSystemModel
from ..mixins import AbstractExplorerModelMixin

class FileSystemModel(QFileSystemModel, AbstractExplorerModelMixin):
    def __init__(self):
        super().__init__()    
    
        
    def scanDirectory(self, path='', onScanDirectoryEnd: Callable = lambda *argv: None):
        """ scan directory for files and folders
        """
        pathIndex = self.setRootPath(path)
        onScanDirectoryEnd(pathIndex)
