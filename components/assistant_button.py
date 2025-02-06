# components/assistant_button.py

from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtGui import QIcon, QColor, QPixmap, QPainter
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, pyqtProperty


class AssistantButton(QPushButton):
    def __init__(self, parent=None, icon_path="icons/chatbot.png", tooltip="Asistente", size=40):
        super().__init__(parent)
        self.icon_path = icon_path
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QPixmap(icon_path).scaled(int(size * 0.6), int(size * 0.6), Qt.KeepAspectRatio, Qt.SmoothTransformation).size())
        self.setFixedSize(size, size)  # Tamaño del botón (cuadrado)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: #3498DB;
                border: none;
                border-radius: {size//2}px;  /* La mitad del tamaño para hacerlo circular */
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: #2980B9;
            }}
            QPushButton:pressed {{
                background-color: #1ABC9C;
            }}
        """)
        self.setToolTip(tooltip)
        self.setCursor(Qt.PointingHandCursor)

        # Añadir sombra para darle profundidad
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(shadow)

        # Animación de pulso
        self.pulse_animation = QPropertyAnimation(self, b"size_")
        self.pulse_animation.setDuration(1000)  # Duración de 1 segundo
        self.pulse_animation.setStartValue(self.size())
        self.pulse_animation.setKeyValueAt(0.5, self.size() + QSize(10, 10))
        self.pulse_animation.setEndValue(self.size())
        self.pulse_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.pulse_animation.setLoopCount(-1)  # Bucle infinito
        self.pulse_animation.start()

    def get_size(self):
        return self.size()

    def set_size(self, size):
        self.resize(size)

    size_ = pyqtProperty(QSize, fget=get_size, fset=set_size)

    def paintEvent(self, event):
        # Pintar el botón circular con bordes suaves
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.palette().button())
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())
        super().paintEvent(event)
