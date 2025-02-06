import os
import uuid  # Para generar IDs únicos si es necesario
import datetime  # Para manejar fechas
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFormLayout, QLineEdit, QTextEdit, QFrame, QFileDialog, QMessageBox, QDateEdit
)
from PyQt5.QtGui import QPixmap, QFont, QIcon, QColor
from PyQt5.QtCore import Qt, QSize

from asistentes.burbujaAsistente_miPerfil import AssistantBubbleMiPerfil


class MiPerfilView(QWidget):
    """
    Vista de 'Mi Perfil' para editar datos de usuario/empresa:
    - Foto de perfil
    - Nombre, correo, contraseña
    - Descripción de la empresa
    - Número de teléfono
    - Dirección
    - Burbuja asistente integrada
    """
    def __init__(self, db_manager, empresa_nombre):
        super().__init__()
        self.db_manager = db_manager
        self.empresa_nombre = empresa_nombre
        self.profile_photo_path = None
        self.assistant_bubble = None
        self.init_ui()

    def init_ui(self):
        # Layout principal vertical, sin bordes extra
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1) Encabezado oscuro
        header_frame = self.create_header()
        main_layout.addWidget(header_frame)

        # 2) Contenedor blanco para la foto + formulario
        content_frame = self.create_content()
        main_layout.addWidget(content_frame)

    def create_header(self):
        header_frame = QFrame()
        header_frame.setFixedHeight(80)
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #2C3E50; /* Encabezado oscuro */
            }
        """)

        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(15, 10, 15, 10)
        header_layout.setSpacing(20)

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("images/logoApp.png").scaled(
            100, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # Título
        title_label = QLabel(f"Mi Perfil - {self.empresa_nombre}")
        title_label.setStyleSheet("color: #ECF0F1;")  # Texto blanco
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # Botón de Asistente
        self.assistant_button = QPushButton()
        self.assistant_button.setIcon(QIcon("icons/chatbot.png"))
        self.assistant_button.setIconSize(QSize(32, 32))
        self.assistant_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 5px;
            }
        """)
        self.assistant_button.setCursor(Qt.PointingHandCursor)
        self.assistant_button.clicked.connect(self.show_assistant)

        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.assistant_button)

        return header_frame

    def create_content(self):
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
                margin: 0px;
                padding: 20px;
            }
        """)

        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # 2.1) Sección superior con la foto de perfil y botón "Cambiar Foto"
        photo_layout = QHBoxLayout()
        photo_layout.setSpacing(20)

        # Foto de perfil (por defecto una imagen)
        self.profile_photo_label = QLabel()
        self.profile_photo_label.setFixedSize(120, 120)
        self.profile_photo_label.setStyleSheet("border: 2px solid #BDC3C7; border-radius: 5px;")
        self.profile_photo_label.setAlignment(Qt.AlignCenter)

        # Cargo una imagen si no hay foto
        pix = QPixmap("icons/profile_placeholder.png").scaled(
            70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.profile_photo_label.setPixmap(pix)

        photo_layout.addWidget(self.profile_photo_label)

        # Botón para cambiar la foto
        change_photo_button = QPushButton("Cambiar Foto")
        change_photo_button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        change_photo_button.setStyleSheet(self.button_style("#3498DB"))
        change_photo_button.clicked.connect(self.change_photo)

        photo_layout.addWidget(change_photo_button)
        photo_layout.addStretch()
        content_layout.addLayout(photo_layout)

        # 2.2) Formulario de datos de perfil
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # Campos
        self.nombre_input = self.create_input_with_icon("Nombre", "icons/name_icon.png")
        self.correo_input = self.create_input_with_icon("Correo", "icons/correo-electronico.png")
        self.password_input = self.create_input_with_icon("Contraseña", "icons/contrasena.png")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.numero_input = self.create_input_with_icon("Número de Teléfono", "icons/phone_icon.png")
        self.direccion_input = self.create_input_with_icon("Dirección", "icons/address_icon.png")

        self.descripcion_text = QTextEdit()
        self.descripcion_text.setPlaceholderText("Descripción de la empresa / perfil...")
        self.descripcion_text.setStyleSheet(self.textedit_style())

        # Añadir filas al formulario
        form_layout.addRow("Nombre:", self.nombre_input)
        form_layout.addRow("Correo:", self.correo_input)
        form_layout.addRow("Contraseña:", self.password_input)
        form_layout.addRow("Número de Teléfono:", self.numero_input)
        form_layout.addRow("Dirección:", self.direccion_input)
        form_layout.addRow("Descripción:", self.descripcion_text)

        content_layout.addLayout(form_layout)

        # 2.3) Botones "Guardar" y "Cancelar"
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        self.save_button = QPushButton("Guardar Cambios")
        self.save_button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.save_button.setStyleSheet(self.button_style("#2ECC71"))
        self.save_button.clicked.connect(self.save_profile)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.cancel_button.setStyleSheet(self.button_style("#E74C3C"))
        self.cancel_button.clicked.connect(self.cancel_edit)

        btn_layout.addWidget(self.save_button)
        btn_layout.addWidget(self.cancel_button)
        content_layout.addLayout(btn_layout)

        return content_frame

    def change_photo(self):
        """
        Permite al usuario seleccionar una imagen desde el sistema de archivos.
        """
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Seleccionar foto de perfil", "", "Imágenes (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.profile_photo_path = file_path
            pix = QPixmap(file_path).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.profile_photo_label.setPixmap(pix)

    def save_profile(self):
        """
        Lógica para guardar los cambios en la BD.
        """
        nombre = self.nombre_input.text().strip()
        correo = self.correo_input.text().strip()
        password = self.password_input.text().strip()
        numero = self.numero_input.text().strip()
        direccion = self.direccion_input.text().strip()
        descripcion = self.descripcion_text.toPlainText().strip()

        if not all([nombre, correo, password, numero, direccion]):
            self.show_message("Nombre, correo, contraseña, número y dirección son obligatorios.")
            return

        try:
            self.db_manager.update_user_profile(
                empresa=self.empresa_nombre,
                nombre=nombre,
                correo=correo,
                password=password,
                numero=numero,
                direccion=direccion,
                descripcion=descripcion,
                photo_path=self.profile_photo_path
            )
            self.show_message("Perfil actualizado correctamente.")
        except Exception as e:
            self.show_message(f"Error al actualizar el perfil: {str(e)}")

    def cancel_edit(self):
        """
        Cancela los cambios y, si lo deseas, recarga los datos originales
        o cierra la ventana, etc.
        """
        self.close()

    def create_input_with_icon(self, placeholder, icon_path):
        inp = QLineEdit()
        inp.setPlaceholderText(placeholder)
        inp.setClearButtonEnabled(True)
        inp.setStyleSheet(self.input_style())
        # Añadir un icono a la izquierda
        action = inp.addAction(QIcon(icon_path), QLineEdit.LeadingPosition)
        return inp

    def input_style(self):
        return """
            QLineEdit {
                font-size: 14px;
                padding: 6px 6px 6px 32px; /* Ajusta el padding para el icono */
                border: 2px solid #BDC3C7;
                border-radius: 5px;
                background-color: #ECF0F1;
            }
            QLineEdit:focus {
                border: 2px solid #3498DB;
                background-color: #FFFFFF;
            }
        """

    def textedit_style(self):
        return """
            QTextEdit {
                font-size: 14px;
                border: 2px solid #BDC3C7;
                border-radius: 5px;
                background-color: #ECF0F1;
            }
            QTextEdit:focus {
                border: 2px solid #3498DB;
                background-color: #FFFFFF;
            }
        """

    def button_style(self, base_color):
        darker_color = QColor(base_color).darker(110).name()
        return f"""
            QPushButton {{
                background-color: {base_color};
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {darker_color};
            }}
        """

    def show_assistant(self):
        """
        Crea y muestra la burbuja asistente específica para MiPerfilView.
        """
        try:
            if self.assistant_bubble:
                self.assistant_bubble.close()
                self.assistant_bubble = None

            self.assistant_bubble = AssistantBubbleMiPerfil(self, self.assistant_button)
            self.assistant_bubble.show()
        except Exception as e:
            # Mostrar un mensaje de error si algo falla al mostrar la burbuja
            error_msg = f"Error al mostrar la burbuja asistente: {str(e)}"
            print(error_msg)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(error_msg)
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def closeEvent(self, event):
        if self.assistant_bubble:
            self.assistant_bubble.close()
        event.accept()

    def show_message(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Información")
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #ECF0F1;
            }
            QMessageBox QLabel {
                color: #2C3E50;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 5px 20px;
                margin: 5px;
                border-radius: 4px;
            }
            QMessageBox QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        msg.exec_()
