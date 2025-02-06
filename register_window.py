# register_window.py
import sys
import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFormLayout, QMessageBox, QCompleter, QProgressBar, QApplication
)
from PyQt5.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QSize
)
from PyQt5.QtGui import (
    QFont, QColor, QIcon, QPixmap, QLinearGradient, QPalette, QBrush
)

from rotatable_label import RotatableLabel
from database_manager import DatabaseManager
from main_window import MainWindow

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        try:
            print("Inicializando RegisterWindow...")
            self.db_manager = DatabaseManager("empresa.db")
            self.db_manager.connect()

            self.setWindowTitle("Registrar Empresa - DataNexus")
            self.setWindowIcon(QIcon("images/logoApp.png"))
            self.showFullScreen()

            self.init_ui()
        except Exception as e:
            print(f"Error en el constructor de RegisterWindow: {e}")
            self.show_message(f"Error en la inicialización: {str(e)}", QMessageBox.Critical)

    def init_ui(self):
        try:
            print("Configurando la interfaz de usuario de RegisterWindow...")
            self.layout_principal = QVBoxLayout()
            self.layout_principal.setContentsMargins(50, 50, 50, 50)
            self.layout_principal.setSpacing(20)
            self.setLayout(self.layout_principal)

            self.set_background()

            # Botón de salir
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

            header_layout = QHBoxLayout()
            header_layout.addStretch()
            header_layout.addWidget(exit_button)

            self.layout_principal.addLayout(header_layout)

            # Labels de bienvenida
            welcome_label = QLabel("¡Regístrate en DataNexus!")
            welcome_label.setAlignment(Qt.AlignCenter)
            welcome_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
            welcome_label.setStyleSheet("color: #ECF0F1; margin-bottom: 10px;")

            subtitle_label = QLabel(
                "Crea una cuenta para gestionar los datos de tu empresa de forma sencilla y eficiente", 
                self
            )
            subtitle_label.setAlignment(Qt.AlignCenter)
            subtitle_label.setFont(QFont("Segoe UI", 14))
            subtitle_label.setStyleSheet("color: #BDC3C7; margin-bottom: 30px;")

            # Logo rotatorio
            self.logo_label = RotatableLabel(self)
            logo_pixmap = QPixmap("images/logoApp.png").scaled(
                150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.logo_label.setPixmap(logo_pixmap)
            self.logo_label.setAlignment(Qt.AlignCenter)

            # Formulario de registro
            form_layout = QFormLayout()
            form_layout.setSpacing(20)

            self.nombre_empresa_input = self.create_input(
                "Nombre de la Empresa", "icons/nombre-empresa.png"
            )
            self.mail_input = self.create_input(
                "Correo Electrónico", "icons/correo-electronico.png"
            )
            self.password_input, self.eye_icon = self.create_password_input()
            self.confirm_password_input, self.eye_icon_confirm = self.create_confirm_password_input()

            form_layout.addRow(self.nombre_empresa_input)
            form_layout.addRow(self.mail_input)
            form_layout.addRow(self.password_input)
            form_layout.addRow(self.confirm_password_input)

            # Indicador de fuerza de contraseña
            self.password_strength_label = QLabel("Fuerza de la contraseña: ")
            self.password_strength_label.setFont(QFont("Segoe UI", 10))
            self.password_strength_label.setStyleSheet("color: #ECF0F1;")
            
            self.password_strength_bar = QProgressBar(self)
            self.password_strength_bar.setFixedHeight(10)
            self.password_strength_bar.setTextVisible(False)
            self.password_strength_bar.setRange(0, 100)
            self.password_strength_bar.setValue(0)
            self.password_strength_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #2C3E50;
                    border-radius: 5px;
                    background-color: #ECF0F1;
                }
                QProgressBar::chunk {
                    background-color: #2ECC71;
                    border-radius: 5px;
                }
            """)

            self.password_input.itemAt(1).widget().textChanged.connect(self.evaluate_password_strength)

            form_layout.addRow(self.password_strength_label)
            form_layout.addRow(self.password_strength_bar)

            # Botones de registro y volver
            self.register_button = self.create_button("Registrar Empresa", "#2ECC71", self.register)
            self.back_button = self.create_button(
                "Volver", "#E74C3C", self.go_back
            )

            button_layout = QHBoxLayout()
            button_layout.addWidget(self.register_button)
            button_layout.addWidget(self.back_button)

            # Añado los widgets y layouts
            self.layout_principal.addWidget(welcome_label)
            self.layout_principal.addWidget(subtitle_label)
            self.layout_principal.addWidget(self.logo_label)
            self.layout_principal.addSpacing(30)
            self.layout_principal.addLayout(form_layout)
            self.layout_principal.addSpacing(30)
            self.layout_principal.addLayout(button_layout)

            # Enlaces y labels de pie
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

            # Animación del logo
            self.animate_logo()
        except Exception as e:
            print(f"Error en init_ui de RegisterWindow: {e}")
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
            self.set_background()
        except Exception as e:
            print(f"Error en resizeEvent de RegisterWindow: {e}")

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

    def create_confirm_password_input(self):
        try:
            input_layout = QHBoxLayout()
            input_layout.setSpacing(10)

            confirm_password_input = QLineEdit(self)
            confirm_password_input.setPlaceholderText("Confirmar Contraseña")
            confirm_password_input.setEchoMode(QLineEdit.Password)
            confirm_password_input.setFont(QFont("Segoe UI", 14))
            confirm_password_input.setStyleSheet(
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
                lambda: self.toggle_password_visibility(confirm_password_input, eye_icon)
            )

            input_layout.addWidget(icon_label)
            input_layout.addWidget(confirm_password_input)
            input_layout.addWidget(eye_icon)

            return input_layout, eye_icon
        except Exception as e:
            print(f"Error al crear confirm password input: {e}")
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

    def evaluate_password_strength(self):
        try:
            password = self.password_input.itemAt(1).widget().text()
            strength, percent = self.get_password_strength(password)

            self.password_strength_label.setText(f"Fuerza de la contraseña: {strength}")

            # Actualizar barra de progreso y color
            self.password_strength_bar.setValue(percent)
            if strength == "Débil":
                self.password_strength_bar.setStyleSheet("""
                    QProgressBar {
                        border: 1px solid #2C3E50;
                        border-radius: 5px;
                        background-color: #ECF0F1;
                    }
                    QProgressBar::chunk {
                        background-color: #E74C3C;
                        border-radius: 5px;
                    }
                """)
            elif strength == "Media":
                self.password_strength_bar.setStyleSheet("""
                    QProgressBar {
                        border: 1px solid #2C3E50;
                        border-radius: 5px;
                        background-color: #ECF0F1;
                    }
                    QProgressBar::chunk {
                        background-color: #F1C40F;
                        border-radius: 5px;
                    }
                """)
            else:
                self.password_strength_bar.setStyleSheet("""
                    QProgressBar {
                        border: 1px solid #2C3E50;
                        border-radius: 5px;
                        background-color: #ECF0F1;
                    }
                    QProgressBar::chunk {
                        background-color: #2ECC71;
                        border-radius: 5px;
                    }
                """)
        except Exception as e:
            print(f"Error al evaluar la fuerza de la contraseña: {e}")

    def get_password_strength(self, password):
        length = len(password)

        has_upper = re.search(r"[A-Z]", password) is not None
        has_lower = re.search(r"[a-z]", password) is not None
        has_digit = re.search(r"\d", password) is not None
        has_special = re.search(r"[#€%!@&$%^&*()_+]", password) is not None

        score = 0

        if length >= 8:
            score += 1
        if has_upper:
            score += 1
        if has_lower:
            score += 1
        if has_digit:
            score += 1
        if has_special:
            score += 1

        if score <= 2:
            return "Débil", 33
        elif score == 3 or score == 4:
            return "Media", 66
        else:
            return "Fuerte", 100

    def register(self):
        try:
            nombre_empresa = self.nombre_empresa_input.itemAt(1).widget().text().strip()
            mail = self.mail_input.itemAt(1).widget().text().strip()
            password = self.password_input.itemAt(1).widget().text()
            confirm_password = self.confirm_password_input.itemAt(1).widget().text()

            # Validaciones básicas:
            if not nombre_empresa or not mail or not password or not confirm_password:
                self.show_message("Todos los campos son obligatorios.", QMessageBox.Warning)
                return

            if password != confirm_password:
                self.show_message("Las contraseñas no coinciden.", QMessageBox.Warning)
                return

            strength, _ = self.get_password_strength(password)
            if strength == "Débil":
                self.show_message("La contraseña es demasiado débil. Por favor, elige una contraseña más fuerte.", QMessageBox.Warning)
                return

            # Verifica si la empresa ya existe en la base maestra
            if self.db_manager.check_company_exists(nombre_empresa):
                self.show_message(f"La empresa {nombre_empresa} ya está registrada.", QMessageBox.Warning)
                return

            # Inserta la empresa en la base
            self.db_manager.insert_empresa(nombre_empresa, mail, password)
            self.show_message(f"Empresa {nombre_empresa} registrada exitosamente!", QMessageBox.Information)
            
            # CREAR LA BASE DE DATOS ESPECÍFICA DE LA EMPRESA
            # Sanitizamos el nombre de la empresa para formar un nombre de archivo válido:
            safe_company_name = "".join(c for c in nombre_empresa if c.isalnum() or c in (' ','.','_')).rstrip()
            db_filename = f"{safe_company_name}.db"  # Por ejemplo, "Avantia.db"

            # Creamos y conectamos el DatabaseManager para esta empresa
            new_db_manager = DatabaseManager(db_filename)
            new_db_manager.connect()
            
            new_db_manager.insert_empresa(nombre_empresa, mail, password)
            
            # Navego al MainWindow pasando el DatabaseManager específico para esta empresa
            self.main_window = MainWindow(nombre_empresa, new_db_manager)
            self.main_window.show()
            self.close()
        except Exception as e:
            print(f"Error al intentar registrar la empresa: {e}")
            self.show_message(f"Error al intentar registrar la empresa: {str(e)}", QMessageBox.Critical)

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

from rotatable_label import RotatableLabel
