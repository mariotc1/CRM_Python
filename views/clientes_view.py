from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout,
    QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QAction,
    QFrame, QSizePolicy, QHeaderView
)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QSize

from asistentes.burbujaAsistente_clientes import AssistantBubbleClientes
from rotatable_label import RotatableLabel


class ClientesView(QWidget):
    def __init__(self, db_manager, empresa_nombre):
        super().__init__()
        self.db_manager = db_manager
        self.empresa_nombre = empresa_nombre
        self.db_manager.connect()
        self.assistant_bubble = None
        self.init_ui()

    #  INICIALIZACIÓN DE LA INTERFAZ
    def init_ui(self):
        # Layout principal vertical sin relleno extra
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1) Encabezado superior (oscuro)
        header_frame = self.create_header()
        main_layout.addWidget(header_frame)

        # 2) Contenedor blanco para la tabla y el formulario
        content_frame = self.create_content()
        main_layout.addWidget(content_frame)

        # Cargar los clientes al iniciar
        self.load_clients()

    #  ENCABEZADO OSCURO
    def create_header(self):
        header_frame = QFrame()
        header_frame.setFixedHeight(80)
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #2C3E50; /* color oscuro */
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
        title_label = QLabel(f"Gestión de Clientes - {self.empresa_nombre}")
        title_label.setStyleSheet("color: #ECF0F1;")
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

        # Añador logo y título al layout del header
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.assistant_button)  # Añado el botón de asistente

        return header_frame

    #  CONTENEDOR PRINCIPAL PARA TABLA + FORMULARIO
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

        # 2.1) Tabla de clientes
        self.clients_table = QTableWidget(self)
        self.clients_table.setColumnCount(8)
        self.clients_table.setHorizontalHeaderLabels([
            "ID Cliente", "Nombre", "Dirección", "Teléfono",
            "Persona Contacto", "Email", "Editar", "Borrar"
        ])

        # Estilo de la tabla
        self.clients_table.setAlternatingRowColors(True)
        self.clients_table.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                alternate-background-color: #ECF0F1;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #3498DB;
                color: white;
                font-weight: bold;
                border: none;
            }
        """)
        self.clients_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.clients_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.clients_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.clients_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.clients_table.setSelectionMode(QTableWidget.SingleSelection)
        self.clients_table.cellClicked.connect(self.populate_form_from_table)

        content_layout.addWidget(self.clients_table)

        # 2.2) Formulario y Botones en Layout Horizontal
        form_and_buttons_layout = QHBoxLayout()
        form_and_buttons_layout.setSpacing(20)

        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        self.id_cliente_input = self.create_input_with_icon("ID Cliente o CIF", "icons/id_icon.png")
        self.nombre_input = self.create_input_with_icon("Nombre", "icons/name_icon.png")
        self.direccion_input = self.create_input_with_icon("Dirección", "icons/address_icon.png")
        self.telefono_input = self.create_input_with_icon("Teléfono", "icons/phone_icon.png")
        self.persona_contacto_input = self.create_input_with_icon("Persona de contacto", "icons/contact_icon.png")
        self.email_input = self.create_input_with_icon("Correo electrónico", "icons/correo-electronico.png")

        form_layout.addRow("ID Cliente / CIF:", self.id_cliente_input)
        form_layout.addRow("Nombre:", self.nombre_input)
        form_layout.addRow("Dirección:", self.direccion_input)
        form_layout.addRow("Teléfono:", self.telefono_input)
        form_layout.addRow("Persona Contacto:", self.persona_contacto_input)
        form_layout.addRow("Correo Electrónico:", self.email_input)

        form_and_buttons_layout.addLayout(form_layout, 2)  # Factor de estiramiento para ocupar más espacio

        # Botones de acción
        button_layout = QVBoxLayout()
        button_layout.setSpacing(15)

        self.save_button = self.create_styled_button("Guardar Cliente", "#2ECC71", self.save_cliente)
        self.update_button = self.create_styled_button("Actualizar Cliente", "#F1C40F", self.update_cliente)
        self.delete_button = self.create_styled_button("Borrar Cliente", "#E74C3C", self.delete_cliente)
        self.create_button = self.create_styled_button("Limpiar Formulario", "#2980B9", self.create_cliente)

        # Por defecto desactivar botones de actualizar y borrar
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)

        # Tamaño para los botones
        for button in [self.save_button, self.update_button, self.delete_button, self.create_button]:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Añadir botones al layout
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.create_button)
        button_layout.addStretch()

        form_and_buttons_layout.addLayout(button_layout, 1)

        content_layout.addLayout(form_and_buttons_layout)

        return content_frame

    #  CREAR CAMPOS CON ÍCONO
    def create_input_with_icon(self, placeholder, icon_path):
        input_field = QLineEdit(self)
        input_field.setPlaceholderText(placeholder)
        input_field.setClearButtonEnabled(True)
        input_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        input_field.setStyleSheet("""
            QLineEdit {
                padding: 8px 8px 8px 32px;
                border: 2px solid #BDC3C7;
                border-radius: 5px;
                font-size: 14px;
                background-color: #ECF0F1;
            }
            QLineEdit:focus {
                border: 2px solid #3498DB;
                background-color: #FFFFFF;
            }
        """)
        # Añadir ícono como acción a la izquierda
        icon_action = QAction(QIcon(icon_path), "", input_field)
        input_field.addAction(icon_action, QLineEdit.LeadingPosition)
        return input_field

    #  CREAR BOTONES CON ESTILO
    def create_styled_button(self, text, color, callback):
        """
        Crea un botón con un color base y un hover algo más oscuro.
        """
        button = QPushButton(text, self)
        button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 12px 24px;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
        """)
        button.clicked.connect(callback)
        return button

    def darken_color(self, color):
        """
        Hace el color ligeramente más oscuro para el hover.
        E.g. #E74C3C -> un tono algo más oscuro.
        """
        c = QColor(color)
        h, s, v, a = c.getHsv()
        v = max(0, v - 30)
        c.setHsv(h, s, v, a)
        return c.name()

    #  MANEJO DE LA TABLA Y OPERACIONES CRUD
    def load_clients(self):
        try:
            clients = self.db_manager.get_all_clients()
            self.clients_table.setRowCount(len(clients))
            for row, client in enumerate(clients):
                for col, value in enumerate(client[:6]):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.clients_table.setItem(row, col, item)

                # Botón para Editar en la columna Editar
                edit_button = QPushButton("Editar")
                edit_button.setStyleSheet("""
                    QPushButton {
                        background-color: #3498DB;
                        color: white;
                        border-radius: 5px;
                        padding: 4px 8px;
                    }
                    QPushButton:hover {
                        background-color: #2980B9;
                    }
                """)
                edit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                edit_button.clicked.connect(lambda checked, r=row: self.edit_cliente(r))
                self.clients_table.setCellWidget(row, 6, edit_button)  # Columna 6 es Editar

                # Botón para Borrar en la columna Borrar
                delete_button = QPushButton("Borrar")
                delete_button.setStyleSheet("""
                    QPushButton {
                        background-color: #E74C3C;
                        color: white;
                        border-radius: 5px;
                        padding: 4px 8px;
                    }
                    QPushButton:hover {
                        background-color: #C0392B;
                    }
                """)
                delete_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                delete_button.clicked.connect(lambda checked, r=row: self.delete_cliente_confirm(r))
                self.clients_table.setCellWidget(row, 7, delete_button)  # Columna 7 es Borrar
        except Exception as e:
            self.show_message(f"Error al cargar los clientes: {str(e)}")

    def save_cliente(self):
        client_data = self.get_client_data()
        if not all(client_data.values()):
            self.show_message("Todos los campos son obligatorios.")
            return
        try:
            # Verificar si el cliente ya existe
            if self.db_manager.get_client_by_id(client_data['id_cliente']):
                self.show_message("El cliente con este ID ya existe.")
                return

            self.db_manager.insert_cliente(*client_data.values())
            self.show_message(f"Cliente {client_data['nombre']} registrado correctamente.")
            self.load_clients()
            self.clear_form()
        except Exception as e:
            self.show_message(f"Error al guardar el cliente: {str(e)}")

    def edit_cliente(self, row):
        try:
            client_id = self.clients_table.item(row, 0).text()
            client = self.db_manager.get_client_by_id(client_id)
            if not client:
                self.show_message("No se encontró el cliente en la base de datos.")
                return
            self.populate_form(client)
            # Deshabilitar el campo ID cliente al actualizar
            self.id_cliente_input.setEnabled(False)
            self.update_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        except Exception as e:
            self.show_message(f"Error al editar el cliente: {str(e)}")

    def update_cliente(self):
        client_data = self.get_client_data()
        if not client_data['id_cliente']:
            self.show_message("El ID del cliente no puede estar vacío.")
            return
        try:
            self.db_manager.update_cliente(*client_data.values())
            self.show_message(f"Cliente {client_data['nombre']} actualizado correctamente.")
            self.load_clients()
            self.clear_form()
        except Exception as e:
            self.show_message(f"Error al actualizar el cliente: {str(e)}")

    def delete_cliente_confirm(self, row):
        try:
            client_id = self.clients_table.item(row, 0).text()
            nombre = self.clients_table.item(row, 1).text()

            reply = QMessageBox.question(
                self, 'Confirmar borrado',
                f"¿Está seguro de que desea borrar al cliente '{nombre}'?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.db_manager.delete_cliente(client_id)
                self.show_message(f"Cliente '{nombre}' borrado correctamente.")
                self.load_clients()
                self.clear_form()
        except Exception as e:
            self.show_message(f"Error al borrar el cliente: {str(e)}")

    def delete_cliente(self):
        """
        Elimina el cliente actualmente cargado en el formulario principal.
        """
        try:
            client_id = self.id_cliente_input.text()
            nombre = self.nombre_input.text()

            if not client_id:
                self.show_message("No hay ningún cliente seleccionado para borrar.")
                return

            reply = QMessageBox.question(
                self, 'Confirmar borrado',
                f"¿Está seguro de que desea borrar al cliente '{nombre}'?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.db_manager.delete_cliente(client_id)
                self.show_message(f"Cliente '{nombre}' borrado correctamente.")
                self.load_clients()
                self.clear_form()
        except Exception as e:
            self.show_message(f"Error al borrar el cliente: {str(e)}")

    def create_cliente(self):
        """
        Prepara el formulario para crear un nuevo cliente.
        """
        self.clear_form()
        self.id_cliente_input.setEnabled(True)
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.show_message("Formulario limpio para crear un nuevo cliente.")

    #  FORM HELPERS
    def get_client_data(self):
        """
        Retorna un dict con los campos (en orden):
        id_cliente, nombre, direccion, telefono, persona_contacto, email
        """
        return {
            'id_cliente': self.id_cliente_input.text(),
            'nombre': self.nombre_input.text(),
            'direccion': self.direccion_input.text(),
            'telefono': self.telefono_input.text(),
            'persona_contacto': self.persona_contacto_input.text(),
            'email': self.email_input.text()
        }

    def populate_form(self, client):
        """
        Rellena el formulario con los datos del cliente seleccionado.
        client es una tupla devuelta por get_client_by_id, por ejemplo:
        (id_cliente, nombre, direccion, telefono, persona_contacto, email)
        """
        self.id_cliente_input.setText(client[0])
        self.nombre_input.setText(client[1])
        self.direccion_input.setText(client[2])
        self.telefono_input.setText(client[3])
        self.persona_contacto_input.setText(client[4])
        self.email_input.setText(client[5])

    def populate_form_from_table(self, row, column):
        """
        Rellena el formulario al hacer clic en una fila de la tabla.
        """
        try:
            client_id = self.clients_table.item(row, 0).text()
            client = self.db_manager.get_client_by_id(client_id)
            if client:
                self.populate_form(client)
                # Deshabilitar el campo ID cliente al actualizar
                self.id_cliente_input.setEnabled(False)
                self.update_button.setEnabled(True)
                self.delete_button.setEnabled(True)
        except Exception as e:
            self.show_message(f"Error al seleccionar el cliente: {str(e)}")

    def clear_form(self):
        """
        Limpia el formulario y restablece el estado de los botones.
        """
        for inp in (
            self.id_cliente_input, self.nombre_input, self.direccion_input,
            self.telefono_input, self.persona_contacto_input, self.email_input
        ):
            inp.clear()

        self.id_cliente_input.setEnabled(True)
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    #  MENSAJES
    def show_message(self, message, title="Información"):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle(title)
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
                color: #fff;
                padding: 5px 20px;
                margin: 5px;
                border-radius: 4px;
            }
            QMessageBox QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    #  MÉTODO PARA MOSTRAR LA BURBUJA ASISTENTE
    def show_assistant(self):
        """
        Crea y muestra la burbuja asistente específica para ClientesView.
        """
        try:
            if self.assistant_bubble:
                self.assistant_bubble.close()
                self.assistant_bubble = None

            self.assistant_bubble = AssistantBubbleClientes(self, self.assistant_button)
            self.assistant_bubble.show()
        except Exception as e:
            # Mostrar un mensaje de error si algo falla al mostrar la burbuja
            error_msg = f"Error al mostrar la burbuja asistente: {str(e)}"
            print(error_msg)  # También puedes usar un QMessageBox para notificar al usuario
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(error_msg)
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    #  CERRAR BURBUJA ASISTENTE AL CERRAR LA VISTA
    def closeEvent(self, event):
        if self.assistant_bubble:
            self.assistant_bubble.close()
        event.accept()
