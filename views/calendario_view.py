import uuid
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QCalendarWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QFormLayout,
    QLineEdit, QTextEdit, QTimeEdit, QComboBox, QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont, QColor, QIcon
from PyQt5.QtCore import Qt, QDate, QTime, QSize

from asistentes.burbujaAsistente_calendario import AssistantBubbleCalendario


class CalendarioView(QWidget):
    def __init__(self, db_manager, empresa_nombre):
        super().__init__()
        self.db_manager = db_manager
        self.empresa_nombre = empresa_nombre
        self.assistant_bubble = None
        self.init_ui()

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
        title_label = QLabel("Calendario de Eventos")
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

        # 2 secciones horizontales:
        # - Izquierda: QCalendarWidget
        # - Derecha: Tabla de eventos + Formulario
        main_h_layout = QHBoxLayout()
        main_h_layout.setSpacing(20)

        # Calendario (Izquierda)
        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet(self.calendar_style())
        self.calendar.setGridVisible(True)  # Muestra líneas de cuadrícula
        self.calendar.selectionChanged.connect(self.on_date_selected)
        main_h_layout.addWidget(self.calendar, 1)  # 'stretch' 1

        # Derecha -> Tabla + Formulario
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)

        # 2.1) Tabla de eventos
        self.eventos_table = QTableWidget()
        self.eventos_table.setColumnCount(6)  # ID, Título, Hora, Lugar, Descripción, Asignado
        self.eventos_table.setHorizontalHeaderLabels([
            "ID", "Título", "Hora", "Lugar", "Descripción", "Asignado A"
        ])
        self.eventos_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.eventos_table.setAlternatingRowColors(True)
        self.eventos_table.setStyleSheet("""
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
        self.eventos_table.itemSelectionChanged.connect(self.on_table_selection_changed)
        right_layout.addWidget(self.eventos_table, 2)

        # 2.2) Formulario para crear/editar evento
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Usamos helpers para los QLineEdit y QTimeEdit con íconos,
        # excepto en el campo "Descripción", que se deja sin ícono.
        self.id_evento_input = self.create_line_edit_with_icon(
            "ID del evento (auto)", "icons/id.png"
        )
        self.id_evento_input.setReadOnly(True)

        self.titulo_input = self.create_line_edit_with_icon(
            "Título del evento", "icons/descripcion.png"
        )

        # Para la hora se usa un QTimeEdit con ícono
        self.hora_input = self.create_time_edit_with_icon(
            "HH:mm", "icons/tiempo.png"
        )

        self.lugar_input = self.create_line_edit_with_icon(
            "Lugar (sala, oficina, etc.)", "icons/ubicacion.png"
        )

        # En el campo de descripción NO se agrega ícono
        self.descripcion_input = QTextEdit()
        self.descripcion_input.setStyleSheet(self.textedit_style())
        self.descripcion_input.setPlaceholderText("Descripción u observaciones")

        self.asignado_input = self.create_line_edit_with_icon(
            "Asignado a...", "icons/icono_cliente.png"
        )

        form_layout.addRow("ID Evento:", self.id_evento_input)
        form_layout.addRow("Título:", self.titulo_input)
        form_layout.addRow("Hora:", self.hora_input)
        form_layout.addRow("Lugar:", self.lugar_input)
        form_layout.addRow("Descripción:", self.descripcion_input)
        form_layout.addRow("Asignado a:", self.asignado_input)

        # 2.3) Botones de acción (crear, actualizar, borrar, limpiar)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        self.create_button = QPushButton("Crear Evento")
        self.create_button.setStyleSheet(self.button_style("#2ECC71"))
        self.create_button.clicked.connect(self.create_evento)

        self.update_button = QPushButton("Actualizar Evento")
        self.update_button.setStyleSheet(self.button_style("#F39C12"))
        self.update_button.clicked.connect(self.update_evento)

        self.delete_button = QPushButton("Borrar Evento")
        self.delete_button.setStyleSheet(self.button_style("#E74C3C"))
        self.delete_button.clicked.connect(self.delete_evento)

        self.clear_button = QPushButton("Limpiar")
        self.clear_button.setStyleSheet(self.button_style("#3498DB"))
        self.clear_button.clicked.connect(self.clear_form)

        btn_layout.addWidget(self.create_button)
        btn_layout.addWidget(self.update_button)
        btn_layout.addWidget(self.delete_button)
        btn_layout.addWidget(self.clear_button)

        right_layout.addLayout(form_layout, 3)
        right_layout.addLayout(btn_layout)

        main_h_layout.addLayout(right_layout, 2)

        content_layout.addLayout(main_h_layout)

        return content_frame

    # MÉTODOS DE MANEJO DE EVENTOS (Crear, Actualizar, Borrar, etc.)
    def create_evento(self):
        id_evento = str(uuid.uuid4())[:8]
        titulo = self.titulo_input.text().strip()
        fecha_qdate = self.calendar.selectedDate()
        fecha_str = fecha_qdate.toString("yyyy-MM-dd")
        hora_str = self.hora_input.time().toString("HH:mm")
        lugar = self.lugar_input.text().strip()
        descripcion = self.descripcion_input.toPlainText().strip()
        asignado_a = self.asignado_input.text().strip()

        if not titulo:
            self.show_message("El título es obligatorio para crear un evento.")
            return

        self.db_manager.insert_evento(
            id_evento, titulo, fecha_str, hora_str, lugar, descripcion, asignado_a
        )
        self.show_message(f"Evento '{titulo}' creado.")
        self.load_eventos_del_dia(fecha_str)
        self.clear_form()

    def load_eventos_del_dia(self, fecha_str):
        eventos = self.db_manager.get_eventos_por_fecha(fecha_str)
        self.eventos_table.setRowCount(len(eventos))

        for row, evento in enumerate(eventos):
            # evento = (ID_EVENTO, TITULO, FECHA, HORA, LUGAR, DESCRIPCION, ASIGNADO_A)
            item_id = QTableWidgetItem(str(evento[0]))
            item_titulo = QTableWidgetItem(str(evento[1]))
            item_hora = QTableWidgetItem(str(evento[3]))
            item_lugar = QTableWidgetItem(str(evento[4]))
            item_desc = QTableWidgetItem(str(evento[5]))
            item_asignado = QTableWidgetItem(str(evento[6]))

            for itm in [item_id, item_titulo, item_hora, item_lugar, item_desc, item_asignado]:
                itm.setTextAlignment(Qt.AlignCenter)

            self.eventos_table.setItem(row, 0, item_id)
            self.eventos_table.setItem(row, 1, item_titulo)
            self.eventos_table.setItem(row, 2, item_hora)
            self.eventos_table.setItem(row, 3, item_lugar)
            self.eventos_table.setItem(row, 4, item_desc)
            self.eventos_table.setItem(row, 5, item_asignado)

    def update_evento(self):
        id_evento = self.id_evento_input.text().strip()
        if not id_evento:
            self.show_message("No hay evento seleccionado para actualizar.")
            return

        titulo = self.titulo_input.text().strip()
        fecha_str = self.calendar.selectedDate().toString("yyyy-MM-dd")
        hora_str = self.hora_input.time().toString("HH:mm")
        lugar = self.lugar_input.text().strip()
        descripcion = self.descripcion_input.toPlainText().strip()
        asignado_a = self.asignado_input.text().strip()

        self.db_manager.update_evento(
            id_evento, titulo, fecha_str, hora_str, lugar, descripcion, asignado_a
        )
        self.show_message(f"Evento '{titulo}' actualizado.")
        self.load_eventos_del_dia(fecha_str)
        self.clear_form()

    def delete_evento(self):
        id_evento = self.id_evento_input.text().strip()
        if not id_evento:
            self.show_message("No hay evento seleccionado para borrar.")
            return

        reply = QMessageBox.question(
            self, "Confirmar borrado",
            "¿Está seguro de querer eliminar este evento?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.db_manager.delete_evento(id_evento)
            fecha_str = self.calendar.selectedDate().toString("yyyy-MM-dd")
            self.load_eventos_del_dia(fecha_str)
            self.show_message("Evento eliminado.")
            self.clear_form()

    def on_date_selected(self):
        fecha_str = self.calendar.selectedDate().toString("yyyy-MM-dd")
        self.load_eventos_del_dia(fecha_str)
        self.clear_form()

    def on_table_selection_changed(self):
        selected = self.eventos_table.selectedItems()
        if not selected:
            return
        row = selected[0].row()

        id_evento = self.eventos_table.item(row, 0).text()
        titulo = self.eventos_table.item(row, 1).text()
        hora = self.eventos_table.item(row, 2).text()
        lugar = self.eventos_table.item(row, 3).text()
        desc = self.eventos_table.item(row, 4).text()
        asignado = self.eventos_table.item(row, 5).text()

        self.id_evento_input.setText(id_evento)
        self.titulo_input.setText(titulo)

        hhmm = hora.split(":")
        if len(hhmm) == 2:
            self.hora_input.setTime(QTime(int(hhmm[0]), int(hhmm[1])))
        self.lugar_input.setText(lugar)
        self.descripcion_input.setPlainText(desc)
        self.asignado_input.setText(asignado)

    def clear_form(self):
        self.id_evento_input.clear()
        self.titulo_input.clear()
        self.hora_input.setTime(QTime.currentTime())
        self.lugar_input.clear()
        self.descripcion_input.clear()
        self.asignado_input.clear()

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

    def calendar_style(self):
        return """
            QCalendarWidget QAbstractItemView:enabled {
                font-size: 14px;
                color: #2C3E50; 
                background-color: #ECF0F1;
                selection-background-color: #3498DB;
                selection-color: #fff;
            }
        """

    def input_style(self):
        return """
            QLineEdit, QTimeEdit {
                font-size: 14px;
                padding: 6px;
                border: 2px solid #BDC3C7;
                border-radius: 5px;
                background-color: #ECF0F1;
            }
            QLineEdit:focus, QTimeEdit:focus {
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

    # Helpers para crear campos con íconos (excepto la descripción)
    def create_line_edit_with_icon(self, placeholder, icon_path):
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setStyleSheet(self.input_style())
        line_edit.addAction(QIcon(icon_path), QLineEdit.LeadingPosition)
        return line_edit

    def create_time_edit_with_icon(self, display_format, icon_path):
        time_edit = QTimeEdit()
        time_edit.setStyleSheet(self.input_style())
        time_edit.setDisplayFormat(display_format)
        if time_edit.lineEdit() is not None:
            time_edit.lineEdit().addAction(QIcon(icon_path), QLineEdit.LeadingPosition)
        return time_edit

    def show_assistant(self):
        try:
            if self.assistant_bubble:
                self.assistant_bubble.close()
                self.assistant_bubble = None

            self.assistant_bubble = AssistantBubbleCalendario(self, self.assistant_button)
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