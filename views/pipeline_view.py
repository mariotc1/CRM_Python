from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,
    QMessageBox, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QSize

from asistentes.burbujaAsistente_pipeline import AssistantBubblePipeline


class PipelineView(QWidget):
    update_signal = pyqtSignal()

    def __init__(self, db_manager, empresa_nombre, main_window):
        super().__init__()
        self.db_manager = db_manager
        self.empresa_nombre = empresa_nombre
        self.main_window = main_window
        self.assistant_bubble = None
        self.init_ui()

    def init_ui(self):
        # Fondo general para la vista
        self.setStyleSheet("background-color: #BDC3C7;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1) Encabezado con fondo de color sólido (sin degradado)
        header_frame = self.create_header()
        main_layout.addWidget(header_frame)

        # 2) Contenedor principal (efecto "tarjeta" con sombra)
        content_frame = self.create_content()

        # Agregar sombra para dar efecto de elevación al contenedor blanco
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 80))
        content_frame.setGraphicsEffect(shadow)

        main_layout.addWidget(content_frame)

        self.refresh_pipeline()

    # --- Encabezado ---
    def create_header(self):
        header_frame = QFrame()
        header_frame.setFixedHeight(80)
        # Se reemplaza el degradado horizontal por un color sólido
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
        title_label = QLabel(f"Pipeline de Ventas - {self.empresa_nombre}")
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

    # --- Contenedor de Contenido ---
    def create_content(self):
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #BDC3C7;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
                margin: 0px;
                padding: 20px;
            }
        """)

        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # Pipeline Stages: cada etapa con su tabla
        stages_layout = QHBoxLayout()
        stages_layout.setSpacing(15)

        self.stage_tables = {}
        stages = ["NUEVO", "CALIFICADO", "PROPUESTA", "GANADO"]
        for stage in stages:
            stage_layout = QVBoxLayout()
            stage_layout.setSpacing(10)

            # Etiqueta de la etapa
            stage_label = QLabel(stage)
            stage_label.setAlignment(Qt.AlignCenter)
            stage_label.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    font-weight: bold;
                    color: #2C3E50;
                }
            """)
            stage_layout.addWidget(stage_label)

            # Tabla de oportunidades
            table = QTableWidget()
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["ID", "Cliente", "Valor", "Mover a"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.setAlternatingRowColors(True)
            table.setStyleSheet("""
                QTableWidget {
                    background-color: #FFFFFF;
                    alternate-background-color: #ECF0F1;
                    gridline-color: #BDC3C7;
                }
                QTableWidget::item {
                    padding: 5px;
                }
                /* Encabezados con fondo sólido */
                QHeaderView::section {
                    background-color: #3498DB;
                    color: white;
                    font-weight: bold;
                    border: none;
                    padding: 8px;
                }
            """)
            table.setMinimumWidth(350)
            table.setFont(QFont("Segoe UI", 10))
            table.verticalHeader().setDefaultSectionSize(35)
            table.verticalHeader().setVisible(False)
            table.setEditTriggers(QTableWidget.NoEditTriggers)

            stage_layout.addWidget(table)
            self.stage_tables[stage] = table
            stages_layout.addLayout(stage_layout)

        content_layout.addLayout(stages_layout)

        # Botones de acción
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        self.refresh_button = self.create_styled_button("Actualizar", "#3498DB", self.refresh_pipeline)
        self.go_to_opportunities_button = self.create_styled_button("Ir a Oportunidades", "#2ECC71", self.go_to_opportunities)

        btn_layout.addWidget(self.refresh_button)
        btn_layout.addWidget(self.go_to_opportunities_button)

        content_layout.addLayout(btn_layout)

        return content_frame

    # --- Botón Estilizado ---
    def create_styled_button(self, text, color, callback):
        button = QPushButton(text, self)
        button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {QColor(color).darker(110).name()};
            }}
        """)
        button.clicked.connect(callback)
        return button

    # --- Refrescar Pipeline ---
    def refresh_pipeline(self):
        """
        Carga las oportunidades desde la DB y las ubica en la tabla correspondiente
        según su etapa (NUEVO, CALIFICADO, PROPUESTA, GANADO). Cada oportunidad tiene el formato:
        (ID_OPORTUNIDAD, CLIENTE, INGRESO_ESPERADO, ESTADO)
        """
        opportunities = self.db_manager.get_all_opportunities()

        # Limpiar todas las tablas
        for stage, table in self.stage_tables.items():
            table.setRowCount(0)

        # Ubicar cada oportunidad en su etapa correspondiente
        for opp in opportunities:
            opp_id, opp_cliente, opp_valor, opp_stage = opp
            opp_stage = opp_stage.upper()
            if opp_stage not in self.stage_tables:
                opp_stage = "NUEVO"

            table = self.stage_tables[opp_stage]
            row = table.rowCount()
            table.insertRow(row)

            # Columna 0: ID
            id_item = QTableWidgetItem(str(opp_id))
            id_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 0, id_item)

            # Columna 1: Cliente
            cliente_item = QTableWidgetItem(str(opp_cliente))
            cliente_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 1, cliente_item)

            # Columna 2: Valor  
            # Puedes cambiar la alineación a derecha si lo prefieres: Qt.AlignRight | Qt.AlignVCenter
            valor_item = QTableWidgetItem(str(opp_valor))
            valor_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 2, valor_item)

            # Columna 3: ComboBox para cambiar de etapa
            change_stage_combo = QComboBox()
            change_stage_combo.setStyleSheet(self.combo_style())
            change_stage_combo.setMinimumHeight(35)
            # Excluir la etapa actual
            other_stages = [s for s in self.stage_tables.keys() if s != opp_stage]
            change_stage_combo.addItem("Mover a...")
            change_stage_combo.addItems(other_stages)

            # Se usa un argumento por defecto para capturar el id actual de la oportunidad
            change_stage_combo.currentTextChanged.connect(
                lambda new_stage, opp_id=opp_id: self.handle_stage_change(opp_id, new_stage)
            )
            table.setCellWidget(row, 3, change_stage_combo)

    def handle_stage_change(self, opp_id, new_stage):
        """
        Actualiza el stage de la oportunidad en la DB y refresca el pipeline.
        Se ignora la opción por defecto "Mover a...".
        """
        if new_stage in ("Mover a...", ""):
            return
        try:
            self.db_manager.update_opportunity_stage(opp_id, new_stage)
            self.refresh_pipeline()
            self.show_message(f"Oportunidad {opp_id} movida a la etapa '{new_stage}'")
        except Exception as e:
            self.show_message(f"Error al cambiar la etapa de la oportunidad: {str(e)}")

    def combo_style(self):
        return """
            QComboBox {
                padding: 8px;
                border: 2px solid #BDC3C7;
                border-radius: 5px;
                background-color: #ECF0F1;
                font-size: 14px;
                min-height: 35px;
            }
            QComboBox:focus {
                border: 2px solid #3498DB;
                background-color: #FFFFFF;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
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

    # --- Cambio de Sección ---
    def go_to_opportunities(self):
        self.main_window.change_section(1)

    # --- Mostrar Mensajes ---
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
                color: #fff;
                padding: 5px 20px;
                margin: 5px;
                border-radius: 4px;
            }
            QMessageBox QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        msg.exec_()

    # --- Mostrar la burbuja asistente ---
    def show_assistant(self):
        try:
            if self.assistant_bubble:
                self.assistant_bubble.close()
                self.assistant_bubble = None

            self.assistant_bubble = AssistantBubblePipeline(self, self.assistant_button)
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

    # --- Al cerrar la vista, se cierra la burbuja asistente ---
    def closeEvent(self, event):
        if self.assistant_bubble:
            self.assistant_bubble.close()
        event.accept()
