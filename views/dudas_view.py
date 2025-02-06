import uuid
import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QFormLayout, QLineEdit, QTextEdit, QComboBox, QMessageBox, QDateEdit
)
from PyQt5.QtGui import QPixmap, QFont, QColor, QIcon
from PyQt5.QtCore import Qt, QSize, QDate

from asistentes.burbujaAsistente_dudas import AssistantBubbleDudas


class DudasView(QWidget):
    def __init__(self, db_manager, empresa_nombre):
        super().__init__()
        self.db_manager = db_manager
        self.empresa_nombre = empresa_nombre
        self.assistant_bubble = None
        self.init_ui()

    # Construcción de la Interfaz
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

        # Cargamos todas las FAQs inicialmente
        self.load_faqs()

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

        # Logo (opcional)
        logo_label = QLabel()
        logo_pixmap = QPixmap("images/logoApp.png").scaled(
            100, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # Título
        title_label = QLabel("Preguntas Frecuentes (FAQ)")
        title_label.setStyleSheet("color: #ECF0F1;")  # Texto blanco
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # Botón de Asistente
        self.assistant_button = QPushButton()
        self.assistant_button.setIcon(QIcon("icons/chatbot.png"))  # Asegúrate de tener este ícono
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
        header_layout.addWidget(self.assistant_button)  # Añadimos el botón de asistente

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

        # 1) Barra de Búsqueda
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar pregunta / respuesta...")
        self.search_input.setStyleSheet(self.input_style())
        search_layout.addWidget(self.search_input)

        self.search_button = QPushButton("Buscar")
        self.search_button.setStyleSheet(self.button_style("#3498DB"))
        self.search_button.clicked.connect(self.search_faqs)
        search_layout.addWidget(self.search_button)

        content_layout.addLayout(search_layout)

        # 2) Tabla de FAQ
        self.faq_table = QTableWidget()
        self.faq_table.setColumnCount(5)  # ID, Pregunta, Respuesta, Categoría, Última Actualización
        self.faq_table.setHorizontalHeaderLabels([
            "ID", "Pregunta", "Respuesta", "Categoría", "Última Act."
        ])
        self.faq_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.faq_table.setAlternatingRowColors(True)
        self.faq_table.setStyleSheet("""
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
        self.faq_table.itemSelectionChanged.connect(self.on_table_selection_changed)
        content_layout.addWidget(self.faq_table)

        # 3) Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        self.id_faq_input = QLineEdit()
        self.id_faq_input.setPlaceholderText("ID de la FAQ (auto)")
        self.id_faq_input.setReadOnly(True)
        self.id_faq_input.setStyleSheet(self.input_style())

        self.pregunta_input = QLineEdit()
        self.pregunta_input.setPlaceholderText("Pregunta...")
        self.pregunta_input.setStyleSheet(self.input_style())

        self.respuesta_input = QTextEdit()
        self.respuesta_input.setPlaceholderText("Respuesta detallada...")
        self.respuesta_input.setStyleSheet(self.textedit_style())

        self.categoria_input = QComboBox()
        self.categoria_input.setStyleSheet(self.combo_style())
        # Ejemplo de categorías:
        self.categoria_input.addItems(["General", "Login", "Oportunidades", "Presupuestos", "Inventario", "Otro"])

        form_layout.addRow("ID FAQ:", self.id_faq_input)
        form_layout.addRow("Pregunta:", self.pregunta_input)
        form_layout.addRow("Respuesta:", self.respuesta_input)
        form_layout.addRow("Categoría:", self.categoria_input)

        content_layout.addLayout(form_layout)

        # 4) Botones CRUD
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        self.create_button = QPushButton("Crear FAQ")
        self.create_button.setStyleSheet(self.button_style("#2ECC71"))
        self.create_button.clicked.connect(self.create_faq)

        self.update_button = QPushButton("Actualizar FAQ")
        self.update_button.setStyleSheet(self.button_style("#F39C12"))
        self.update_button.clicked.connect(self.update_faq)

        self.delete_button = QPushButton("Borrar FAQ")
        self.delete_button.setStyleSheet(self.button_style("#E74C3C"))
        self.delete_button.clicked.connect(self.delete_faq)

        self.clear_button = QPushButton("Limpiar")
        self.clear_button.setStyleSheet(self.button_style("#3498DB"))
        self.clear_button.clicked.connect(self.clear_form)

        btn_layout.addWidget(self.create_button)
        btn_layout.addWidget(self.update_button)
        btn_layout.addWidget(self.delete_button)
        btn_layout.addWidget(self.clear_button)

        content_layout.addLayout(btn_layout)

        return content_frame

    # Manejo de FAQ (CRUD + Búsqueda)
    def load_faqs(self):
        faqs = self.db_manager.get_all_faqs()
        self.populate_faq_table(faqs)

    def populate_faq_table(self, faqs):
        self.faq_table.setRowCount(len(faqs))
        for row, faq in enumerate(faqs):
            # faq = (ID_FAQ, PREGUNTA, RESPUESTA, CATEGORIA, ULTIMA_ACTUALIZACION)
            for col, value in enumerate(faq):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.faq_table.setItem(row, col, item)

    def search_faqs(self):
        keyword = self.search_input.text().strip()
        if not keyword:
            # Si no hay palabra clave, cargamos todo
            self.load_faqs()
        else:
            faqs = self.db_manager.search_faqs_by_keyword(keyword)
            self.populate_faq_table(faqs)

    def create_faq(self):
        id_faq = str(uuid.uuid4())[:8]
        pregunta = self.pregunta_input.text().strip()
        respuesta = self.respuesta_input.toPlainText().strip()
        categoria = self.categoria_input.currentText()
        # Usamos la fecha actual como "Última actualización"
        ultima_act = datetime.date.today().strftime("%Y-%m-%d")

        if not pregunta or not respuesta:
            self.show_message("La 'Pregunta' y 'Respuesta' son obligatorias.")
            return

        self.db_manager.insert_faq(id_faq, pregunta, respuesta, categoria, ultima_act)
        self.show_message(f"FAQ creada con ID {id_faq}.")
        self.load_faqs()
        self.clear_form()

    def update_faq(self):
        id_faq = self.id_faq_input.text().strip()
        if not id_faq:
            self.show_message("No hay FAQ seleccionada para actualizar.")
            return

        pregunta = self.pregunta_input.text().strip()
        respuesta = self.respuesta_input.toPlainText().strip()
        categoria = self.categoria_input.currentText()
        ultima_act = datetime.date.today().strftime("%Y-%m-%d")

        self.db_manager.update_faq(id_faq, pregunta, respuesta, categoria, ultima_act)
        self.show_message(f"FAQ '{id_faq}' actualizada.")
        self.load_faqs()
        self.clear_form()

    def delete_faq(self):
        id_faq = self.id_faq_input.text().strip()
        if not id_faq:
            self.show_message("No hay FAQ seleccionada para eliminar.")
            return

        reply = QMessageBox.question(
            self, "Confirmar borrado",
            "¿Está seguro de que desea eliminar esta FAQ?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.db_manager.delete_faq(id_faq)
            self.show_message("FAQ eliminada.")
            self.load_faqs()
            self.clear_form()

    def on_table_selection_changed(self):
        selected = self.faq_table.selectedItems()
        if not selected:
            return
        row = selected[0].row()

        id_faq = self.faq_table.item(row, 0).text()
        pregunta = self.faq_table.item(row, 1).text()
        respuesta = self.faq_table.item(row, 2).text()
        categoria = self.faq_table.item(row, 3).text()
        ultima_act = self.faq_table.item(row, 4).text()

        self.id_faq_input.setText(id_faq)
        self.pregunta_input.setText(pregunta)
        self.respuesta_input.setPlainText(respuesta)
        self.categoria_input.setCurrentText(categoria)

    def clear_form(self):
        self.id_faq_input.clear()
        self.pregunta_input.clear()
        self.respuesta_input.clear()
        self.categoria_input.setCurrentIndex(0)

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

    def input_style(self):
        return """
            QLineEdit {
                font-size: 14px;
                padding: 6px;
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

    #  MÉTODO PARA MOSTRAR LA BURBUJA ASISTENTE
    def show_assistant(self):
        """
        Crea y muestra la burbuja asistente específica para DudasView.
        """
        try:
            if self.assistant_bubble:
                self.assistant_bubble.close()
                self.assistant_bubble = None

            self.assistant_bubble = AssistantBubbleDudas(self, self.assistant_button)
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