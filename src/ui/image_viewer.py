from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class ImageViewer(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(400, 300)
        self.setStyleSheet("background-color: #f0f0f0; border: 1px solid #cccccc;")

    def setPixmap(self, pixmap):
        if pixmap:
            # Görüntüyü widget boyutuna göre ölçeklendir
            scaled_pixmap = pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            super().setPixmap(scaled_pixmap)
        else:
            super().setPixmap(QPixmap())

    def resizeEvent(self, event):
        # Widget yeniden boyutlandırıldığında görüntüyü de ölçeklendir
        if self.pixmap():
            self.setPixmap(self.pixmap())
