from PyQt5.QtWidgets import QFileSystemModel
from .Mixins import AbstractExplorerModelMixin
from typing import Callable

class FileSystemModel(QFileSystemModel, AbstractExplorerModelMixin):
    def __init__(self):
        super().__init__()    
    
        
    def scanDirectory(self, path='', onScanDirectoryEnd: Callable = lambda *argv: None):
        """ scan directory for files and folders
        """
        pathIndex = self.setRootPath(path)
        onScanDirectoryEnd(pathIndex)
