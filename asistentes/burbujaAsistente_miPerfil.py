# asistentes/burbujaAsistente_miPerfil.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QPoint, QRectF
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QColor, QLinearGradient, QFont


class AssistantBubbleMiPerfil(QDialog):
    """
    Burbuja en modo Qt.Popup que describe las funcionalidades de la vista de Mi Perfil.
    """
    def __init__(self, parent=None, button_ref=None):
        super().__init__(parent, Qt.Popup | Qt.FramelessWindowHint)
        self.button_ref = button_ref
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(780, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Título
        title_label = QLabel("<h2 style='color:#ECF0F1;'>Asistente: Mi Perfil</h2>")
        title_label.setAlignment(Qt.AlignCenter)

        # Texto con las funcionalidades
        info_label = QLabel(
            "<p style='color:#ECF0F1; font-size:14px;'>"
            "En esta sección puedes gestionar y actualizar tu perfil y los datos de tu empresa:<br><br>"
            "• <b>Foto de Perfil:</b> Cambia tu imagen de perfil para personalizar tu cuenta.<br>"
            "• <b>Nombre:</b> Actualiza el nombre de usuario o de la empresa.<br>"
            "• <b>Correo:</b> Modifica tu dirección de correo electrónico para recibir notificaciones.<br>"
            "• <b>Contraseña:</b> Cambia tu contraseña para mantener la seguridad de tu cuenta.<br>"
            "• <b>Descripción:</b> Añade o edita la descripción de tu empresa para proporcionar más información a tus clientes.<br><br>"
            "Recuerda mantener tu información actualizada para asegurar una mejor gestión y comunicación con tu equipo y clientes."
            "</p>"
        )
        info_label.setAlignment(Qt.AlignLeft)
        info_label.setStyleSheet("background: transparent;")

        layout.addWidget(title_label)
        layout.addWidget(info_label)
        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        w = self.width()
        h = self.height()
        r = 15
        margin = 10
        
        bubble_path = QPainterPath()
        rect = QRectF(margin, margin, w - 2*margin, h - 2*margin)
        bubble_path.addRoundedRect(rect, r, r)
        
        # Pico en la parte superior, apuntando hacia abajo
        picoSize = 15
        picoPath = QPainterPath()

        # Ajusta la posición del pico (ej. cerca del borde derecho)
        xPicoBase = rect.right() - 40
        yPicoBase = rect.top()
        
        picoPath.moveTo(xPicoBase, yPicoBase)
        picoPath.lineTo(xPicoBase + picoSize, yPicoBase)
        picoPath.lineTo(xPicoBase + picoSize/2, yPicoBase - picoSize)
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
        super().showEvent(event)
        if self.button_ref is not None:
            # Calculamos la posición para que la burbuja salga debajo del botón
            btn_pos = self.button_ref.mapToGlobal(QPoint(0, 0))
            btn_w = self.button_ref.width()
            btn_h = self.button_ref.height()
            
            x = btn_pos.x() + btn_w - self.width() + 30
            y = btn_pos.y() + btn_h + 5
            self.move(x, y)