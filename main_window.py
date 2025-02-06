import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout,
    QFrame, QStackedWidget, QPushButton, QApplication
)
from PyQt5.QtGui import QIcon, QFont, QColor, QPixmap, QBrush, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve

from views.clientes_view import ClientesView
from views.oportunidades_view import OportunidadesView
from views.presupuestos_view import PresupuestosView
from views.infoCRM_view import CRMInfoView
from views.inventario_view import InventarioView
from views.pipeline_view import PipelineView
from views.mandarInforme_view import MandarInformeView
from views.miPerfil_view import MiPerfilView
from views.tareas_view import TareasView
from views.calendario_view import CalendarioView
from views.dudas_view import DudasView
from database_manager import DatabaseManager

from rotatable_label import RotatableLabel


class MainWindow(QWidget):
    def __init__(self, empresa_nombre, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.empresa_nombre = empresa_nombre

        self.setWindowTitle(f"{empresa_nombre} - DataNexus CRM")
        self.showFullScreen()
        self.setWindowIcon(QIcon("images/logoApp.png"))

        self.init_ui()

    def init_ui(self):
        """
        Crea la interfaz principal con un encabezado y un layout dividido en
        sidebar (izquierda) y área de contenido (derecha).
        """
        # -- Layout vertical principal --
        main_vertical_layout = QVBoxLayout(self)
        main_vertical_layout.setContentsMargins(0, 0, 0, 0)
        main_vertical_layout.setSpacing(0)

        # 1) Encabezado superior
        self.header_frame = QFrame()
        self.header_frame.setFixedHeight(80)
        self.header_frame.setStyleSheet("""
            QFrame {
                background-color: #2C3E50; /* Mismo color que la parte alta del login */
            }
        """)
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(15, 10, 15, 10)
        header_layout.setSpacing(20)

        # Logo en el encabezado (RotatableLabel)
        self.header_logo_label = RotatableLabel(self)
        header_logo_pix = QPixmap("images/logoApp.png").scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.header_logo_label.setPixmap(header_logo_pix)
        self.header_logo_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # Título en el encabezado
        header_title_label = QLabel(f"Bienvenido a DataNexus")
        header_title_label.setStyleSheet("color: #ECF0F1;")
        header_title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header_title_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # Añado logo y texto al layout del encabezado
        header_layout.addWidget(self.header_logo_label)
        header_layout.addWidget(header_title_label)
        header_layout.addStretch()

        # 2) Contenedor central para sidebar + QStackedWidget
        central_frame = QFrame()
        central_layout = QHBoxLayout(central_frame)
        central_layout.setContentsMargins(5, 5, 5, 5)
        central_layout.setSpacing(5)

        # 2.1) Sidebar
        self.sidebar = QFrame()
        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: #34495E;
                border-radius: 8px;
                margin: 0px;
            }
        """)
        self.sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(10)

        # Botón de mostrar/ocultar sidebar
        self.toggle_button = QPushButton("Menú")
        self.toggle_button.setIcon(QIcon("icons/menu.png"))
        self.toggle_button.setIconSize(QSize(31, 31))
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                color: white;
                border: none;
                padding: 12px;  /* Reducido de 12px a 8px */
                text-align: left;
                font-size: 16px;  /* Reducido de 16px a 14px */
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #4E6D8C;
            }
        """)
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        sidebar_layout.addWidget(self.toggle_button)

        # Definición de los botones del sidebar
        buttons = [
            (" Información CRM", "icons/crm.png", -1),
            (" Clientes", "icons/icono_Cliente.png", 0),
            (" Oportunidades", "icons/oportunidad.png", 1),
            (" Presupuestos", "icons/presupuesto.png", 2),
            (" Inventario", "icons/inventario.png", 3),
            (" Pipeline", "icons/pipeline.png", -2),
            (" Mandar informe", "icons/contacto.png", -3),
            (" Tareas", "icons/tarea.png", -4),
            (" Calendario", "icons/evento.png", -5),
            (" Dudas", "icons/pr.png", -6),
            (" Mi perfil", "icons/miPerfil.png", -7),
            (" Volver", "icons/back.png", -8),
            (" Salir", "icons/logout.png", -9)
        ]

        for text, icon, index in buttons:
            btn = QPushButton(text)
            btn.setIcon(QIcon(icon))
            btn.setIconSize(QSize(31, 31))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #2C3E50;
                    color: white;
                    border: none;
                    padding: 12px;
                    text-align: left;
                    font-size: 16px;  /* Reducido de 16px a 14px */
                    font-weight: bold;
                    border-radius: 6px;
                    margin: 3px 0;
                }}
                QPushButton:hover {{
                    background-color: #4E6D8C;
                }}
            """)
            if text == "Volver":
                btn.setStyleSheet(btn.styleSheet() + "background-color: #27AE60;")
            elif text == "Salir":
                btn.setStyleSheet(btn.styleSheet() + "background-color: #E74C3C;")

            btn.clicked.connect(lambda checked, idx=index: self.change_section(idx))
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # 2.2) Área principal con QStackedWidget
        self.main_area = QStackedWidget()
        self.main_area.setStyleSheet("""
            QStackedWidget {
                background-color: #FFFFFF;
                border-radius: 8px;
                margin: 0px;
            }
        """)

        # Creo y añado todas las vistas
        self.miPerfil_view = MiPerfilView(self.db_manager, self.empresa_nombre)
        self.main_area.addWidget(self.miPerfil_view)
        
        self.client_view = ClientesView(self.db_manager, self.empresa_nombre)
        self.main_area.addWidget(self.client_view)

        self.oportunidades_view = OportunidadesView(self.db_manager, self.empresa_nombre)
        self.main_area.addWidget(self.oportunidades_view)

        self.presupuestos_view = PresupuestosView(self.db_manager, self.empresa_nombre)
        self.main_area.addWidget(self.presupuestos_view)

        self.crm_info_view = CRMInfoView(self.empresa_nombre, self)
        self.main_area.addWidget(self.crm_info_view)

        self.inventario_view = InventarioView(self.db_manager, self.empresa_nombre)
        self.main_area.addWidget(self.inventario_view)

        self.pipeline_view = PipelineView(self.db_manager, self.empresa_nombre, self)
        self.main_area.addWidget(self.pipeline_view)

        self.mandarInforme_view = MandarInformeView(self.db_manager, self.empresa_nombre, self)
        self.main_area.addWidget(self.mandarInforme_view)
        
        self.tareas_view = TareasView(self.db_manager, self.empresa_nombre, self)
        self.main_area.addWidget(self.tareas_view)

        self.calendario_view = CalendarioView(self.db_manager, self.empresa_nombre)
        self.main_area.addWidget(self.calendario_view)

        self.dudas_view = DudasView(self.db_manager, self.empresa_nombre)
        self.main_area.addWidget(self.dudas_view)

        # Defino la vista inicial
        self.main_area.setCurrentWidget(self.crm_info_view)

        # Añado sidebar + main_area al layout horizontal
        central_layout.addWidget(self.sidebar)
        central_layout.addWidget(self.main_area)

        # Añado los 2 frames (header + central) al layout vertical principal
        main_vertical_layout.addWidget(self.header_frame)
        main_vertical_layout.addWidget(central_frame)

        self.sidebar_visible = True
        self.set_gradient_background()
        self.animate_header_logo()

    def set_gradient_background(self):
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#2C3E50"))
        gradient.setColorAt(1, QColor("#3498DB"))

        palette = self.palette()
        palette.setBrush(self.backgroundRole(), QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.set_gradient_background()

    def animate_header_logo(self):
        """
        Animamos la propiedad rotation de 0° a 360° repetidamente,
        consiguiendo una rotación continua en el logo del encabezado.
        """
        self.header_logo_animation = QPropertyAnimation(self.header_logo_label, b"rotation")
        self.header_logo_animation.setDuration(10000)  # 10 segundos para una rotación completa
        self.header_logo_animation.setStartValue(0)
        self.header_logo_animation.setEndValue(360)
        self.header_logo_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.header_logo_animation.setLoopCount(-1)  # Repetir indefinidamente
        self.header_logo_animation.start()

    def toggle_sidebar(self):
        width = self.sidebar.width()
        if self.sidebar_visible:
            # Ocultamos
            new_width = 50
            self.sidebar_visible = False
        else:
            new_width = 250
            self.sidebar_visible = True

        # Animación para transición suave
        self.animation = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

        # Ajustar texto de botones según esté visible u oculto
        for button in self.sidebar.findChildren(QPushButton):
            if button == self.toggle_button:
                continue
            if not button.property("full_text"):
                button.setProperty("full_text", button.text())

            if self.sidebar_visible:
                button.setText(button.property("full_text"))
            else:
                # Si oculta dejo únicamente el ícono
                button.setText("")

    def change_section(self, index):
        if index == -1:
            self.main_area.setCurrentWidget(self.crm_info_view)
        elif index == 0:
            self.main_area.setCurrentWidget(self.client_view)
        elif index == 1:
            self.main_area.setCurrentWidget(self.oportunidades_view)
        elif index == 2:
            self.main_area.setCurrentWidget(self.presupuestos_view)
        elif index == 3:
            self.main_area.setCurrentWidget(self.inventario_view)
        elif index == -2:
            self.main_area.setCurrentWidget(self.pipeline_view)
        elif index == -3:
            self.main_area.setCurrentWidget(self.mandarInforme_view)
        elif index == -4:
            self.main_area.setCurrentWidget(self.tareas_view)
        elif index == -5:
            self.main_area.setCurrentWidget(self.calendario_view)
        elif index == -6:
            self.main_area.setCurrentWidget(self.dudas_view)
        elif index == -7:
            self.main_area.setCurrentWidget(self.miPerfil_view)
        elif index == -8:
            self.open_login_window()
        elif index == -9:
            self.close()

    def open_login_window(self):
        from welcome_window import WelcomeWindow
        self.close()
        self.welcome_window = WelcomeWindow()
        self.welcome_window.show()

from rotatable_label import RotatableLabel


