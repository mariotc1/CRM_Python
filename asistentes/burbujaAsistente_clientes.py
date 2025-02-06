from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QPoint, QRectF
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPixmap, QColor, QLinearGradient

class AssistantBubbleClientes(QDialog):
    """
    Burbuja en modo Qt.Popup, con el pico arriba (hacia abajo),
    y un degradado #2C3E50 -> #3498DB al estilo Login.
    """
    def __init__(self, parent=None, button_ref=None):
        super().__init__(parent, Qt.Popup | Qt.FramelessWindowHint)
        self.button_ref = button_ref
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(550, 260)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title_label = QLabel("<h2 style='color:#ECF0F1;'>Asistente: Gestión de Clientes</h2>")
        title_label.setAlignment(Qt.AlignCenter)

        info_label = QLabel(
            "<p style='color:#ECF0F1; font-size:14px;'>"
            "En esta sección podrás:<br>"
            "• <b>Registrar</b> nuevos clientes,<br>"
            "• <b>Actualizar</b> los datos de un cliente existente,<br>"
            "• <b>Eliminar</b> un cliente.<br><br>"
            "Además, verás una <b>tabla</b> con tus clientes,<br>"
            "donde puedes pulsar <b>Editar</b> para cargar los datos en el formulario.<br><br>"
            "¡Disfruta la experiencia con DataNexus!</p>"
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
        r = 15  # radio esquinas
        margin = 10
        
        bubble_path = QPainterPath()
        rect = QRectF(margin, margin, w - 2*margin, h - 2*margin)
        bubble_path.addRoundedRect(rect, r, r)
        
        picoSize = 15
        picoPath = QPainterPath()
        
        # Por ejemplo, cerca de la derecha
        xPicoBase = rect.right() - 40
        yPicoBase = rect.top()
        
        picoPath.moveTo(xPicoBase, yPicoBase)               # Inicio
        picoPath.lineTo(xPicoBase + picoSize, yPicoBase)    # línea horizontal
        picoPath.lineTo(xPicoBase + picoSize/2, yPicoBase - picoSize)  # triángulo arriba
        picoPath.closeSubpath()
        
        bubble_path.addPath(picoPath)
        
        # Degradado vertical #2C3E50 a #3498DB (mismo que en Login)
        gradient = QLinearGradient(0, 0, 0, h)
        gradient.setColorAt(0, QColor("#2C3E50"))
        gradient.setColorAt(1, QColor("#3498DB"))
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(gradient))
        painter.drawPath(bubble_path)

    def showEvent(self, event):
        """
        Coloca la burbuja DEBAJO del botón, para que el pico
        (que está en la parte superior) apunte hacia él.
        """
        super().showEvent(event)
        if self.button_ref is not None:
            btn_pos = self.button_ref.mapToGlobal(QPoint(0, 0))
            btn_w = self.button_ref.width()
            btn_h = self.button_ref.height()
            
            # Movemos la burbuja "debajo" del botón
            x = btn_pos.x() + btn_w - self.width() + 30
            y = btn_pos.y() + btn_h + 5  # un margen de 5 px debajo del botón
            self.move(x, y)
