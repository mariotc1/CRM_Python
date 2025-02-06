import uuid
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QFormLayout, QLineEdit, QTextEdit, QComboBox, QDateEdit,
    QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont, QColor, QIcon
from PyQt5.QtCore import Qt, QDate, QSize

from asistentes.burbujaAsistente_tareas import AssistantBubbleTareas


class TareasView(QWidget):
    def __init__(self, db_manager, empresa_nombre, main_window):
        super().__init__()
        self.db_manager = db_manager
        self.empresa_nombre = empresa_nombre
        self.main_window = main_window
        self.assistant_bubble = None
        self.init_ui()

    #  Construcción de la Interfaz
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1) Encabezado oscuro
        header_frame = self.create_header()
        main_layout.addWidget(header_frame)

        # 2) Contenedor blanco
        content_frame = self.create_content()
        main_layout.addWidget(content_frame)

        # Cargamos las tareas al iniciar
        self.load_tareas()

    def create_header(self):
        header_frame = QFrame()
        header_frame.setFixedHeight(80)
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #2C3E50;
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
        title_label = QLabel("Gestión de Tareas")
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

        # 2.1) Tabla de Tareas
        self.tareas_table = QTableWidget()
        self.tareas_table.setColumnCount(8)
        self.tareas_table.setHorizontalHeaderLabels([
            "ID", "Título", "Descripción", "Creación",
            "Vencimiento", "Asignado a", "Prioridad", "Estado"
        ])
        self.tareas_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tareas_table.setAlternatingRowColors(True)
        self.tareas_table.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                alternate-background-color: #ECF0F1;
            }
            QHeaderView::section {
                background-color: #3498DB;
                color: white;
                font-weight: bold;
                border: none;
            }
        """)
        self.tareas_table.itemSelectionChanged.connect(self.on_table_selection_changed)
        content_layout.addWidget(self.tareas_table)

        # 2.2) Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # Utilizamos helpers para crear los campos con íconos
        self.id_tarea_input = self.create_line_edit_with_icon(
            "ID de la Tarea (autogenerado)", "icons/id.png"
        )
        self.id_tarea_input.setReadOnly(True)

        self.titulo_input = self.create_line_edit_with_icon(
            "Título breve de la tarea", "icons/id_icon.png"
        )

        # Para el campo de descripción se crea un contenedor que incluye el ícono
        desc_container, self.descripcion_input = self.create_text_edit_with_icon(
            "Descripción más detallada", "icons/descripcion.png"
        )

        self.fecha_creacion_input = self.create_date_edit_with_icon(
            "yyyy-MM-dd", "icons/evento.png"
        )
        self.fecha_creacion_input.setDate(QDate.currentDate())

        self.fecha_vencimiento_input = self.create_date_edit_with_icon(
            "yyyy-MM-dd", "icons/evento.png"
        )

        self.asignado_input = self.create_line_edit_with_icon(
            "Persona responsable o equipo", "icons/icono_cliente.png"
        )

        self.prioridad_combo = QComboBox()
        self.prioridad_combo.setStyleSheet(self.combo_style())
        self.prioridad_combo.addItems(["Baja", "Media", "Alta"])

        self.estado_combo = QComboBox()
        self.estado_combo.setStyleSheet(self.combo_style())
        self.estado_combo.addItems(["Pendiente", "En proceso", "Completada"])

        form_layout.addRow("ID Tarea:", self.id_tarea_input)
        form_layout.addRow("Título:", self.titulo_input)
        form_layout.addRow("Descripción:", desc_container)
        form_layout.addRow("Creación:", self.fecha_creacion_input)
        form_layout.addRow("Vencimiento:", self.fecha_vencimiento_input)
        form_layout.addRow("Asignado a:", self.asignado_input)
        form_layout.addRow("Prioridad:", self.prioridad_combo)
        form_layout.addRow("Estado:", self.estado_combo)

        content_layout.addLayout(form_layout)

        # 2.3) Botones CRUD
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        self.create_button = QPushButton("Crear Tarea")
        self.create_button.setStyleSheet(self.button_style("#2ECC71"))
        self.create_button.clicked.connect(self.create_tarea)

        self.update_button = QPushButton("Actualizar Tarea")
        self.update_button.setStyleSheet(self.button_style("#F39C12"))
        self.update_button.clicked.connect(self.update_tarea)

        self.delete_button = QPushButton("Borrar Tarea")
        self.delete_button.setStyleSheet(self.button_style("#E74C3C"))
        self.delete_button.clicked.connect(self.delete_tarea)

        self.clear_button = QPushButton("Limpiar Formulario")
        self.clear_button.setStyleSheet(self.button_style("#3498DB"))
        self.clear_button.clicked.connect(self.clear_form)

        btn_layout.addWidget(self.create_button)
        btn_layout.addWidget(self.update_button)
        btn_layout.addWidget(self.delete_button)
        btn_layout.addWidget(self.clear_button)

        content_layout.addLayout(btn_layout)

        return content_frame

    #  CRUD de Tareas
    def create_tarea(self):
        id_tarea = str(uuid.uuid4())[:8]
        titulo = self.titulo_input.text().strip()
        descripcion = self.descripcion_input.toPlainText().strip()
        fecha_creacion = self.fecha_creacion_input.date().toString("yyyy-MM-dd")
        fecha_vencimiento = self.fecha_vencimiento_input.date().toString("yyyy-MM-dd")
        asignado_a = self.asignado_input.text().strip()
        prioridad = self.prioridad_combo.currentText()
        estado = self.estado_combo.currentText()

        if not titulo:
            self.show_message("El campo 'Título' es obligatorio.")
            return

        # Insertamos
        self.db_manager.insert_tarea(
            id_tarea, titulo, descripcion, fecha_creacion, 
            fecha_vencimiento, asignado_a, prioridad, estado
        )
        self.show_message(f"Tarea '{titulo}' creada con éxito.")
        self.load_tareas()
        self.clear_form()

    def load_tareas(self):
        tareas = self.db_manager.get_all_tareas()
        self.tareas_table.setRowCount(len(tareas))

        for row, tarea in enumerate(tareas):
            # tarea = (ID_TAREA, TITULO, DESCRIPCION, FECHA_CREACION, FECHA_VENCIMIENTO, ASIGNADO_A, PRIORIDAD, ESTADO)
            for col, value in enumerate(tarea):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.tareas_table.setItem(row, col, item)

    def update_tarea(self):
        id_tarea = self.id_tarea_input.text().strip()
        if not id_tarea:
            self.show_message("No hay tarea seleccionada para actualizar.")
            return

        titulo = self.titulo_input.text().strip()
        descripcion = self.descripcion_input.toPlainText().strip()
        fecha_creacion = self.fecha_creacion_input.date().toString("yyyy-MM-dd")
        fecha_vencimiento = self.fecha_vencimiento_input.date().toString("yyyy-MM-dd")
        asignado_a = self.asignado_input.text().strip()
        prioridad = self.prioridad_combo.currentText()
        estado = self.estado_combo.currentText()

        self.db_manager.update_tarea(
            id_tarea, titulo, descripcion, fecha_creacion, 
            fecha_vencimiento, asignado_a, prioridad, estado
        )
        self.show_message(f"Tarea '{titulo}' actualizada con éxito.")
        self.load_tareas()
        self.clear_form()

    def delete_tarea(self):
        id_tarea = self.id_tarea_input.text().strip()
        if not id_tarea:
            self.show_message("No hay tarea seleccionada para borrar.")
            return

        reply = QMessageBox.question(
            self, "Confirmar borrado", 
            "¿Seguro que deseas eliminar esta tarea?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.db_manager.delete_tarea(id_tarea)
            self.show_message("Tarea eliminada con éxito.")
            self.load_tareas()
            self.clear_form()

    #  Selección en la tabla
    def on_table_selection_changed(self):
        selected = self.tareas_table.selectedItems()
        if not selected:
            return
        row = selected[0].row()

        # Cogemos los valores de esa fila
        id_tarea = self.tareas_table.item(row, 0).text()
        titulo = self.tareas_table.item(row, 1).text()
        descripcion = self.tareas_table.item(row, 2).text()
        fecha_creacion = self.tareas_table.item(row, 3).text()
        fecha_vencimiento = self.tareas_table.item(row, 4).text()
        asignado_a = self.tareas_table.item(row, 5).text()
        prioridad = self.tareas_table.item(row, 6).text()
        estado = self.tareas_table.item(row, 7).text()

        # Rellenamos el formulario
        self.id_tarea_input.setText(id_tarea)
        self.titulo_input.setText(titulo)
        self.descripcion_input.setPlainText(descripcion)
        self.fecha_creacion_input.setDate(QDate.fromString(fecha_creacion, "yyyy-MM-dd"))
        self.fecha_vencimiento_input.setDate(QDate.fromString(fecha_vencimiento, "yyyy-MM-dd"))
        self.asignado_input.setText(asignado_a)
        self.prioridad_combo.setCurrentText(prioridad)
        self.estado_combo.setCurrentText(estado)

    #  Otras Utilidades
    def clear_form(self):
        self.id_tarea_input.clear()
        self.titulo_input.clear()
        self.descripcion_input.clear()
        self.fecha_creacion_input.setDate(QDate.currentDate())
        self.fecha_vencimiento_input.setDate(QDate.currentDate())
        self.asignado_input.clear()
        self.prioridad_combo.setCurrentIndex(0)
        self.estado_combo.setCurrentIndex(0)

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
                padding: 5px 15px;
                margin: 5px;
                border-radius: 4px;
            }
            QMessageBox QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        msg.exec_()

    #  Estilos Reutilizables
    def input_style(self):
        return """
            QLineEdit, QDateEdit {
                font-size: 14px;
                padding: 6px;
                border: 2px solid #BDC3C7;
                border-radius: 5px;
                background-color: #ECF0F1;
            }
            QLineEdit:focus, QDateEdit:focus {
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

    def combo_style(self):
        return """
            QComboBox {
                font-size: 14px;
                padding: 6px;
                border: 2px solid #BDC3C7;
                border-radius: 5px;
                background-color: #ECF0F1;
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

    def button_style(self, base_color):
        darker_color = QColor(base_color).darker(110).name()
        return f"""
            QPushButton {{
                background-color: {base_color};
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {darker_color};
            }}
        """

    #  Helpers para crear campos con iconos
    def create_line_edit_with_icon(self, placeholder, icon_path):
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setStyleSheet(self.input_style())
        line_edit.addAction(QIcon(icon_path), QLineEdit.LeadingPosition)
        return line_edit

    def create_date_edit_with_icon(self, display_format, icon_path):
        date_edit = QDateEdit()
        date_edit.setStyleSheet(self.input_style())
        date_edit.setDisplayFormat(display_format)
        if date_edit.lineEdit() is not None:
            date_edit.lineEdit().addAction(QIcon(icon_path), QLineEdit.LeadingPosition)
        return date_edit

    def create_text_edit_with_icon(self, placeholder, icon_path):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(icon_path).pixmap(24, 24))
        layout.addWidget(icon_label)
        text_edit = QTextEdit()
        text_edit.setStyleSheet(self.textedit_style())
        text_edit.setPlaceholderText(placeholder)
        layout.addWidget(text_edit)
        return container, text_edit

    #  MÉTODO PARA MOSTRAR LA BURBUJA ASISTENTE
    def show_assistant(self):
        try:
            if self.assistant_bubble:
                self.assistant_bubble.close()
                self.assistant_bubble = None

            self.assistant_bubble = AssistantBubbleTareas(self, self.assistant_button)
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

    #  CERRAR BURBUJA ASISTENTE AL CERRAR LA VISTA
    def closeEvent(self, event):
        if self.assistant_bubble:
            self.assistant_bubble.close()
        event.accept()