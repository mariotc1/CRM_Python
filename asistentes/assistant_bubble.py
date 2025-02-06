# assistants/assistant_bubble.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QPoint, QRectF, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPixmap, QColor, QLinearGradient


class AssistantBubble(QDialog):
    """
    Diálogo personalizado en forma de burbuja (con 'pico') que sale del botón.
    Con Qt.Popup se cierra automáticamente al pinchar fuera.
    Incluye un efecto 'snake' para atraer la atención del usuario.
    """

    def __init__(self, parent=None, message="", button_ref=None):
        # Qt.Popup => se cierra solo al pinchar fuera
        super().__init__(parent, Qt.Popup | Qt.FramelessWindowHint)
        self.button_ref = button_ref
        self.message = message
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(300, 200)
        self.init_ui()
        self.animate_snake()

    def init_ui(self):
        # Layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("images/logoApp.png").scaled(
            50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        # Texto
        text_label = QLabel(self.message)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setWordWrap(True)
        text_label.setStyleSheet("color: #ECF0F1; font-size: 14px;")

        layout.addWidget(logo_label)
        layout.addWidget(text_label)
        self.setLayout(layout)

    def paintEvent(self, event):
        """
        Dibuja el 'bocadillo' con un pico apuntando al botón del asistente.
        Además aplica un degradado atractivo.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        w = self.width()
        h = self.height()
        r = 15  # Radio de bordes
        margin = 10

        # Path burbuja
        bubble_path = QPainterPath()
        rect = QRectF(margin, margin, w - 2 * margin, h - 2 * margin)
        bubble_path.addRoundedRect(rect, r, r)

        # Pico (abajo-dcha)
        picoSize = 15
        picoPath = QPainterPath()
        xPicoBase = rect.right() - 50  # Ajusta la posición horizontal del pico
        yPicoBase = rect.bottom()
        picoPath.moveTo(xPicoBase, yPicoBase)
        picoPath.lineTo(xPicoBase + picoSize, yPicoBase)
        picoPath.lineTo(xPicoBase + picoSize / 2, yPicoBase + picoSize)
        picoPath.closeSubpath()
        bubble_path.addPath(picoPath)

        # Degradado
        gradient = QLinearGradient(0, 0, 0, h)
        gradient.setColorAt(0, QColor("#2C3E50"))
        gradient.setColorAt(1, QColor("#3498DB"))

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(gradient))
        painter.drawPath(bubble_path)

    def showEvent(self, event):
        """
        Posiciona la burbuja cerca del botón y muestra el asistente.
        """
        super().showEvent(event)
        if self.button_ref is not None:
            btn_pos = self.button_ref.mapToGlobal(QPoint(0, 0))
            btn_w = self.button_ref.width()
            btn_h = self.button_ref.height()

            # Posiciona la burbuja en la esquina inferior derecha
            x = btn_pos.x() + btn_w - self.width() + 30
            y = btn_pos.y() + btn_h + 10  # Ajusta la posición vertical del asistente
            self.move(x, y)

    def animate_snake(self):
        """
        Añade un efecto 'snake' moviendo la burbuja ligeramente de lado a lado.
        """
        self.snake_animation = QPropertyAnimation(self, b"pos")
        self.snake_animation.setDuration(1000)  # Duración de un ciclo completo
        self.snake_animation.setStartValue(self.pos())
        self.snake_animation.setEndValue(self.pos() + QPoint(-10, 0))  # Mover 10 píxeles a la izquierda
        self.snake_animation.setEasingCurve(QEasingCurve.InOutSine)
        self.snake_animation.setLoopCount(-1)  # Repetir indefinidamente
        self.snake_animation.setDirection(QPropertyAnimation.Forward)
        self.snake_animation.start()

    def closeEvent(self, event):
        """
        Detiene la animación cuando se cierra el asistente.
        """
        self.snake_animation.stop()
        super().closeEvent(event)
