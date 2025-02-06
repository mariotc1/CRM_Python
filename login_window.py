# login_window.py
import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFormLayout, QMessageBox, QCompleter, QApplication
)
from PyQt5.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QSize
)
from PyQt5.QtGui import (
    QFont, QColor, QIcon, QPixmap, QLinearGradient, QPalette, QBrush
)

from rotatable_label import RotatableLabel  # Asegúrate de que esta ruta sea correcta
from database_manager import DatabaseManager
from main_window import MainWindow  # Asegúrate de que esta ruta sea correcta

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        try:
            print("Inicializando LoginWindow...")
            self.db_manager = DatabaseManager("empresa.db")
            self.db_manager.connect()

            self.setWindowTitle("Iniciar Sesión - DataNexus")
            self.setWindowIcon(QIcon("images/logoApp.png"))
            self.showFullScreen()

            self.init_ui()
        except Exception as e:
            print(f"Error en el constructor de LoginWindow: {e}")
            self.show_message(f"Error en la inicialización: {str(e)}", QMessageBox.Critical)

    def init_ui(self):
        try:
            print("Configurando la interfaz de usuario de LoginWindow...")
            self.layout_principal = QVBoxLayout()
            self.layout_principal.setContentsMargins(50, 50, 50, 50)
            self.layout_principal.setSpacing(20)
            self.setLayout(self.layout_principal)

            self.set_background()

            # Botón de salir (arriba a la derecha)
            exit_button = QPushButton(self)
            exit_button.setIcon(QIcon("icons/logout.png"))
            exit_button.setIconSize(QSize(30, 30))
            exit_button.setFixedSize(32, 32)
            exit_button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                    border-radius: 16px;
                }
            """)
            exit_button.setCursor(Qt.PointingHandCursor)
            exit_button.clicked.connect(self.close)

            # HEADER layout
            header_layout = QHBoxLayout()
            header_layout.addStretch()
            header_layout.addWidget(exit_button)

            self.layout_principal.addLayout(header_layout)

            # Labels de bienvenida
            welcome_label = QLabel("¡Bienvenido de Nuevo a DataNexus!")
            welcome_label.setAlignment(Qt.AlignCenter)
            welcome_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
            welcome_label.setStyleSheet("color: #ECF0F1; margin-bottom: 10px;")

            subtitle_label = QLabel(
                "Inicia sesión para gestionar los datos de tu empresa de forma sencilla y eficiente", 
                self
            )
            subtitle_label.setAlignment(Qt.AlignCenter)
            subtitle_label.setFont(QFont("Segoe UI", 14))
            subtitle_label.setStyleSheet("color: #BDC3C7; margin-bottom: 30px;")

            # Logo rotatorio (con animación)
            self.logo_label = RotatableLabel(self)
            logo_pixmap = QPixmap("images/logoApp.png").scaled(
                150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.logo_label.setPixmap(logo_pixmap)
            self.logo_label.setAlignment(Qt.AlignCenter)

            # Formulario de login
            form_layout = QFormLayout()
            form_layout.setSpacing(20)

            self.nombre_empresa_input = self.create_input(
                "Nombre de la Empresa", "icons/nombre-empresa.png"
            )
            self.mail_input = self.create_input(
                "Correo Electrónico", "icons/correo-electronico.png"
            )
            self.password_input, self.eye_icon = self.create_password_input()

            form_layout.addRow(self.nombre_empresa_input)
            form_layout.addRow(self.mail_input)
            form_layout.addRow(self.password_input)

            # Botones de inicio y volver
            self.login_button = self.create_button("Iniciar sesión", "#2ECC71", self.login)
            self.back_button = self.create_button(
                "Volver", "#E74C3C", self.go_back
            )

            button_layout = QHBoxLayout()
            button_layout.addWidget(self.login_button)
            button_layout.addWidget(self.back_button)

            # Añadimos los widgets y layouts
            self.layout_principal.addWidget(welcome_label)
            self.layout_principal.addWidget(subtitle_label)
            self.layout_principal.addWidget(self.logo_label)
            self.layout_principal.addSpacing(30)
            self.layout_principal.addLayout(form_layout)
            self.layout_principal.addSpacing(30)
            self.layout_principal.addLayout(button_layout)

            # Enlaces y labels de pie
            forgot_password_link = QLabel("<a href='#'>¿Olvidaste tu contraseña?</a>", self)
            forgot_password_link.setFont(QFont("Segoe UI", 12))
            forgot_password_link.setStyleSheet("color: #ECF0F1;")
            forgot_password_link.setAlignment(Qt.AlignCenter)
            forgot_password_link.setTextInteractionFlags(Qt.TextBrowserInteraction)
            forgot_password_link.setOpenExternalLinks(False)
            forgot_password_link.linkActivated.connect(self.forgot_password)
            self.layout_principal.addWidget(forgot_password_link)

            version_label = QLabel("DataNexus CRM v1.0", self)
            version_label.setFont(QFont("Segoe UI", 10))
            version_label.setStyleSheet("color: #BDC3C7;")
            version_label.setAlignment(Qt.AlignCenter)
            self.layout_principal.addWidget(version_label)

            copyright_label = QLabel(
                "© 2025 DataNexus. Todos los derechos reservados.", self
            )
            copyright_label.setFont(QFont("Segoe UI", 10))
            copyright_label.setStyleSheet("color: #BDC3C7;")
            copyright_label.setAlignment(Qt.AlignCenter)
            self.layout_principal.addWidget(copyright_label)

            # Lanzamos la animación "flip" horizontal del logo
            self.animate_logo()
        except Exception as e:
            print(f"Error en init_ui de LoginWindow: {e}")
            self.show_message(f"Error en la interfaz de usuario: {str(e)}", QMessageBox.Critical)

    def set_background(self):
        try:
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor("#2C3E50"))
            gradient.setColorAt(1, QColor("#3498DB"))

            palette = self.palette()
            palette.setBrush(self.backgroundRole(), QBrush(gradient))
            self.setPalette(palette)
            self.setAutoFillBackground(True)
        except Exception as e:
            print(f"Error al establecer el fondo: {e}")

    def resizeEvent(self, event):
        try:
            super().resizeEvent(event)
            # Actualizar el degradado al cambiar el tamaño
            self.set_background()
        except Exception as e:
            print(f"Error en resizeEvent de LoginWindow: {e}")

    def create_input(self, placeholder, icon_path):
        try:
            input_layout = QHBoxLayout()
            input_layout.setSpacing(10)

            line_edit = QLineEdit(self)
            line_edit.setPlaceholderText(placeholder)
            line_edit.setFont(QFont("Segoe UI", 14))
            line_edit.setStyleSheet(
                """
                QLineEdit {
                    padding: 12px;
                    border-radius: 6px;
                    border: 2px solid #34495E;
                    background-color: #ECF0F1;
                    color: #2C3E50;
                }
                QLineEdit:focus {
                    border: 2px solid #3498DB;
                }
                """
            )

            if placeholder == "Correo Electrónico":
                completer = QCompleter(["@gmail.com", "@hotmail.com", "@outlook.com", "@yahoo.com"])
                line_edit.setCompleter(completer)

            icon_label = QLabel(self)
            icon_pixmap = QPixmap(icon_path).scaled(
                24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            icon_label.setPixmap(icon_pixmap)
            icon_label.setFixedSize(24, 24)

            input_layout.addWidget(icon_label)
            input_layout.addWidget(line_edit)

            return input_layout
        except Exception as e:
            print(f"Error al crear input '{placeholder}': {e}")
            return QHBoxLayout()

    def create_password_input(self):
        try:
            input_layout = QHBoxLayout()
            input_layout.setSpacing(10)

            password_input = QLineEdit(self)
            password_input.setPlaceholderText("Contraseña")
            password_input.setEchoMode(QLineEdit.Password)
            password_input.setFont(QFont("Segoe UI", 14))
            password_input.setStyleSheet(
                """
                QLineEdit {
                    padding: 12px;
                    border-radius: 6px;
                    border: 2px solid #34495E;
                    background-color: #ECF0F1;
                    color: #2C3E50;
                }
                QLineEdit:focus {
                    border: 2px solid #3498DB;
                }
                """
            )

            icon_label = QLabel(self)
            icon_pixmap = QPixmap("icons/contrasena.png").scaled(
                24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            icon_label.setPixmap(icon_pixmap)
            icon_label.setFixedSize(24, 24)

            eye_icon = QPushButton(self)
            eye_icon.setIcon(QIcon("icons/ic_visibility_off.png"))
            eye_icon.setIconSize(QSize(24, 24))
            eye_icon.setFixedSize(24, 24)
            eye_icon.setStyleSheet(
                """
                QPushButton {
                    border: none;
                    background-color: transparent;
                }
                QPushButton:hover {
                    background-color: rgba(52, 152, 219, 0.1);
                    border-radius: 12px;
                }
                """
            )
            eye_icon.setCursor(Qt.PointingHandCursor)
            eye_icon.clicked.connect(
                lambda: self.toggle_password_visibility(password_input, eye_icon)
            )

            input_layout.addWidget(icon_label)
            input_layout.addWidget(password_input)
            input_layout.addWidget(eye_icon)

            return input_layout, eye_icon
        except Exception as e:
            print(f"Error al crear password input: {e}")
            return QHBoxLayout(), QPushButton()

    def toggle_password_visibility(self, password_input, eye_icon):
        try:
            if password_input.echoMode() == QLineEdit.Password:
                password_input.setEchoMode(QLineEdit.Normal)
                eye_icon.setIcon(QIcon("icons/ic_visibility.png"))
            else:
                password_input.setEchoMode(QLineEdit.Password)
                eye_icon.setIcon(QIcon("icons/ic_visibility_off.png"))
        except Exception as e:
            print(f"Error al alternar visibilidad de la contraseña: {e}")

    def create_button(self, text, color, on_click):
        try:
            button = QPushButton(text, self)
            button.setFont(QFont("Segoe UI", 16, QFont.Bold))
            button.setCursor(Qt.PointingHandCursor)
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    padding: 12px 20px;
                    border-radius: 6px;
                    border: none;
                    transition: background-color 0.3s;
                }}
                QPushButton:hover {{
                    background-color: {self.lighten_color(color)};
                }}
                """
            )
            button.clicked.connect(on_click)
            return button
        except Exception as e:
            print(f"Error al crear botón '{text}': {e}")
            return QPushButton()

    def lighten_color(self, color):
        try:
            c = QColor(color)
            h, s, l, _ = c.getHsl()
            return QColor.fromHsl(h, s, min(255, l + 20)).name()
        except Exception as e:
            print(f"Error al aclarar el color '{color}': {e}")
            return color

    def animate_logo(self):
        try:
            self.logo_animation = QPropertyAnimation(self.logo_label, b"rotation")
            self.logo_animation.setDuration(10000)
            self.logo_animation.setStartValue(0)
            self.logo_animation.setEndValue(360)
            self.logo_animation.setEasingCurve(QEasingCurve.InOutQuad)
            self.logo_animation.setLoopCount(-1)
            self.logo_animation.start()
        except Exception as e:
            print(f"Error en animación del logo: {e}")

    def forgot_password(self):
        try:
            email = self.mail_input.itemAt(1).widget().text()
            if not email:
                self.show_message("Por favor, ingresa tu correo electrónico.", QMessageBox.Warning)
                return

            # Aquí deberías implementar la lógica para enviar un correo de recuperación
            # Por ahora, solo mostraremos un mensaje informativo
            self.show_message(
                f"Se ha enviado un correo de recuperación a {email}. "
                "Por favor, revisa tu bandeja de entrada.",
                QMessageBox.Information
            )
        except Exception as e:
            print(f"Error al procesar 'Olvidaste tu contraseña': {e}")
            self.show_message(f"Error al enviar el correo: {str(e)}", QMessageBox.Critical)

    def login(self):
        try:
            nombre_empresa = self.nombre_empresa_input.itemAt(1).widget().text().strip()
            mail = self.mail_input.itemAt(1).widget().text().strip()
            password = self.password_input.itemAt(1).widget().text()

            print(f"Intentando iniciar sesión con Empresa: {nombre_empresa}, Correo: {mail}")

            if not nombre_empresa or not mail or not password:
                self.show_message("Todos los campos son obligatorios.", QMessageBox.Warning)
                return

            # Crea la instancia de DatabaseManager usando el nombre de la empresa
            safe_company_name = "".join(c for c in nombre_empresa if c.isalnum() or c in (' ','.','_')).rstrip()
            db_filename = f"{safe_company_name}.db"
            company_db_manager = DatabaseManager(db_filename)
            company_db_manager.connect()

            # Verifica las credenciales en la base de datos específica
            if company_db_manager.check_login(mail, password, nombre_empresa):
                print("Inicio de sesión exitoso.")
                self.show_message("¡Inicio de sesión exitoso!", QMessageBox.Information)
                self.main_window = MainWindow(nombre_empresa, company_db_manager)
                self.main_window.show()
                self.close()
            else:
                print("Credenciales incorrectas o empresa no registrada.")
                self.show_message("Credenciales incorrectas o empresa no registrada.", QMessageBox.Warning)
        except Exception as e:
            print(f"Error al intentar iniciar sesión: {e}")
            self.show_message(f"Error al intentar iniciar sesión: {str(e)}", QMessageBox.Critical)

    def go_back(self):
        try:
            from welcome_window import WelcomeWindow
            self.welcome_window = WelcomeWindow()
            self.welcome_window.show()
            self.close()
        except Exception as e:
            print(f"Error al regresar a WelcomeWindow: {e}")
            self.show_message(f"Error al regresar: {str(e)}", QMessageBox.Critical)

    def show_message(self, message, icon):
        try:
            msg = QMessageBox()
            msg.setIcon(icon)
            msg.setText(message)
            msg.setWindowTitle("DataNexus")
            msg.setStyleSheet(
                """
                QMessageBox {
                    background-color: #ECF0F1;
                }
                QMessageBox QLabel {
                    color: #2C3E50;
                }
                QMessageBox QPushButton {
                    background-color: #3498DB;
                    color: white;
                    padding: 5px 15px;
                    border-radius: 3px;
                    border: none;
                }
                QMessageBox QPushButton:hover {
                    background-color: #2980B9;
                }
                """
            )
            msg.exec_()
        except Exception as e:
            print(f"Error al mostrar mensaje: {e}")

    from rotatable_label import RotatableLabel