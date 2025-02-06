from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QFormLayout, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox, 
    QDateEdit, QFrame, QSizePolicy, QAction, QHeaderView
)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QDate, QSize

from asistentes.burbujaAsistente_oportunidades import AssistantBubbleOportunidades

class OportunidadesView(QWidget):
    def __init__(self, db_manager, empresa_nombre):
        super().__init__()
        self.db_manager = db_manager
        self.empresa_nombre = empresa_nombre
        self.db_manager.connect()
        self.assistant_bubble = None
        self.init_ui()

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

        # Cargar las oportunidades al iniciar
        self.load_oportunidades()

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
        title_label = QLabel(f"Gestión de Oportunidades - {self.empresa_nombre}")
        title_label.setStyleSheet("color: #ECF0F1;")  # texto claro
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

        # 2.1) Tabla de oportunidades
        self.oportunidades_table = QTableWidget(self)
        self.oportunidades_table.setColumnCount(9)
        self.oportunidades_table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Cliente", "Fecha", 
            "Presupuesto", "Ingreso Esperado", "Estado", "Editar", "Borrar"
        ])

        # Estilo de la tabla
        self.oportunidades_table.setAlternatingRowColors(True)
        self.oportunidades_table.setStyleSheet("""
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
        self.oportunidades_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.oportunidades_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.oportunidades_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Hacer tabla solo lectura
        self.oportunidades_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.oportunidades_table.setSelectionMode(QTableWidget.SingleSelection)
        self.oportunidades_table.cellClicked.connect(self.populate_form_from_table)

        content_layout.addWidget(self.oportunidades_table)

        # 2.2) Formulario y Botones en Layout Horizontal
        form_and_buttons_layout = QHBoxLayout()
        form_and_buttons_layout.setSpacing(20)

        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        self.id_oportunidad_input = self.create_input_with_icon("ID Oportunidad", "icons/id_icon.png")
        self.nombre_oportunidad_input = self.create_input_with_icon("Nombre Oportunidad", "icons/name_icon.png")

        self.cliente_combo = self.create_combo_box("Seleccionar Cliente")
        self.load_clientes_into_combo()

        self.fecha_input = self.create_date_edit()

        self.presupuesto_combo = self.create_combo_box("Seleccionar Presupuesto")
        self.load_presupuestos_into_combo()

        self.ingreso_esperado_input = self.create_input_with_icon("Ingreso Esperado", "icons/money_icon.png")

        self.estado_combo = self.create_combo_box()
        self.estado_combo.addItems(["Seleccionar Estado", "En proceso", "Ganada", "Perdida"])

        form_layout.addRow("ID Oportunidad:", self.id_oportunidad_input)
        form_layout.addRow("Nombre Oportunidad:", self.nombre_oportunidad_input)
        form_layout.addRow("Cliente:", self.cliente_combo)
        form_layout.addRow("Fecha:", self.fecha_input)
        form_layout.addRow("Presupuesto:", self.presupuesto_combo)
        form_layout.addRow("Ingreso Esperado:", self.ingreso_esperado_input)
        form_layout.addRow("Estado:", self.estado_combo)

        form_and_buttons_layout.addLayout(form_layout, 2)

        # Botones de acción
        button_layout = QVBoxLayout()
        button_layout.setSpacing(15)

        self.save_button = self.create_styled_button("Guardar Oportunidad", "#2ECC71", self.save_oportunidad)
        self.update_button = self.create_styled_button("Actualizar Oportunidad", "#F39C12", self.update_oportunidad)
        self.delete_button = self.create_styled_button("Borrar Oportunidad", "#E74C3C", self.delete_oportunidad)
        self.create_button = self.create_styled_button("Limpiar formulario", "#2980B9", self.create_oportunidad)

        # Por defecto, desactivar botones de actualizar y borrar
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)

        # Establecer política de tamaño para los botones
        for button in [self.save_button, self.update_button, self.delete_button, self.create_button]:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.create_button)  # Nuevo botón "Crear Oportunidad"
        button_layout.addStretch()  # Empujar los botones hacia arriba

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
            for cliente in clientes:
                combo_text = f"{cliente[0]} - {cliente[1]}"
                self.cliente_combo.addItem(combo_text)
        except Exception as e:
            self.show_message(f"Error al cargar los clientes: {str(e)}")

    def load_presupuestos_into_combo(self):
        try:
            presupuestos = self.db_manager.get_all_presupuestos()
            for presupuesto in presupuestos:
                combo_text = f"{presupuesto[0]} - {presupuesto[1]}"  # ID_PRESUPUESTO - NOMBRE
                self.presupuesto_combo.addItem(combo_text)
        except Exception as e:
            self.show_message(f"Error al cargar los presupuestos: {str(e)}")

    #  CREAR QDATEEDIT CON ESTILO
    def create_date_edit(self):
        date_edit = QDateEdit(self)
        date_edit.setDate(QDate.currentDate())
        date_edit.setDisplayFormat("yyyy-MM-dd")
        date_edit.setStyleSheet(self.dateedit_style())
        date_edit.setCalendarPopup(True)
        date_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return date_edit

    #  ESTILOS PARA QCOMBOBOX Y QDATEEDIT
    def combo_style(self):
        return """
            QComboBox {
                padding: 8px 8px 8px 8px;
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

    #  BOTONES CON ESTILO
    def create_styled_button(self, text, color, callback):
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
        """
        c = QColor(color)
        h, s, v, a = c.getHsv()
        v = max(0, v - 30)  # Ajusta la cantidad de "oscuridad"
        c.setHsv(h, s, v, a)
        return c.name()

    #  MANEJO DE LA TABLA Y OPERACIONES CRUD
    def load_oportunidades(self):
        try:
            oportunidades = self.db_manager.get_all_oportunidades()
            self.oportunidades_table.setRowCount(len(oportunidades))
            for row, oportunidad in enumerate(oportunidades):
                for col, value in enumerate(oportunidad[:7]):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.oportunidades_table.setItem(row, col, item)

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
                edit_button.clicked.connect(lambda checked, r=row: self.edit_oportunidad(r))

                # Botón para Borrar
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
                delete_button.clicked.connect(lambda checked, r=row: self.delete_oportunidad_confirm(r))

                # Asignar botones a sus respectivas columnas
                self.oportunidades_table.setCellWidget(row, 7, edit_button)  # Columna "Editar"
                self.oportunidades_table.setCellWidget(row, 8, delete_button)  # Columna "Borrar"
        except Exception as e:
            self.show_message(f"Error al cargar las oportunidades: {str(e)}")

    def save_oportunidad(self):
        oportunidad_data = self.get_oportunidad_data()
        if not all([
            oportunidad_data['id_oportunidad'], oportunidad_data['nombre_oportunidad'],
            oportunidad_data['cliente'], oportunidad_data['presupuesto'],
            oportunidad_data['ingreso_esperado'], oportunidad_data['estado']
        ]):
            self.show_message("Todos los campos son obligatorios.")
            return

        try:
            # Verificar si la oportunidad ya existe
            if self.db_manager.get_oportunidad_by_id(oportunidad_data['id_oportunidad']):
                self.show_message("La oportunidad con este ID ya existe.")
                return

            self.db_manager.insert_oportunidad(
                oportunidad_data['id_oportunidad'],
                oportunidad_data['nombre_oportunidad'],
                oportunidad_data['cliente'],
                oportunidad_data['fecha'],
                oportunidad_data['presupuesto'],
                float(oportunidad_data['ingreso_esperado']),
                oportunidad_data['estado']
            )
            self.show_message(f"Oportunidad '{oportunidad_data['nombre_oportunidad']}' registrada correctamente.")
            self.load_oportunidades()
            self.clear_form()
        except Exception as e:
            self.show_message(f"Error al guardar la oportunidad: {str(e)}")

    def edit_oportunidad(self, row):
        try:
            oportunidad_id = self.oportunidades_table.item(row, 0).text()
            oportunidad = self.db_manager.get_oportunidad_by_id(oportunidad_id)
            if not oportunidad:
                self.show_message("No se encontró la oportunidad en la base de datos.")
                return
            self.populate_form(oportunidad)
            # Deshabilitar el campo ID oportunidad al actualizar
            self.id_oportunidad_input.setEnabled(False)
            self.update_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        except Exception as e:
            self.show_message(f"Error al editar la oportunidad: {str(e)}")

    def update_oportunidad(self):
        oportunidad_data = self.get_oportunidad_data()
        if not oportunidad_data['id_oportunidad']:
            self.show_message("El ID de la oportunidad no puede estar vacío.")
            return

        try:
            self.db_manager.update_oportunidad(
                oportunidad_data['id_oportunidad'],
                oportunidad_data['nombre_oportunidad'],
                oportunidad_data['cliente'],
                oportunidad_data['fecha'],
                oportunidad_data['presupuesto'],
                float(oportunidad_data['ingreso_esperado']),
                oportunidad_data['estado']
            )
            self.show_message(f"Oportunidad '{oportunidad_data['nombre_oportunidad']}' actualizada correctamente.")
            self.load_oportunidades()
            self.clear_form()
        except Exception as e:
            self.show_message(f"Error al actualizar la oportunidad: {str(e)}")

    def delete_oportunidad_confirm(self, row):
        try:
            oportunidad_id = self.oportunidades_table.item(row, 0).text()
            nombre_oportunidad = self.oportunidades_table.item(row, 1).text()

            reply = QMessageBox.question(
                self, 'Confirmar borrado', 
                f"¿Está seguro de que desea borrar la oportunidad '{nombre_oportunidad}'?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.db_manager.delete_oportunidad(oportunidad_id)
                self.show_message(f"Oportunidad '{nombre_oportunidad}' borrada correctamente.")
                self.load_oportunidades()
                self.clear_form()
        except Exception as e:
            self.show_message(f"Error al borrar la oportunidad: {str(e)}")

    def delete_oportunidad(self):
        """
        Elimina la oportunidad actualmente cargada en el formulario principal.
        """
        try:
            id_oportunidad = self.id_oportunidad_input.text()
            nombre_oportunidad = self.nombre_oportunidad_input.text()

            if not id_oportunidad:
                self.show_message("No hay ninguna oportunidad seleccionada para borrar.")
                return

            reply = QMessageBox.question(
                self, 'Confirmar borrado', 
                f"¿Está seguro de que desea borrar la oportunidad '{nombre_oportunidad}'?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.db_manager.delete_oportunidad(id_oportunidad)
                self.show_message(f"Oportunidad '{nombre_oportunidad}' borrada correctamente.")
                self.load_oportunidades()
                self.clear_form()
        except Exception as e:
            self.show_message(f"Error al borrar la oportunidad: {str(e)}")

    def create_oportunidad(self):
        """
        Función para crear una nueva oportunidad directamente desde la tabla.
        """
        self.clear_form()
        self.id_oportunidad_input.setEnabled(True)
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.show_message("Formulario limpio para crear una nueva oportunidad.")

    def get_oportunidad_data(self):
        """
        Retorna un dict con los campos de la oportunidad.
        """
        return {
            'id_oportunidad': self.id_oportunidad_input.text(),
            'nombre_oportunidad': self.nombre_oportunidad_input.text(),
            'cliente': self.cliente_combo.currentText().split(" - ")[0] if " - " in self.cliente_combo.currentText() else self.cliente_combo.currentText(),
            'fecha': self.fecha_input.date().toString("yyyy-MM-dd"),
            'presupuesto': self.presupuesto_combo.currentText().split(" - ")[0] if " - " in self.presupuesto_combo.currentText() else self.presupuesto_combo.currentText(),
            'ingreso_esperado': self.ingreso_esperado_input.text(),
            'estado': self.estado_combo.currentText()
        }

    def populate_form(self, oportunidad):
        """
        Rellena el formulario con los datos de la oportunidad seleccionada.
        """
        self.id_oportunidad_input.setText(oportunidad[0])
        self.nombre_oportunidad_input.setText(oportunidad[1])
        
        # Seleccionar el cliente en el combo
        cliente_id = oportunidad[2]
        cliente_name = self.db_manager.get_client_name_by_id(cliente_id)
        cliente_text = f"{cliente_id} - {cliente_name}"
        index = self.cliente_combo.findText(cliente_text)
        if index != -1:
            self.cliente_combo.setCurrentIndex(index)
        else:
            self.cliente_combo.setCurrentIndex(0)

        # Fecha
        fecha = QDate.fromString(oportunidad[3], "yyyy-MM-dd")
        self.fecha_input.setDate(fecha)

        # Presupuesto
        presupuesto_id = oportunidad[4]
        presupuesto_name = self.get_presupuesto_name_by_id(presupuesto_id)
        presupuesto_text = f"{presupuesto_id} - {presupuesto_name}"
        index = self.presupuesto_combo.findText(presupuesto_text)
        if index != -1:
            self.presupuesto_combo.setCurrentIndex(index)
        else:
            self.presupuesto_combo.setCurrentIndex(0)

        # Ingreso Esperado
        self.ingreso_esperado_input.setText(str(oportunidad[5]))

        # Estado
        estado = oportunidad[6]
        index = self.estado_combo.findText(estado)
        if index != -1:
            self.estado_combo.setCurrentIndex(index)
        else:
            self.estado_combo.setCurrentIndex(0)

    def populate_form_from_table(self, row, column):
        """
        Rellena el formulario al hacer clic en una fila de la tabla.
        """
        try:
            oportunidad_id = self.oportunidades_table.item(row, 0).text()
            oportunidad = self.db_manager.get_oportunidad_by_id(oportunidad_id)
            if oportunidad:
                self.populate_form(oportunidad)
                # Deshabilitar el campo ID oportunidad al actualizar
                self.id_oportunidad_input.setEnabled(False)
                self.update_button.setEnabled(True)
                self.delete_button.setEnabled(True)
        except Exception as e:
            self.show_message(f"Error al seleccionar la oportunidad: {str(e)}")

    def get_presupuesto_name_by_id(self, presupuesto_id):
        """
        Método auxiliar para obtener el nombre del presupuesto dado su ID.
        """
        try:
            presupuestos = self.db_manager.get_all_presupuestos()
            for presupuesto in presupuestos:
                if presupuesto[0] == presupuesto_id:
                    return presupuesto[1]
            return "Desconocido"
        except Exception as e:
            self.show_message(f"Error al obtener el nombre del presupuesto: {str(e)}")
            return "Desconocido"

    def clear_form(self):
        """
        Limpia el formulario y restablece el estado de los botones.
        """
        self.id_oportunidad_input.clear()
        self.nombre_oportunidad_input.clear()
        self.cliente_combo.setCurrentIndex(0)
        self.fecha_input.setDate(QDate.currentDate())
        self.presupuesto_combo.setCurrentIndex(0)
        self.ingreso_esperado_input.clear()
        self.estado_combo.setCurrentIndex(0)

        self.id_oportunidad_input.setEnabled(True)
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    #  MENSAJE EMERGENTE
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
        Crea y muestra la burbuja asistente específica para OportunidadesView.
        """
        try:
            if self.assistant_bubble:
                self.assistant_bubble.close()
                self.assistant_bubble = None

            self.assistant_bubble = AssistantBubbleOportunidades(self, self.assistant_button)
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

    #  CERRAR BURBUJA ASISTENTE AL CERRAR LA VISTA
    def closeEvent(self, event):
        if self.assistant_bubble:
            self.assistant_bubble.close()
        event.accept()
