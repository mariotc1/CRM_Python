import webbrowser
from urllib.parse import quote
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton, QGroupBox, QFormLayout, QMessageBox, QComboBox, QFrame
)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor
from PyQt5.QtCore import Qt, QDate, QSize

from asistentes.burbujaAsistente_mandarInforme import AssistantBubbleMandarInforme


class MandarInformeView(QWidget):
    def __init__(self, db_manager, empresa_nombre, main_window):
        super().__init__()
        self.db_manager = db_manager
        self.empresa_nombre = empresa_nombre
        self.main_window = main_window
        self.assistant_bubble = None
        self.init_ui()

    def init_ui(self):
        # Layout principal vertical
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1) Encabezado oscuro
        header_frame = self.create_header()
        main_layout.addWidget(header_frame)

        # 2) Contenedor blanco para combos y paneles (WhatsApp / Email)
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
        title_label = QLabel(f"Enviar Informe - {self.empresa_nombre}")
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
        header_layout.addWidget(self.assistant_button)  # botón de asistente

        return header_frame

    #  CONTENEDOR BLANCO (Combos + Paneles WhatsApp/Email)
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

        # Sección para elegir "tipo de informe" y "ID"
        selection_layout = QHBoxLayout()
        selection_layout.setSpacing(15)

        self.comboTipoInforme = QComboBox()
        self.comboTipoInforme.setStyleSheet(self.combo_style())
        self.comboTipoInforme.addItems(["Seleccione un tipo", "Cliente", "Oportunidad", "Presupuesto"])
        self.comboTipoInforme.currentIndexChanged.connect(self.on_tipo_informe_changed)
        selection_layout.addWidget(self.comboTipoInforme)

        self.comboId = QComboBox()
        self.comboId.setStyleSheet(self.combo_style())
        self.comboId.currentIndexChanged.connect(self.on_id_changed)
        selection_layout.addWidget(self.comboId)

        content_layout.addLayout(selection_layout)

        # Paneles: WhatsApp (izquierda) y Email (derecha)
        panels_layout = QHBoxLayout()
        panels_layout.setSpacing(20)

        # Panel Izquierdo
        whatsapp_group = self.create_whatsapp_group()
        panels_layout.addWidget(whatsapp_group)

        # Panel Derecho
        email_group = self.create_email_group()
        panels_layout.addWidget(email_group)

        content_layout.addLayout(panels_layout)

        return content_frame

    #  Grupo WhatsApp
    def create_whatsapp_group(self):
        whatsapp_group = QGroupBox("Enviar Informe por WhatsApp")
        whatsapp_group.setStyleSheet(self.group_box_style())

        whatsapp_layout = QFormLayout(whatsapp_group)
        whatsapp_layout.setContentsMargins(10, 10, 10, 10)
        whatsapp_layout.setSpacing(10)

        self.whatsapp_number_input = QLineEdit()
        self.whatsapp_number_input.setStyleSheet(self.input_style())
        self.whatsapp_number_input.setPlaceholderText("Número de teléfono (ej: +34...)")
        whatsapp_layout.addRow("Número:", self.whatsapp_number_input)

        self.whatsapp_message_text = QTextEdit()
        self.whatsapp_message_text.setStyleSheet(self.textedit_style())
        self.whatsapp_message_text.setPlaceholderText("Mensaje a enviar...")
        whatsapp_layout.addRow("Mensaje:", self.whatsapp_message_text)

        self.send_whatsapp_button = QPushButton(" Enviar por WhatsApp")
        self.send_whatsapp_button.setIcon(QIcon("icons/whatsapp.png"))
        self.send_whatsapp_button.setStyleSheet(self.button_style("#2ECC71"))
        self.send_whatsapp_button.clicked.connect(self.send_via_whatsapp)
        whatsapp_layout.addRow(self.send_whatsapp_button)

        return whatsapp_group

    #  Grupo Email
    def create_email_group(self):
        email_group = QGroupBox("Enviar Informe por Email")
        email_group.setStyleSheet(self.group_box_style())

        email_layout = QFormLayout(email_group)
        email_layout.setContentsMargins(10, 10, 10, 10)
        email_layout.setSpacing(10)

        self.email_to_input = QLineEdit()
        self.email_to_input.setStyleSheet(self.input_style())
        self.email_to_input.setPlaceholderText("Correo destinatario (ej: usuario@gmail.com)")
        email_layout.addRow("Para:", self.email_to_input)

        self.email_subject_input = QLineEdit()
        self.email_subject_input.setStyleSheet(self.input_style())
        self.email_subject_input.setPlaceholderText("Asunto del mensaje")
        email_layout.addRow("Asunto:", self.email_subject_input)

        self.email_body_text = QTextEdit()
        self.email_body_text.setStyleSheet(self.textedit_style())
        self.email_body_text.setPlaceholderText("Mensaje a enviar...")
        email_layout.addRow("Mensaje:", self.email_body_text)

        self.send_email_button = QPushButton(" Enviar por Email")
        self.send_email_button.setIcon(QIcon("icons/correo-electronico.png"))
        self.send_email_button.setStyleSheet(self.button_style("#3498DB"))
        self.send_email_button.clicked.connect(self.send_via_email)
        email_layout.addRow(self.send_email_button)

        return email_group

    def group_box_style(self):
        return """
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #2C3E50;
                border: 2px solid #2C3E50;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
            }
        """

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

    def button_style(self, base_color):
        darker_color = QColor(base_color).darker(110).name()
        return f"""
            QPushButton {{
                background-color: {base_color};
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {darker_color};
            }}
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

    #  Manejo de Combos
    def on_tipo_informe_changed(self):
        tipo = self.comboTipoInforme.currentText()
        self.comboId.clear()

        if tipo == "Cliente":
            all_clients = self.db_manager.get_all_clients()
            self.comboId.addItem("Seleccione un ID")
            for client in all_clients:
                self.comboId.addItem(client[0])  # ID_CLIENTE
        elif tipo == "Oportunidad":
            all_oportunidades = self.db_manager.get_all_oportunidades()
            self.comboId.addItem("Seleccione un ID")
            for opp in all_oportunidades:
                self.comboId.addItem(opp[0])
        elif tipo == "Presupuesto":
            all_presupuestos = self.db_manager.get_all_presupuestos()
            self.comboId.addItem("Seleccione un ID")
            for pre in all_presupuestos:
                self.comboId.addItem(pre[0])
        else:
            self.comboId.addItem("Seleccione un ID")

    def on_id_changed(self):
        tipo = self.comboTipoInforme.currentText()
        seleccion_id = self.comboId.currentText()
        if not seleccion_id or tipo == "Seleccione un tipo" or seleccion_id == "Seleccione un ID":
            return

        # Limpiar campos
        self.whatsapp_number_input.clear()
        self.email_to_input.clear()
        self.whatsapp_message_text.clear()
        self.email_body_text.clear()
        self.email_subject_input.clear()

        if tipo == "Cliente":
            data = self.db_manager.get_client_by_id(seleccion_id)
            if data:
                _, nombre, direccion, telefono, contacto, email = data
                self.whatsapp_number_input.setText(telefono)
                self.email_to_input.setText(email)

                mensaje = (
                    f"Hola {nombre},\n\n"
                    f"Te enviamos este informe de cliente.\n"
                    f"Dirección: {direccion}\n"
                    f"Persona contacto: {contacto}\n\n"
                    f"Saludos,\n{self.empresa_nombre}"
                )
                self.whatsapp_message_text.setText(mensaje)
                self.email_body_text.setText(mensaje)
                self.email_subject_input.setText(f"Informe para {nombre}")

        elif tipo == "Oportunidad":
            opp_data = self.db_manager.get_oportunidad_by_id(seleccion_id)
            if opp_data:
                id_opp, nom_opp, cliente_id, fecha, presupuesto, ingreso_esp, estado = opp_data
                client_data = self.db_manager.get_client_by_id(cliente_id)
                if client_data:
                    _, nombre_cli, _, telefono_cli, contacto_cli, email_cli = client_data
                    self.whatsapp_number_input.setText(telefono_cli)
                    self.email_to_input.setText(email_cli)

                    mensaje = (
                        f"Hola {nombre_cli},\n\n"
                        f"Te enviamos el informe de la oportunidad '{nom_opp}'.\n"
                        f"Fecha: {fecha}\nPresupuesto: {presupuesto}\n"
                        f"Ingreso Esperado: {ingreso_esp}\nEstado: {estado}\n\n"
                        f"Saludos,\n{self.empresa_nombre}"
                    )
                    self.whatsapp_message_text.setText(mensaje)
                    self.email_body_text.setText(mensaje)
                    self.email_subject_input.setText(f"Informe - Oportunidad {nom_opp}")

        elif tipo == "Presupuesto":
            pres_data = self.db_manager.get_presupuesto_by_id(seleccion_id)
            if pres_data:
                id_pre, nom_pre, cliente_id, fecha_cre, fecha_exp, subtot, total = pres_data
                client_data = self.db_manager.get_client_by_id(cliente_id)
                if client_data:
                    _, nombre_cli, _, telefono_cli, contacto_cli, email_cli = client_data
                    self.whatsapp_number_input.setText(telefono_cli)
                    self.email_to_input.setText(email_cli)

                    mensaje = (
                        f"Hola {nombre_cli},\n\n"
                        f"Adjuntamos el detalle del presupuesto '{nom_pre}'.\n"
                        f"Fecha de creación: {fecha_cre}\n"
                        f"Fecha de expiración: {fecha_exp}\n"
                        f"Subtotal: {subtot}\n"
                        f"Total: {total}\n\n"
                        f"Saludos,\n{self.empresa_nombre}"
                    )
                    self.whatsapp_message_text.setText(mensaje)
                    self.email_body_text.setText(mensaje)
                    self.email_subject_input.setText(f"Presupuesto {nom_pre}")

    #  Enviar por WhatsApp
    def send_via_whatsapp(self):
        phone_number = self.whatsapp_number_input.text().strip()
        message = self.whatsapp_message_text.toPlainText().strip()

        if phone_number and message:
            encoded_message = quote(message)
            url = f"https://api.whatsapp.com/send?phone={phone_number}&text={encoded_message}"
            webbrowser.open(url)
        else:
            self.show_message("Por favor, completa el número y el mensaje antes de enviar por WhatsApp.")

    #  Enviar por Email
    def send_via_email(self):
        email_to = self.email_to_input.text().strip()
        subject = self.email_subject_input.text().strip()
        body = self.email_body_text.toPlainText().strip()

        if email_to and subject and body:
            # Credenciales de envío
            cred = self.db_manager.get_company_credentials(self.empresa_nombre)
            if not cred:
                self.show_message("No se encontraron credenciales para el envío de correo.")
                return

            user, password = cred[0], cred[1]

            msg = MIMEMultipart()
            msg["From"] = user
            msg["To"] = email_to
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(user, password)
                server.send_message(msg)
                server.quit()
                self.show_message("Correo enviado correctamente.")
            except Exception as e:
                self.show_message(f"Error al enviar el correo: {str(e)}")
        else:
            self.show_message("Por favor, completa el destinatario, asunto y mensaje antes de enviar el correo.")

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

    def show_assistant(self):
        """
        Crea y muestra la burbuja asistente específica para MandarInformeView.
        """
        try:
            if self.assistant_bubble:
                self.assistant_bubble.close()
                self.assistant_bubble = None

            self.assistant_bubble = AssistantBubbleMandarInforme(self, self.assistant_button)
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
