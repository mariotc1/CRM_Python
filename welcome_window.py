import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication,
    QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor, QLinearGradient, QPalette, QBrush
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve

from login_window import LoginWindow
from register_window import RegisterWindow
from rotatable_label import RotatableLabel

class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bienvenido - DataNexus CRM")
        self.setWindowIcon(QIcon("images/logoApp.png"))
        self.showFullScreen()
        self.set_background()
        self.init_ui()

    def set_background(self):
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#2C3E50"))
        gradient.setColorAt(1, QColor("#3498DB"))

        palette = self.palette()
        palette.setBrush(self.backgroundRole(), QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        header_layout = QHBoxLayout()
        header_layout.addStretch()
        exit_button = self.create_exit_button()
        header_layout.addWidget(exit_button)
        header_layout.setContentsMargins(0, 20, 20, 0)
        main_layout.addLayout(header_layout)

        main_layout.addStretch()

        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setSpacing(30)

        welcome_label = self.create_label("¡Bienvenido a DataNexus!", 36, QFont.Bold, "#ECF0F1")
        subtitle_label = self.create_label("Gestiona los datos de tu empresa de forma sencilla y eficiente", 18, QFont.Normal, "#BDC3C7")

        self.logo_label = self.create_logo_label()
        self.animate_logo()

        welcome_text = self.create_label("¿Tienes una cuenta?", 24, QFont.Normal, "#ECF0F1")

        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.setAlignment(Qt.AlignCenter)

        self.login_button = self.create_button("Iniciar Sesión", "#2ECC71", "#27AE60")
        self.register_button = self.create_button("Crear Cuenta", "#E74C3C", "#C0392B")

        buttons_layout.addWidget(self.login_button)
        buttons_layout.addWidget(self.register_button)

        content_layout.addWidget(welcome_label)
        content_layout.addWidget(subtitle_label)
        content_layout.addWidget(self.logo_label)
        content_layout.addWidget(welcome_text)
        content_layout.addLayout(buttons_layout)

        main_layout.addLayout(content_layout)

        main_layout.addStretch()

        footer_layout = QVBoxLayout()
        version_label = self.create_label("DataNexus CRM v1.0", 10, QFont.Normal, "#BDC3C7")
        copyright_label = self.create_label("© 2025 DataNexus. Todos los derechos reservados.", 10, QFont.Normal, "#BDC3C7")
        footer_layout.addWidget(version_label)
        footer_layout.addWidget(copyright_label)
        main_layout.addLayout(footer_layout)

    def create_exit_button(self):
        exit_button = QPushButton(self)
        exit_button.setIcon(QIcon("icons/logout.png"))
        exit_button.setIconSize(QSize(30, 30))
        exit_button.setFixedSize(40, 40)
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        exit_button.setCursor(Qt.PointingHandCursor)
        exit_button.clicked.connect(self.close)
        return exit_button

    def create_label(self, text, font_size, font_weight, color):
        label = QLabel(text, self)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Segoe UI", font_size, font_weight))
        label.setStyleSheet(f"color: {color};")
        return label

    def create_logo_label(self):
        logo_label = RotatableLabel(self)
        logo_pixmap = QPixmap("images/logoApp.png").scaled(
            200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        return logo_label

    def create_button(self, text, bg_color, hover_color):
        button = QPushButton(text)
        button.setFixedSize(200, 40)
        # Usamos fuente en negrita para mayor visibilidad
        button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        button.setCursor(Qt.PointingHandCursor)
        
        # Agregar efecto de sombra para resaltar el texto
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setOffset(1, 1)
        shadow.setColor(QColor(0, 0, 0, 160))
        button.setGraphicsEffect(shadow)
        
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {hover_color};
            }}
        """)
        if text == "Iniciar Sesión":
            button.clicked.connect(self.open_login)
        else:
            button.clicked.connect(self.open_register)
        return button

    def animate_logo(self):
        self.logo_animation = QPropertyAnimation(self.logo_label, b"rotation")
        self.logo_animation.setDuration(10000)
        self.logo_animation.setStartValue(0)
        self.logo_animation.setEndValue(360)
        self.logo_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.logo_animation.setLoopCount(-1)
        self.logo_animation.start()

    def open_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def open_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    welcome_window = WelcomeWindow()
    welcome_window.show()
    sys.exit(app.exec_())
