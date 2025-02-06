import math
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtGui import QPainter, QPixmap

class RotatableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._rotation = 0
        self._pixmap = None

    def setPixmap(self, pixmap):
        super().setPixmap(pixmap)
        self._pixmap = pixmap

    @pyqtProperty(float)
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, angle):
        self._rotation = angle
        self.update()

    def paintEvent(self, event):
        if not self._pixmap:
            super().paintEvent(event)
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        w = self.width()
        h = self.height()

        # Translación para centrar
        painter.translate(w / 2, h / 2)

        # Convertir grados a radianes
        angle_radians = math.radians(self._rotation)
        # Efecto flip horizontal:
        scale_x = math.cos(angle_radians)
        painter.scale(scale_x, 1.0)

        pw = self._pixmap.width()
        ph = self._pixmap.height()
        painter.translate(-pw / 2, -ph / 2)

        painter.drawPixmap(0, 0, self._pixmap)