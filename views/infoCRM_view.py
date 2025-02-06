import webbrowser
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton,
    QScrollArea, QFrame
)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QSize
from asistentes.burbujaAsistente_infoCRM import AssistantBubbleCRMInfo

class CRMInfoView(QWidget):
    def __init__(self, empresa_nombre, main_window):
        super().__init__()
        self.empresa_nombre = empresa_nombre
        self.main_window = main_window
        self.assistant_bubble = None
        self.init_ui()

    def init_ui(self):
        """
        Genera una interfaz con un encabezado (#2C3E50)
        y un contenedor blanco (scrollable) para la info, accesos directos, etc.
        """
        # Layout vertical principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1) ENCABEZADO superior
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
            120, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # Título en el encabezado
        title_label = QLabel("DataNexus CRM")
        title_label.setStyleSheet("color: #ECF0F1;")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # Botón de asistente en el encabezado
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
        header_layout.addWidget(self.assistant_button)  # Añadimos el botón

        # 2) CONTENEDOR para el scroll
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
                margin: 0px;
                padding: 0px;
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # Un scroll_area para la información extensa
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)

        scroll_content = QWidget()
        scroll_content_layout = QVBoxLayout(scroll_content)
        scroll_content_layout.setSpacing(20)
        scroll_content_layout.setContentsMargins(0, 0, 0, 0)

        # 2.1) Mensaje de bienvenida combinado
        welcome_combined_label = QLabel(f"""
            <div style="text-align: center;">
                <span style="font-size: 24px; color: #2C3E50; font-weight: bold;">
                    ¡Hola {self.empresa_nombre}!
                </span><br>
                <span style="font-size: 18px; color: #7F8C8D;">
                    Estamos encantados de que confíes en nosotros.
                </span>
            </div>
        """)
        welcome_combined_label.setAlignment(Qt.AlignCenter)
        welcome_combined_label.setWordWrap(True)

        # 2.2) Información detallada 
        info_text = """
        <h3>DataNexus CRM: Tu aliado en la gestión de clientes</h3>
        <p>Nuestra herramienta está diseñada para ayudarte a gestionar tus relaciones con los clientes de manera eficiente y efectiva.</p>
        <h4>Con DataNexus CRM podrás:</h4>
        <ul>
            <li>📊 Gestionar clientes y sus datos de contacto</li>
            <li>🎯 Seguir oportunidades de venta</li>
            <li>💼 Crear y gestionar presupuestos</li>
            <li>📈 Analizar tu pipeline de ventas</li>
            <li>📨 Mandar informes a tus clientes</li>
            <li>✅ Gestionar tus tareas</li>
            <li>🗓️ Ver tus eventos en el calendario</li>
            <li>❓ Gestionar las dudas</li>
            <li>🚀 Y mucho más...</li>
        </ul>
        <p>Estamos aquí para ayudarte a hacer crecer tu negocio y mejorar tus relaciones con los clientes.</p>
        """
        info_label = QLabel(info_text)
        info_label.setStyleSheet("""
            font-size: 16px;
            line-height: 1.5;
            color: #2C3E50;
        """)
        info_label.setWordWrap(True)
        info_label.setTextFormat(Qt.RichText)

        # ---------------------------------------------------------
        # 2.3) Accesos directos (botones)
        # ---------------------------------------------------------
        shortcuts_label = QLabel("Accesos directos a nuestras herramientas")
        shortcuts_label.setAlignment(Qt.AlignCenter)
        shortcuts_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #2C3E50;
        """)

        shortcuts_layout = QHBoxLayout()
        shortcuts_layout.setSpacing(10)
        shortcuts_layout.setContentsMargins(0, 0, 0, 0)
        shortcuts_layout.setAlignment(Qt.AlignCenter)
        shortcuts = [
            (" Clientes", "icons/icono_Cliente.png", "#3498db", 0),
            (" Oportunidades", "icons/oportunidad.png", "#2ecc71", 1),
            (" Presupuestos", "icons/presupuesto.png", "#e74c3c", 2),
            (" Inventario", "icons/inventario.png", "#f39c12", 3),
            (" Pipeline", "icons/pipeline.png", "#9b59b6", -2),
            (" Mandar Informe", "icons/contacto.png", "#3498db", -3),
            (" Crear tareas", "icons/tarea.png", "#2ecc71", -4),
            (" Calendario", "icons/evento.png", "#e74c3c", -5),
            (" Dudas", "icons/pr.png", "#f39c12", -6),
            (" Mi perfil", "icons/miPerfil.png", "#9b59b6", -7)
        ]
        for text, icon_path, color, idx in shortcuts:
            btn = QPushButton(text)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(24, 24))  # Reducido de iconos si es necesario
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    font-size: 14px;
                    padding: 10px;  /* Reducido de 15px */
                    border-radius: 8px;
                }}
                QPushButton:hover {{
                    background-color: {self.darken_color(color)};
                }}
            """)
            btn.setMinimumWidth(120)  # Asegura un tamaño mínimo
            btn.clicked.connect(lambda _, i=idx: self.main_window.change_section(i))
            shortcuts_layout.addWidget(btn)

        # ---------------------------------------------------------
        # 2.4) Redes sociales y contacto
        # ---------------------------------------------------------
        social_label = QLabel("Contáctanos por nuestras redes")
        social_label.setAlignment(Qt.AlignCenter)
        social_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #2C3E50;
        """)

        social_layout = QHBoxLayout()
        social_layout.setSpacing(10)
        social_layout.setContentsMargins(0, 0, 0, 0)
        social_layout.setAlignment(Qt.AlignCenter)
        social_links = [
            ("Instagram", "icons/instagram.png", "https://www.instagram.com/datanexus"),
            ("Email", "icons/correo-electronico.png", "mailto:info@datanexus.com"),
            ("Teléfono", "icons/phone_icon.png", "tel:+983102027"),
            ("WhatsApp", "icons/whatsApp.png", "https://wa.me/+34644071074")
        ]
        for text, icon_path, link_url in social_links:
            btn = QPushButton(text)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(24, 24))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #34495E;
                    color: white;
                    font-size: 14px;
                    padding: 10px;  /* Reducido de 15px */
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #2C3E50;
                }
            """)
            btn.setMinimumWidth(120)  # Asegura un tamaño mínimo
            btn.clicked.connect(lambda _, url=link_url: self.open_link(url))
            social_layout.addWidget(btn)

        scroll_content_layout.addWidget(welcome_combined_label)
        scroll_content_layout.addWidget(info_label)

        scroll_content_layout.addWidget(shortcuts_label)
        scroll_content_layout.addLayout(shortcuts_layout)

        scroll_content_layout.addWidget(social_label)
        scroll_content_layout.addLayout(social_layout)

        scroll_area.setWidget(scroll_content)

        content_layout.addWidget(scroll_area)

        main_layout.addWidget(header_frame)
        main_layout.addWidget(content_frame)

    def open_link(self, url):
        webbrowser.open(url)

    def darken_color(self, color):
        """
        Hace el color ligeramente más oscuro para el hover.
        E.g. #E74C3C -> un tono algo más oscuro.
        """
        c = QColor(color)
        h, s, v, a = c.getHsv()
        v = max(0, v - 30)
        c = QColor()
        c.setHsv(h, s, v, a)
        return c.name()

    def show_assistant(self):
        """
        Crea y muestra la burbuja asistente específica para CRMInfoView.
        """
        try:
            if self.assistant_bubble:
                self.assistant_bubble.close()
                self.assistant_bubble = None

            self.assistant_bubble = AssistantBubbleCRMInfo(self, self.assistant_button)
            self.assistant_bubble.show()
        except Exception as e:
            error_msg = f"Error al mostrar la burbuja asistente: {str(e)}"
            print(error_msg)
            from PyQt5.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(error_msg)
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
