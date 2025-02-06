from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QFormLayout, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox,
    QDateEdit, QFrame, QSizePolicy, QHeaderView, QAction
)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QDate, QSize, pyqtSignal

from asistentes.burbujaAsistente_presupuestos import AssistantBubblePresupuestos


class PresupuestosView(QWidget):
    switch_to_inventario = pyqtSignal(int)

    def __init__(self, db_manager, empresa_nombre):
        super().__init__()
        self.db_manager = db_manager
        self.empresa_nombre = empresa_nombre
        self.db_manager.connect()
        self.assistant_bubble = None
        self.init_ui()
        self.load_presupuestos()
        self.load_clientes()

    #  INICIALIZACIÓN DE LA INTERFAZ
    def init_ui(self):
        # Layout principal vertical sin relleno extra
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1) Encabezado superior (oscuro)
        header_frame = self.create_header()
        main_layout.addWidget(header_frame)

        # 2) Contenedor blanco para tabla y formulario
        content_frame = self.create_content()
        main_layout.addWidget(content_frame)

    #  ENCABEZADO OSCURO
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
        title_label = QLabel(f"Gestión de Presupuestos - {self.empresa_nombre}")
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

        # Añado logo y título al layout del header
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.assistant_button)  # botón de asistente

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

        # 2.1) Tabla de presupuestos
        self.presupuestos_table = QTableWidget(self)
        self.presupuestos_table.setColumnCount(8)  # Añadimos dos columnas extra para "Editar" y "Borrar"
        self.presupuestos_table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Cliente", "Fecha Creación",
            "Fecha Expiración", "Subtotal", "Total", "Acciones"
        ])

        # Estilo de la tabla
        self.presupuestos_table.setAlternatingRowColors(True)
        self.presupuestos_table.setStyleSheet("""
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
        self.presupuestos_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.presupuestos_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.presupuestos_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.presupuestos_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.presupuestos_table.setSelectionMode(QTableWidget.SingleSelection)
        self.presupuestos_table.cellClicked.connect(self.populate_form_from_table)

        content_layout.addWidget(self.presupuestos_table)

        # 2.2) Formulario y Botones en Layout Horizontal
        form_and_buttons_layout = QHBoxLayout()
        form_and_buttons_layout.setSpacing(20)

        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        self.id_presupuesto_input = self.create_input_with_icon("ID Presupuesto", "icons/id_icon.png")
        self.nombre_input = self.create_input_with_icon("Nombre Presupuesto", "icons/name_icon.png")

        self.cliente_combo = self.create_combo_box("Seleccionar Cliente")
        self.load_clientes_into_combo()

        self.fecha_creacion_input = self.create_date_edit()
        self.fecha_creacion_input.setDisplayFormat("yyyy-MM-dd")

        self.fecha_expiracion_input = self.create_date_edit()
        self.fecha_expiracion_input.setDate(QDate.currentDate().addDays(30))
        self.fecha_expiracion_input.setDisplayFormat("yyyy-MM-dd")

        self.subtotal_input = self.create_input_with_icon("Subtotal", "icons/money_icon.png")
        self.total_input = self.create_input_with_icon("Total", "icons/money_icon.png")

        form_layout.addRow("ID Presupuesto:", self.id_presupuesto_input)
        form_layout.addRow("Nombre:", self.nombre_input)
        form_layout.addRow("Cliente:", self.cliente_combo)
        form_layout.addRow("Fecha Creación:", self.fecha_creacion_input)
        form_layout.addRow("Fecha Expiración:", self.fecha_expiracion_input)
        form_layout.addRow("Subtotal:", self.subtotal_input)
        form_layout.addRow("Total:", self.total_input)

        form_and_buttons_layout.addLayout(form_layout, 2)

        # Botones de acción
        button_layout = QVBoxLayout()
        button_layout.setSpacing(15)

        self.save_button = self.create_styled_button("Guardar Presupuesto", "#2ECC71", self.save_presupuesto)
        self.update_button = self.create_styled_button("Actualizar Presupuesto", "#F39C12", self.update_presupuesto)
        self.delete_button = self.create_styled_button("Borrar Presupuesto", "#E74C3C", self.delete_presupuesto)
        self.view_products_button = self.create_styled_button("Ver Inventario", "#9B59B6", self.view_products)

        # Por defecto, desactivar botones de actualizar y borrar
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)

        # Establecer política de tamaño para los botones
        for button in [self.save_button, self.update_button, self.delete_button, self.view_products_button]:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Añadir botones al layout
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.view_products_button)  # Botón modificado
        button_layout.addStretch()  # Empujar los botones hacia arriba

        form_and_buttons_layout.addLayout(button_layout, 1)

        # Añadir el layout horizontal al content_layout
        content_layout.addLayout(form_and_buttons_layout)

        # 2.3) Botón "Crear Presupuesto" debajo del formulario (centro)
        crear_presupuesto_layout = QHBoxLayout()
        crear_presupuesto_layout.addStretch()
        self.create_button = self.create_styled_button("LIMPIAR FORMULARIO", "#2980B9", self.create_presupuesto)
        crear_presupuesto_layout.addWidget(self.create_button)
        crear_presupuesto_layout.addStretch()

        content_layout.addLayout(crear_presupuesto_layout)

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

    #  CREAR COMBOBOX CON ESTILO
    def create_combo_box(self, placeholder=None):
        combo = QComboBox(self)
        combo.setStyleSheet(self.combo_style())
        if placeholder:
            combo.addItem(placeholder)
        combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return combo

    def load_clientes_into_combo(self):
        try:
            clientes = self.db_manager.get_all_clients()
            self.cliente_combo.clear()
            self.cliente_combo.addItem("Seleccionar Cliente")
            for cliente in clientes:
                combo_text = f"{cliente[0]} - {cliente[1]}"
                self.cliente_combo.addItem(combo_text)
        except Exception as e:
            self.show_message(f"Error al cargar los clientes: {str(e)}")

    def create_date_edit(self):
        date_edit = QDateEdit(self)
        date_edit.setDate(QDate.currentDate())
        date_edit.setStyleSheet(self.dateedit_style())
        date_edit.setCalendarPopup(True)
        date_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return date_edit

    def combo_style(self):
        return """
            QComboBox {
                padding: 8px;
                border: 2px solid #BDC3C7;
                border-radius: 5px;
                background-color: #ECF0F1;
                font-size: 14px;
            }
            QComboBox:focus {
                border: 2px solid #3498DB;
                background-color: #FFFFFF;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left-width: 1px;
                border-left-color: #BDC3C7;
                border-left-style: solid;
            }
            QComboBox QAbstractItemView {
                background-color: #ECF0F1;
                selection-background-color: #3498DB;
                selection-color: white;
            }
        """

    def dateedit_style(self):
        return """
            QDateEdit {
                padding: 8px;
                border: 2px solid #BDC3C7;
                border-radius: 5px;
                background-color: #ECF0F1;
                font-size: 14px;
            }
            QDateEdit:focus {
                border: 2px solid #3498DB;
                background-color: #FFFFFF;
            }
        """

    def create_styled_button(self, text, color, callback):
        button = QPushButton(text, self)
        button.setFont(QFont("Segoe UI", 10, QFont.Bold))
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
        """
        c = QColor(color)
        h, s, v, a = c.getHsv()
        v = max(0, v - 30)
        c.setHsv(h, s, v, a)
        return c.name()

    #  MANEJO DE LA TABLA Y OPERACIONES CRUD
    def load_presupuestos(self):
        try:
            presupuestos = self.db_manager.get_all_presupuestos()
            self.presupuestos_table.setRowCount(len(presupuestos))
            for row, presupuesto in enumerate(presupuestos):
                # presupuesto = (id, nombre, cliente, fecha_creacion, fecha_expiracion, subtotal, total)
                for col, value in enumerate(presupuesto[:7]):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.presupuestos_table.setItem(row, col, item)

                # Botón para Editar
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
                edit_button.clicked.connect(lambda checked, r=row: self.edit_presupuesto(r))
                self.presupuestos_table.setCellWidget(row, 7, edit_button)  # Columna 7 es "Acciones"
        except Exception as e:
            self.show_message(f"Error al cargar los presupuestos: {str(e)}")

    def save_presupuesto(self):
        presupuesto_data = self.get_presupuesto_data()
        if not all([
            presupuesto_data['id_presupuesto'], presupuesto_data['nombre'],
            presupuesto_data['cliente'], presupuesto_data['fecha_creacion'],
            presupuesto_data['fecha_expiracion'], presupuesto_data['subtotal'],
            presupuesto_data['total']
        ]):
            self.show_message("Todos los campos son obligatorios.")
            return

        # Validar que 'subtotal' y 'total' sean números
        try:
            subtotal = float(presupuesto_data['subtotal'])
            total = float(presupuesto_data['total'])
            if subtotal < 0 or total < 0:
                raise ValueError("Los valores de subtotal y total no pueden ser negativos.")
        except ValueError as ve:
            self.show_message(f"Valores numéricos inválidos: {ve}")
            return

        try:
            # Verificar si el presupuesto ya existe
            if self.db_manager.get_presupuesto_by_id(presupuesto_data['id_presupuesto']):
                self.show_message("El presupuesto con este ID ya existe.")
                return

            self.db_manager.insert_presupuesto(
                presupuesto_data['id_presupuesto'],
                presupuesto_data['nombre'],
                presupuesto_data['cliente'],
                presupuesto_data['fecha_creacion'],
                presupuesto_data['fecha_expiracion'],
                subtotal,
                total
            )
            self.show_message(f"Presupuesto '{presupuesto_data['nombre']}' guardado correctamente.")
            self.load_presupuestos()
            self.clear_form()
        except Exception as e:
            self.show_message(f"Error al guardar el presupuesto: {str(e)}")

    def edit_presupuesto(self, row):
        try:
            id_presupuesto = self.presupuestos_table.item(row, 0).text()
            presupuesto = self.db_manager.get_presupuesto_by_id(id_presupuesto)
            if not presupuesto:
                self.show_message("No se encontró el presupuesto en la base de datos.")
                return
            self.populate_form(presupuesto)
            # Deshabilitar el campo ID presupuesto al actualizar
            self.id_presupuesto_input.setEnabled(False)
            self.update_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        except Exception as e:
            self.show_message(f"Error al editar el presupuesto: {str(e)}")

    def update_presupuesto(self):
        presupuesto_data = self.get_presupuesto_data()
        if not presupuesto_data['id_presupuesto']:
            self.show_message("El ID del presupuesto no puede estar vacío.")
            return

        # Validar que 'subtotal' y 'total' sean números
        try:
            subtotal = float(presupuesto_data['subtotal'])
            total = float(presupuesto_data['total'])
            if subtotal < 0 or total < 0:
                raise ValueError("Los valores de subtotal y total no pueden ser negativos.")
        except ValueError as ve:
            self.show_message(f"Valores numéricos inválidos: {ve}")
            return

        try:
            self.db_manager.update_presupuesto(
                presupuesto_data['id_presupuesto'],
                presupuesto_data['nombre'],
                presupuesto_data['cliente'],
                presupuesto_data['fecha_creacion'],
                presupuesto_data['fecha_expiracion'],
                subtotal,
                total
            )
            self.show_message(f"Presupuesto '{presupuesto_data['nombre']}' actualizado correctamente.")
            self.load_presupuestos()
            self.clear_form()
        except Exception as e:
            self.show_message(f"Error al actualizar el presupuesto: {str(e)}")

    def delete_presupuesto_confirm(self, row):
        try:
            id_presupuesto = self.presupuestos_table.item(row, 0).text()
            nombre = self.presupuestos_table.item(row, 1).text()

            reply = QMessageBox.question(
                self, 'Confirmar borrado',
                f"¿Está seguro de que desea borrar el presupuesto '{nombre}'?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.db_manager.delete_presupuesto(id_presupuesto)
                self.show_message(f"Presupuesto '{nombre}' borrado correctamente.")
                self.load_presupuestos()
                self.clear_form()
        except Exception as e:
            self.show_message(f"Error al borrar el presupuesto: {str(e)}")

    def delete_presupuesto(self):
        """
        Elimina el presupuesto actualmente cargado en el formulario principal.
        """
        try:
            id_presupuesto = self.id_presupuesto_input.text()
            nombre = self.nombre_input.text()

            if not id_presupuesto:
                self.show_message("No hay ningún presupuesto seleccionado para borrar.")
                return

            reply = QMessageBox.question(
                self, 'Confirmar borrado',
                f"¿Está seguro de que desea borrar el presupuesto '{nombre}'?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.db_manager.delete_presupuesto(id_presupuesto)
                self.show_message(f"Presupuesto '{nombre}' borrado correctamente.")
                self.load_presupuestos()
                self.clear_form()
        except Exception as e:
            self.show_message(f"Error al borrar el presupuesto: {str(e)}")

    def create_presupuesto(self):
        """
        Prepara el formulario para crear un nuevo presupuesto.
        """
        self.clear_form()
        self.id_presupuesto_input.setEnabled(True)
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.show_message("Formulario limpio para crear un nuevo presupuesto.")

    def load_clientes(self):
        try:
            clientes = self.db_manager.get_all_clients()
            self.cliente_combo.clear()
            self.cliente_combo.addItem("Seleccionar Cliente")
            for cliente in clientes:
                combo_text = f"{cliente[0]} - {cliente[1]}"
                self.cliente_combo.addItem(combo_text)
        except Exception as e:
            self.show_message(f"Error al cargar los clientes: {str(e)}")

    def get_presupuesto_data(self):
        """
        Retorna un dict con los campos del presupuesto.
        """
        return {
            'id_presupuesto': self.id_presupuesto_input.text(),
            'nombre': self.nombre_input.text(),
            'cliente': self.cliente_combo.currentText().split(" - ")[0] if " - " in self.cliente_combo.currentText() else self.cliente_combo.currentText(),
            'fecha_creacion': self.fecha_creacion_input.date().toString("yyyy-MM-dd"),
            'fecha_expiracion': self.fecha_expiracion_input.date().toString("yyyy-MM-dd"),
            'subtotal': self.subtotal_input.text(),
            'total': self.total_input.text()
        }

    def populate_form(self, presupuesto):
        """
        Rellena el formulario con los datos del presupuesto seleccionado.
        """
        self.id_presupuesto_input.setText(presupuesto[0])
        self.nombre_input.setText(presupuesto[1])
        self.cliente_combo.setCurrentText(presupuesto[2])
        self.fecha_creacion_input.setDate(QDate.fromString(presupuesto[3], "yyyy-MM-dd"))
        self.fecha_expiracion_input.setDate(QDate.fromString(presupuesto[4], "yyyy-MM-dd"))
        self.subtotal_input.setText(str(presupuesto[5]))
        self.total_input.setText(str(presupuesto[6]))

    def populate_form_from_table(self, row, column):
        """
        Rellena el formulario al hacer clic en una fila de la tabla.
        """
        try:
            id_presupuesto = self.presupuestos_table.item(row, 0).text()
            presupuesto = self.db_manager.get_presupuesto_by_id(id_presupuesto)
            if presupuesto:
                self.populate_form(presupuesto)
                self.id_presupuesto_input.setEnabled(False)
                self.update_button.setEnabled(True)
                self.delete_button.setEnabled(True)
        except Exception as e:
            self.show_message(f"Error al seleccionar el presupuesto: {str(e)}")

    def clear_form(self):
        """
        Limpia el formulario y restablece el estado de los botones.
        """
        self.id_presupuesto_input.clear()
        self.nombre_input.clear()
        self.cliente_combo.setCurrentIndex(0)
        self.fecha_creacion_input.setDate(QDate.currentDate())
        self.fecha_expiracion_input.setDate(QDate.currentDate().addDays(30))
        self.subtotal_input.clear()
        self.total_input.clear()

        self.id_presupuesto_input.setEnabled(True)
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)

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

    def show_assistant(self):
        """
        Crea y muestra la burbuja asistente específica para PresupuestosView.
        """
        try:
            if self.assistant_bubble:
                self.assistant_bubble.close()
                self.assistant_bubble = None

            self.assistant_bubble = AssistantBubblePresupuestos(self, self.assistant_button)
            self.assistant_bubble.show()
        except Exception as e:
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

    def view_products(self):
        """
        Navega directamente a la vista de Inventario.
        """
        self.switch_to_inventario.emit(3)
