from PyQt5.QtCore import Qt
from PyQt5.Qt import QWidget, QLabel, QVBoxLayout, QLayout
from PyQt5.QtGui import QPixmap
from ..imageDataItem import ImageDataItem

class ImagePreviewItem(QWidget):
    def __init__(
        self,
        imageDataItem: ImageDataItem
    ):
        super().__init__()

        self._data = imageDataItem
        self.data.view = self
        self._organizeLayout()
        
    def markAsAnotated(self):
        """ Change style sheet to mark as anotated
        """
        self.setStyleSheet(
            """
            QWidget {
            background-color: rgb(0, 255, 0);
            }
            """
        )

    @property
    def data(self)-> ImageDataItem:
        return self._data

    def _organizeLayout(self):
        pixmap = QPixmap.fromImage(self.data.qImage)
        pixmap = pixmap.scaledToHeight(200)
        preview = QLabel()
        preview.setPixmap(pixmap)
        preview.setFixedSize(pixmap.size())

        name = QLabel(self.data.displayText)
        name.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(preview)
        layout.addWidget(name)
        layout.addStretch()
        layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(layout)
