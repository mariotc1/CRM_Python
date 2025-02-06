from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QSizePolicy, QFrame, QMessageBox, QFormLayout, QLineEdit, QAction,
    QDialog, QSpinBox, QDoubleSpinBox, QHeaderView
)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QSize, pyqtSignal

from asistentes.burbujaAsistente_inventario import AssistantBubbleInventario


class InventarioView(QWidget):
    update_signal = pyqtSignal()

    def __init__(self, db_manager, empresa_nombre):
        super().__init__()
        self.db_manager = db_manager
        self.empresa_nombre = empresa_nombre
        self.db_manager.connect()
        self.assistant_bubble = None
        self.setContentsMargins(0, 0, 0, 0)
        self.init_ui()

    def init_ui(self):
        # Layout vertical principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1) ENCABEZADO SUPERIOR
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
        title_label = QLabel(f"Gestión de Inventario - {self.empresa_nombre}")
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

        # Añadir widgets al layout del header
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.assistant_button)

        # 2) CONTENEDOR CENTRAL
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
                padding: 20px;
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # 2.1) Tabla de Inventario
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Proveedor", "Nombre", "Descripción",
            "IVA (%)", "Precio", "Stock"
        ])
        self.load_inventory()
        self.table.setStyleSheet("""
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
        self.table.setAlternatingRowColors(True)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        content_layout.addWidget(self.table)

        # 2.2) Botones de Acción
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setSpacing(20)
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        # Botón "Añadir Producto"
        self.add_button = self.create_styled_button(
            "Añadir Producto", "#2ECC71", self.add_product, icon_path="icons/add.png"
        )

        # Botón "Editar Producto"
        self.edit_button = self.create_styled_button(
            "Editar Producto", "#F39C12", self.edit_product, icon_path="icons/edit.png"
        )

        # Botón "Eliminar Producto" (NUEVO)
        self.delete_button = self.create_styled_button(
            "Eliminar Producto", "#E74C3C", self.delete_product, icon_path="icons/delete.png"
        )

        # Botón "Actualizar"
        self.refresh_button = self.create_styled_button(
            "Actualizar", "#3498DB", self.refresh_table, icon_path="icons/refresh.png"
        )

        # Añadir Stretch para alinear los botones a la derecha
        buttons_layout.addStretch()

        # Añadir botones al layout en el orden deseado
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.refresh_button)

        content_layout.addWidget(buttons_frame)

        main_layout.addWidget(header_frame)
        main_layout.addWidget(content_frame)

        # Ajuste para que no se expanda de más la tabla
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def create_styled_button(self, text, color, callback, icon_path=None):
        button = QPushButton(text, self)
        button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
                text-align: left;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
        """)
        if icon_path:
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(20, 20))
            # Se vuelve a establecer el style para incluir el icono (opcional)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    padding: 10px 20px;
                    border-radius: 8px;
                    border: none;
                    text-align: left;
                    min-width: 120px;
                    icon-size: 20px 20px;
                }}
                QPushButton:hover {{
                    background-color: {self.darken_color(color)};
                }}
            """)
        button.clicked.connect(callback)
        return button

    # Método para oscurecer el color en hover
    def darken_color(self, color):
        c = QColor(color)
        h, s, v, a = c.getHsv()
        v = max(0, v - 30)
        c.setHsv(h, s, v, a)
        return c.name()

    def load_inventory(self):
        self.table.setRowCount(0)
        products = self.db_manager.get_all_products()
        self.table.setRowCount(len(products))
        for row, product in enumerate(products):
            for col, value in enumerate(product):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)

    def add_product(self):
        dialog = ProductDialog(self.db_manager)
        if dialog.exec_():
            self.refresh_table()
            self.update_signal.emit()

    def edit_product(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            self.show_message("Por favor, seleccione un producto para editar.")
            return

        row = selected_items[0].row()
        product_id = int(self.table.item(row, 0).text())
        product = self.db_manager.get_product(product_id)

        dialog = ProductDialog(self.db_manager, product)
        if dialog.exec_():
            self.refresh_table()
            self.update_signal.emit()

    def delete_product(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            self.show_message("Por favor, seleccione un producto para eliminar.")
            return

        row = selected_items[0].row()
        product_id = int(self.table.item(row, 0).text())

        confirm = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            "¿Está seguro de que desea eliminar el producto seleccionado?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                self.db_manager.delete_product(product_id)
                self.refresh_table()
                self.update_signal.emit()
            except Exception as e:
                self.show_message(f"Error al eliminar el producto: {str(e)}")

    def refresh_table(self):
        self.load_inventory()

    #  MENSAJES
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

    #  BURBUJA ASISTENTE
    def show_assistant(self):
        if self.assistant_bubble:
            self.assistant_bubble.close()
            self.assistant_bubble = None

        self.assistant_bubble = AssistantBubbleInventario(self, self.assistant_button)
        self.assistant_bubble.show()

    #  CERRAR BURBUJA ASISTENTE AL CERRAR LA VISTA
    def closeEvent(self, event):
        if self.assistant_bubble:
            self.assistant_bubble.close()
        event.accept()


#  DIÁLOGO PARA AÑADIR/EDITAR PRODUCTO
class ProductDialog(QDialog):
    def __init__(self, db_manager, product=None):
        super().__init__()
        self.db_manager = db_manager
        self.product = product
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Añadir/Editar Producto")
        self.setModal(True)

        # Layout vertical principal (espacio en blanco con esquinas redondeadas)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # -- Encabezado del diálogo --
        header_frame = QFrame()
        header_frame.setFixedHeight(60)
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #2C3E50;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 10, 10, 10)
        header_layout.setSpacing(10)

        header_label = QLabel("Producto")
        header_label.setStyleSheet("color: #ECF0F1;")
        header_label.setFont(QFont("Segoe UI", 16, QFont.Bold))

        header_layout.addWidget(header_label)
        header_layout.addStretch()

        # -- Contenido del diálogo (blanco) --
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }
        """)
        content_layout = QFormLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # Campos
        self.proveedor_input = self.create_input_with_icon("Proveedor", "icons/supplier_icon.png")
        self.nombre_input = self.create_input_with_icon("Nombre del Producto", "icons/product_icon.png")
        self.descripcion_input = self.create_input_with_icon("Descripción", "icons/description_icon.png")

        self.iva_input = QSpinBox()
        self.iva_input.setRange(0, 100)
        self.iva_input.setStyleSheet("""
            QSpinBox {
                padding: 6px;
                border: 2px solid #BDC3C7;
                border-radius: 5px;
                background-color: #ECF0F1;
            }
            QSpinBox:focus {
                border: 2px solid #3498DB;
                background-color: #FFFFFF;
            }
        """)
        self.precio_input = QDoubleSpinBox()
        self.precio_input.setRange(0, 1000000)
        self.precio_input.setDecimals(2)
        self.precio_input.setStyleSheet("""
            QDoubleSpinBox {
                padding: 6px;
                border: 2px solid #BDC3C7;
                border-radius: 5px;
                background-color: #ECF0F1;
            }
            QDoubleSpinBox:focus {
                border: 2px solid #3498DB;
                background-color: #FFFFFF;
            }
        """)
        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 1000000)
        self.stock_input.setStyleSheet("""
            QSpinBox {
                padding: 6px;
                border: 2px solid #BDC3C7;
                border-radius: 5px;
                background-color: #ECF0F1;
            }
            QSpinBox:focus {
                border: 2px solid #3498DB;
                background-color: #FFFFFF;
            }
        """)

        # Añadimos filas al formulario
        content_layout.addRow("Proveedor:", self.proveedor_input)
        content_layout.addRow("Nombre:", self.nombre_input)
        content_layout.addRow("Descripción:", self.descripcion_input)
        content_layout.addRow("IVA (%):", self.iva_input)
        content_layout.addRow("Precio:", self.precio_input)
        content_layout.addRow("Stock:", self.stock_input)

        # Botones (Guardar, Cancelar)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        save_button = QPushButton("Guardar")
        save_button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #2ECC71;
                color: white;
                padding: 8px 20px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #27AE60;
            }
        """)
        save_button.clicked.connect(self.save_product)

        cancel_button = QPushButton("Cancelar")
        cancel_button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                padding: 8px 20px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        cancel_button.clicked.connect(self.reject)

        btn_layout.addStretch()
        btn_layout.addWidget(save_button)
        btn_layout.addWidget(cancel_button)

        content_layout.addRow(btn_layout)

        # Montamos header y contenido en el layout vertical
        main_layout.addWidget(header_frame)
        main_layout.addWidget(content_frame)

        # Precargamos si es edición
        if self.product:
            self.load_product_data()

        # Fijamos dimensiones mínimas, para que sea un diálogo decente
        self.setMinimumWidth(400)

    #  CAMPOS CON ÍCONO
    def create_input_with_icon(self, placeholder, icon_path):
        inp = QLineEdit()
        inp.setPlaceholderText(placeholder)
        inp.setClearButtonEnabled(True)
        inp.setStyleSheet("""
            QLineEdit {
                padding: 6px 6px 6px 32px;
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
        # Añadir ícono como acción
        icon_action = QAction(QIcon(icon_path), "", inp)
        inp.addAction(icon_action, QLineEdit.LeadingPosition)
        return inp

    #  CARGAR DATOS DE PRODUCTO (si es edición)
    def load_product_data(self):
        # product = (id, proveedor, nombre, descripcion, iva, precio, stock)
        self.proveedor_input.setText(self.product[1])
        self.nombre_input.setText(self.product[2])
        self.descripcion_input.setText(self.product[3])
        self.iva_input.setValue(int(self.product[4]))
        self.precio_input.setValue(float(self.product[5]))
        self.stock_input.setValue(int(self.product[6]))

    #  GUARDAR/CERRAR
    def save_product(self):
        proveedor = self.proveedor_input.text()
        nombre = self.nombre_input.text()
        descripcion = self.descripcion_input.text()
        iva = self.iva_input.value()
        precio = self.precio_input.value()
        stock = self.stock_input.value()

        if not all([proveedor, nombre, descripcion]):
            self.show_message("Todos los campos son obligatorios.")
            return

        if self.product:
            # update
            try:
                self.db_manager.update_product(
                    self.product[0], proveedor, nombre, descripcion, iva, precio, stock
                )
                self.accept()
            except Exception as e:
                self.show_message(f"Error al actualizar el producto: {str(e)}")
        else:
            # insert
            try:
                self.db_manager.add_product(
                    proveedor, nombre, descripcion, iva, precio, stock
                )
                self.accept()
            except Exception as e:
                self.show_message(f"Error al guardar el producto: {str(e)}")

    #  MENSAJES
    def show_message(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Advertencia")
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