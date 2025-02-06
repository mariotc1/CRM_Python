import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        if not os.path.exists(self.db_name):
            print("La base de datos no existe, creando la base de datos y tablas...")
            self.create_db()
        else:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()

        self.check_tables()

    def create_db(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

        print("Creando las tablas...")

        # ======================================
        #  Tabla IDENTIFICACION
        # ======================================
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS IDENTIFICACION (
                NOMBRE_EMPRESA TEXT NOT NULL,
                MAIL TEXT NOT NULL,
                PASSWORD TEXT NOT NULL
            )
        """)

        # ======================================
        #  Tabla CLIENTES
        # ======================================
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS CLIENTES (
                ID_CLIENTE TEXT PRIMARY KEY,
                NOMBRE TEXT NOT NULL,
                DIRECCION TEXT NOT NULL,
                TELEFONO TEXT NOT NULL,
                PERSONA_CONTACTO TEXT NOT NULL,
                EMAIL TEXT NOT NULL
            )
        """)

        # ======================================
        #  Tabla OPORTUNIDADES
        # ======================================
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS OPORTUNIDADES (
                ID_OPORTUNIDAD TEXT PRIMARY KEY,
                NOMBRE_OPORTUNIDAD TEXT NOT NULL,
                CLIENTE TEXT NOT NULL,
                FECHA DATE NOT NULL,
                PRESUPUESTO TEXT NOT NULL,
                INGRESO_ESPERADO REAL NOT NULL,
                ESTADO TEXT NOT NULL,
                FOREIGN KEY (CLIENTE) REFERENCES CLIENTES(ID_CLIENTE)
            )
        """)

        # ======================================
        #  Tabla PRESUPUESTOS
        # ======================================
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS PRESUPUESTOS (
                ID_PRESUPUESTO TEXT PRIMARY KEY,
                NOMBRE TEXT NOT NULL,
                CLIENTE TEXT NOT NULL,
                FECHA_CREACION DATE NOT NULL,
                FECHA_EXPIRACION DATE NOT NULL,
                SUBTOTAL REAL NOT NULL,
                TOTAL REAL NOT NULL,
                FOREIGN KEY (CLIENTE) REFERENCES CLIENTES(ID_CLIENTE)
            )
        """)

        # ======================================
        #  Tabla PRODUCTOS
        # ======================================
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS PRODUCTOS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proveedor TEXT NOT NULL,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                iva INTEGER NOT NULL,
                precio REAL NOT NULL,
                stock INTEGER NOT NULL
            )
        """)

        # ======================================
        #  Tabla PERFIL  (NUEVA)
        # ======================================
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS PERFIL (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOMBRE_EMPRESA TEXT NOT NULL,
                NOMBRE_USUARIO TEXT,
                MAIL TEXT,
                PASSWORD TEXT,
                FOTO_PATH TEXT,
                DESCRIPCION TEXT,
                FOREIGN KEY (NOMBRE_EMPRESA) REFERENCES IDENTIFICACION(NOMBRE_EMPRESA)
            )
        """)

        self.connection.commit()
        print("Tablas creadas correctamente.")

    def check_tables(self):
        """Verifica que las tablas estén creadas; si no, las crea."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in self.cursor.fetchall()]
        print(f"Tablas en la base de datos: {tables}")

        # Verificación y creación de CLIENTES
        if 'CLIENTES' not in tables:
            print("La tabla CLIENTES no existe. Creando tabla...")
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS CLIENTES (
                    ID_CLIENTE TEXT PRIMARY KEY,
                    NOMBRE TEXT NOT NULL,
                    DIRECCION TEXT NOT NULL,
                    TELEFONO TEXT NOT NULL,
                    PERSONA_CONTACTO TEXT NOT NULL,
                    EMAIL TEXT NOT NULL
                )
            """)
            self.connection.commit()
            print("Tabla CLIENTES creada.")

        # Verificación y creación de IDENTIFICACION
        if 'IDENTIFICACION' not in tables:
            print("La tabla IDENTIFICACION no existe. Creando tabla...")
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS IDENTIFICACION (
                    NOMBRE_EMPRESA TEXT NOT NULL,
                    MAIL TEXT NOT NULL,
                    PASSWORD TEXT NOT NULL
                )
            """)
            self.connection.commit()
            print("Tabla IDENTIFICACION creada.")

        # Verificación y creación de OPORTUNIDADES
        if 'OPORTUNIDADES' not in tables:
            print("La tabla OPORTUNIDADES no existe. Creando tabla...")
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS OPORTUNIDADES (
                    ID_OPORTUNIDAD TEXT PRIMARY KEY,
                    NOMBRE_OPORTUNIDAD TEXT NOT NULL,
                    CLIENTE TEXT NOT NULL,
                    FECHA DATE NOT NULL,
                    PRESUPUESTO TEXT NOT NULL,
                    INGRESO_ESPERADO REAL NOT NULL,
                    ESTADO TEXT NOT NULL,
                    FOREIGN KEY (CLIENTE) REFERENCES CLIENTES(ID_CLIENTE)
                )
            """)
            self.connection.commit()
            print("Tabla OPORTUNIDADES creada.")

        # Verificación y creación de PRESUPUESTOS
        if 'PRESUPUESTOS' not in tables:
            print("La tabla PRESUPUESTOS no existe. Creando tabla...")
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS PRESUPUESTOS (
                    ID_PRESUPUESTO TEXT PRIMARY KEY,
                    NOMBRE TEXT NOT NULL,
                    CLIENTE TEXT NOT NULL,
                    FECHA_CREACION DATE NOT NULL,
                    FECHA_EXPIRACION DATE NOT NULL,
                    SUBTOTAL REAL NOT NULL,
                    TOTAL REAL NOT NULL,
                    FOREIGN KEY (CLIENTE) REFERENCES CLIENTES(ID_CLIENTE)
                )
            """)
            self.connection.commit()
            print("Tabla PRESUPUESTOS creada.")

        # Verificación y creación de PRODUCTOS
        if 'PRODUCTOS' not in tables:
            print("La tabla PRODUCTOS no existe. Creando tabla...")
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS PRODUCTOS (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    proveedor TEXT NOT NULL,
                    nombre TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    iva INTEGER NOT NULL,
                    precio REAL NOT NULL,
                    stock INTEGER NOT NULL
                )
            """)
            self.connection.commit()
            print("Tabla PRODUCTOS creada.")

        # Verificación y creación de PERFIL
        if 'PERFIL' not in tables:
            print("La tabla PERFIL no existe. Creando tabla...")
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS PERFIL (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NOMBRE_EMPRESA TEXT NOT NULL,
                    NOMBRE_USUARIO TEXT,
                    MAIL TEXT,
                    PASSWORD TEXT,
                    FOTO_PATH TEXT,
                    DESCRIPCION TEXT,
                    FOREIGN KEY (NOMBRE_EMPRESA) REFERENCES IDENTIFICACION(NOMBRE_EMPRESA)
                )
            """)
            self.connection.commit()
            print("Tabla PERFIL creada.")

        # Verificación y creación de TAREAS
        if 'TAREAS' not in tables:
            print("La tabla TAREAS no existe. Creando tabla...")
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS TAREAS (
                    ID_TAREA TEXT PRIMARY KEY,
                    TITULO TEXT NOT NULL,
                    DESCRIPCION TEXT,
                    FECHA_CREACION DATE NOT NULL,
                    FECHA_VENCIMIENTO DATE,
                    ASIGNADO_A TEXT,
                    PRIORIDAD TEXT,
                    ESTADO TEXT
                )
            """)
            self.connection.commit()
            print("Tabla TAREAS creada.")
            
        if 'EVENTOS' not in tables:
            print("La tabla EVENTOS no existe. Creando tabla...")
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS EVENTOS (
                    ID_EVENTO TEXT PRIMARY KEY,
                    TITULO TEXT NOT NULL,
                    FECHA DATE NOT NULL,
                    HORA TEXT NOT NULL,
                    LUGAR TEXT,
                    DESCRIPCION TEXT,
                    ASIGNADO_A TEXT
                )
            """)
            self.connection.commit()
            print("Tabla EVENTOS creada.")
            
        if 'FAQ' not in tables:
            print("La tabla FAQ no existe. Creando tabla...")
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS FAQ (
                    ID_FAQ TEXT PRIMARY KEY,
                    PREGUNTA TEXT NOT NULL,
                    RESPUESTA TEXT NOT NULL,
                    CATEGORIA TEXT,
                    ULTIMA_ACTUALIZACION DATE
                )
            """)
            self.connection.commit()
            print("Tabla FAQ creada.")

    #   MÉTODOS GENÉRICOS
    def execute_query(self, query, params=()):
        """Ejecuta una consulta que no devuelve resultados (INSERT, UPDATE, DELETE)."""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error al ejecutar la consulta: {e}")

    def execute_read_query(self, query, params=()):
        """Ejecuta una consulta que devuelve resultados (SELECT)."""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al ejecutar la consulta de lectura: {e}")
            return []

    def close(self):
        if self.connection:
            self.connection.close()

    #   IDENTIFICACION
    def insert_empresa(self, nombre, mail, password):
        try:
            self.cursor.execute("""
                INSERT INTO IDENTIFICACION (NOMBRE_EMPRESA, MAIL, PASSWORD)
                VALUES (?, ?, ?)
            """, (nombre, mail, password))
            self.connection.commit()
        except Exception as e:
            print(f"Error al insertar la empresa: {str(e)}")

    def check_company_exists(self, nombre_empresa):
        self.cursor.execute("""
            SELECT * FROM IDENTIFICACION WHERE NOMBRE_EMPRESA = ?
        """, (nombre_empresa,))
        result = self.cursor.fetchone()
        return (result is not None)

    def check_login(self, mail, password, nombre_empresa):
        self.cursor.execute("""
            SELECT * FROM IDENTIFICACION WHERE MAIL = ? AND PASSWORD = ? AND NOMBRE_EMPRESA = ?
        """, (mail, password, nombre_empresa))
        result = self.cursor.fetchone()
        return (result is not None)

    def get_company_credentials(self, nombre_empresa):
        """
        Retorna (MAIL, PASSWORD) para la empresa dada.
        """
        self.cursor.execute("""
            SELECT MAIL, PASSWORD 
            FROM IDENTIFICACION
            WHERE NOMBRE_EMPRESA = ?
        """, (nombre_empresa,))
        return self.cursor.fetchone()  # (mail, password) o None

    #   PERFIL 
    def get_user_profile(self, nombre_empresa):
        """
        Devuelve la fila de PERFIL para esa empresa, o None si no existe.
        Estructura: (ID, NOMBRE_EMPRESA, NOMBRE_USUARIO, MAIL, PASSWORD, FOTO_PATH, DESCRIPCION)
        """
        self.cursor.execute("SELECT * FROM PERFIL WHERE NOMBRE_EMPRESA = ?", (nombre_empresa,))
        return self.cursor.fetchone()

    def update_user_profile(self, empresa, nombre, correo, password, descripcion, photo_path):
        """
        Inserta o actualiza la fila en PERFIL asociada a la empresa dada.
        - nombre se guardará en NOMBRE_USUARIO
        - correo en MAIL
        - password en PASSWORD
        - photo_path en FOTO_PATH
        - descripcion en DESCRIPCION
        """
        # Primero vemos si ya existe registro en PERFIL
        self.cursor.execute("SELECT ID FROM PERFIL WHERE NOMBRE_EMPRESA = ?", (empresa,))
        row = self.cursor.fetchone()

        if row:
            # UPDATE
            perfil_id = row[0]
            try:
                self.cursor.execute("""
                    UPDATE PERFIL
                    SET NOMBRE_USUARIO = ?,
                        MAIL = ?,
                        PASSWORD = ?,
                        FOTO_PATH = ?,
                        DESCRIPCION = ?
                    WHERE ID = ?
                """, (nombre, correo, password, photo_path, descripcion, perfil_id))
                self.connection.commit()
            except Exception as e:
                print(f"Error al actualizar el perfil: {str(e)}")
        else:
            # INSERT
            try:
                self.cursor.execute("""
                    INSERT INTO PERFIL (NOMBRE_EMPRESA, NOMBRE_USUARIO, MAIL, PASSWORD, FOTO_PATH, DESCRIPCION)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (empresa, nombre, correo, password, photo_path, descripcion))
                self.connection.commit()
            except Exception as e:
                print(f"Error al insertar el perfil: {str(e)}")

    #   CLIENTES
    def insert_cliente(self, id_cliente, nombre, direccion, telefono, persona_contacto, email):
        try:
            self.cursor.execute("""
                INSERT INTO CLIENTES (ID_CLIENTE, NOMBRE, DIRECCION, TELEFONO, PERSONA_CONTACTO, EMAIL)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (id_cliente, nombre, direccion, telefono, persona_contacto, email))
            self.connection.commit()
        except Exception as e:
            print(f"Error al insertar el cliente: {str(e)}")

    def get_all_clients(self):
        self.cursor.execute("SELECT * FROM CLIENTES")
        return self.cursor.fetchall()

    def get_client_by_id(self, id_cliente):
        self.cursor.execute("SELECT * FROM CLIENTES WHERE ID_CLIENTE = ?", (id_cliente,))
        return self.cursor.fetchone()

    def update_cliente(self, id_cliente, nombre, direccion, telefono, persona_contacto, email):
        self.cursor.execute("""
            UPDATE CLIENTES SET 
            NOMBRE = ?, DIRECCION = ?, TELEFONO = ?, PERSONA_CONTACTO = ?, EMAIL = ?
            WHERE ID_CLIENTE = ?
        """, (nombre, direccion, telefono, persona_contacto, email, id_cliente))
        self.connection.commit()

    def delete_cliente(self, id_cliente):
        self.cursor.execute("DELETE FROM CLIENTES WHERE ID_CLIENTE = ?", (id_cliente,))
        self.connection.commit()
    
    def get_client_name_by_id(self, id_cliente):
        """
        Devuelve el nombre del cliente dado su ID.
        """
        self.cursor.execute("SELECT NOMBRE FROM CLIENTES WHERE ID_CLIENTE = ?", (id_cliente,))
        result = self.cursor.fetchone()
        return result[0] if result else "Desconocido"

    #   OPORTUNIDADES
    def insert_oportunidad(self, id_oportunidad, nombre_oportunidad, cliente, fecha, presupuesto, ingreso_esperado, estado):
        try:
            self.cursor.execute("""
                INSERT INTO OPORTUNIDADES (ID_OPORTUNIDAD, NOMBRE_OPORTUNIDAD, CLIENTE, FECHA, PRESUPUESTO, INGRESO_ESPERADO, ESTADO)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (id_oportunidad, nombre_oportunidad, cliente, fecha, presupuesto, ingreso_esperado, estado))
            self.connection.commit()
        except Exception as e:
            print(f"Error al insertar la oportunidad: {str(e)}")

    def get_all_oportunidades(self):
        self.cursor.execute("SELECT * FROM OPORTUNIDADES")
        return self.cursor.fetchall()

    def get_oportunidad_by_id(self, id_oportunidad):
        self.cursor.execute("SELECT * FROM OPORTUNIDADES WHERE ID_OPORTUNIDAD = ?", (id_oportunidad,))
        return self.cursor.fetchone()

    def update_oportunidad(self, id_oportunidad, nombre_oportunidad, cliente, fecha, presupuesto, ingreso_esperado, estado):
        self.cursor.execute("""
            UPDATE OPORTUNIDADES SET 
            NOMBRE_OPORTUNIDAD = ?, CLIENTE = ?, FECHA = ?, PRESUPUESTO = ?, INGRESO_ESPERADO = ?, ESTADO = ?
            WHERE ID_OPORTUNIDAD = ?
        """, (nombre_oportunidad, cliente, fecha, presupuesto, ingreso_esperado, estado, id_oportunidad))
        self.connection.commit()

    def delete_oportunidad(self, id_oportunidad):
        self.cursor.execute("DELETE FROM OPORTUNIDADES WHERE ID_OPORTUNIDAD = ?", (id_oportunidad,))
        self.connection.commit()

    #   PRESUPUESTOS
    def insert_presupuesto(self, id_presupuesto, nombre, cliente, fecha_creacion, fecha_expiracion, subtotal, total):
        self.cursor.execute("""
            INSERT INTO PRESUPUESTOS (ID_PRESUPUESTO, NOMBRE, CLIENTE, FECHA_CREACION, FECHA_EXPIRACION, SUBTOTAL, TOTAL)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (id_presupuesto, nombre, cliente, fecha_creacion, fecha_expiracion, subtotal, total))
        self.connection.commit()

    def update_presupuesto(self, id_presupuesto, nombre, cliente, fecha_creacion, fecha_expiracion, subtotal, total):
        self.cursor.execute("""
            UPDATE PRESUPUESTOS SET 
            NOMBRE = ?, CLIENTE = ?, FECHA_CREACION = ?, FECHA_EXPIRACION = ?, SUBTOTAL = ?, TOTAL = ?
            WHERE ID_PRESUPUESTO = ?
        """, (nombre, cliente, fecha_creacion, fecha_expiracion, subtotal, total, id_presupuesto))
        self.connection.commit()

    def delete_presupuesto(self, id_presupuesto):
        self.cursor.execute("DELETE FROM PRESUPUESTOS WHERE ID_PRESUPUESTO = ?", (id_presupuesto,))
        self.connection.commit()

    def get_all_presupuestos(self):
        self.cursor.execute("SELECT * FROM PRESUPUESTOS")
        return self.cursor.fetchall()

    def get_presupuesto_by_id(self, id_presupuesto):
        self.cursor.execute("SELECT * FROM PRESUPUESTOS WHERE ID_PRESUPUESTO = ?", (id_presupuesto,))
        return self.cursor.fetchone()

    #   PRODUCTOS
    def add_product(self, proveedor, nombre, descripcion, iva, precio, stock):
        query = """INSERT INTO PRODUCTOS (proveedor, nombre, descripcion, iva, precio, stock)
                   VALUES (?, ?, ?, ?, ?, ?)"""
        self.execute_query(query, (proveedor, nombre, descripcion, iva, precio, stock))

    def get_all_products(self):
        query = "SELECT * FROM PRODUCTOS"
        return self.execute_read_query(query)

    def get_product(self, product_id):
        query = "SELECT * FROM PRODUCTOS WHERE id = ?"
        result = self.execute_read_query(query, (product_id,))
        if result:
            return result[0]
        return None

    def update_product(self, product_id, proveedor, nombre, descripcion, iva, precio, stock):
        query = """UPDATE PRODUCTOS
                   SET proveedor = ?, nombre = ?, descripcion = ?, iva = ?, precio = ?, stock = ?
                   WHERE id = ?"""
        self.execute_query(query, (proveedor, nombre, descripcion, iva, precio, stock, product_id))

    def delete_product(self, product_id):
        query = "DELETE FROM PRODUCTOS WHERE id = ?"
        self.execute_query(query, (product_id,))

    #   PIPELINE / ETAPAS
    def get_all_opportunities(self):
        """
        Devuelve las oportunidades con un subset de columnas
        para el Pipeline (ID_OPORTUNIDAD, CLIENTE, INGRESO_ESPERADO, ESTADO).
        """
        self.cursor.execute("SELECT ID_OPORTUNIDAD, CLIENTE, INGRESO_ESPERADO, ESTADO FROM OPORTUNIDADES")
        return self.cursor.fetchall()

    def update_opportunity_stage(self, opportunity_id, new_stage):
        self.cursor.execute(
            "UPDATE OPORTUNIDADES SET ESTADO = ? WHERE ID_OPORTUNIDAD = ?",
            (new_stage, opportunity_id)
        )
        self.connection.commit()

    #   TAREAS
    def insert_tarea(self, id_tarea, titulo, descripcion, fecha_creacion, fecha_vencimiento, asignado_a, prioridad, estado):
        try:
            self.cursor.execute("""
                INSERT INTO TAREAS (ID_TAREA, TITULO, DESCRIPCION, FECHA_CREACION, FECHA_VENCIMIENTO, ASIGNADO_A, PRIORIDAD, ESTADO)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (id_tarea, titulo, descripcion, fecha_creacion, fecha_vencimiento, asignado_a, prioridad, estado))
            self.connection.commit()
        except Exception as e:
            print(f"Error al insertar la tarea: {str(e)}")

    def get_all_tareas(self):
        self.cursor.execute("SELECT * FROM TAREAS")
        return self.cursor.fetchall()

    def get_tarea_by_id(self, id_tarea):
        self.cursor.execute("SELECT * FROM TAREAS WHERE ID_TAREA = ?", (id_tarea,))
        return self.cursor.fetchone()

    def update_tarea(self, id_tarea, titulo, descripcion, fecha_creacion, fecha_vencimiento, asignado_a, prioridad, estado):
        self.cursor.execute("""
            UPDATE TAREAS
            SET TITULO = ?, DESCRIPCION = ?, FECHA_CREACION = ?, FECHA_VENCIMIENTO = ?, 
                ASIGNADO_A = ?, PRIORIDAD = ?, ESTADO = ?
            WHERE ID_TAREA = ?
        """, (titulo, descripcion, fecha_creacion, fecha_vencimiento, asignado_a, prioridad, estado, id_tarea))
        self.connection.commit()

    def delete_tarea(self, id_tarea):
        self.cursor.execute("DELETE FROM TAREAS WHERE ID_TAREA = ?", (id_tarea,))
        self.connection.commit()
        
    def insert_evento(self, id_evento, titulo, fecha, hora, lugar, descripcion, asignado_a):
        try:
            self.cursor.execute("""
                INSERT INTO EVENTOS (ID_EVENTO, TITULO, FECHA, HORA, LUGAR, DESCRIPCION, ASIGNADO_A)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (id_evento, titulo, fecha, hora, lugar, descripcion, asignado_a))
            self.connection.commit()
        except Exception as e:
            print(f"Error al insertar el evento: {str(e)}")

    #   EVENTOS
    def get_all_eventos(self):
        # Retorna todos los eventos
        self.cursor.execute("SELECT * FROM EVENTOS")
        return self.cursor.fetchall()

    def get_eventos_por_fecha(self, fecha_str):
        query = """
            SELECT ID_EVENTO, TITULO, FECHA, HORA, LUGAR, DESCRIPCION, ASIGNADO_A 
            FROM EVENTOS 
            WHERE FECHA = ?
        """
        try:
            self.cursor.execute(query, (fecha_str,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener eventos por fecha: {e}")
            return []

    def get_evento_by_id(self, id_evento):
        self.cursor.execute("SELECT * FROM EVENTOS WHERE ID_EVENTO = ?", (id_evento,))
        return self.cursor.fetchone()

    def update_evento(self, id_evento, titulo, fecha, hora, lugar, descripcion, asignado_a):
        self.cursor.execute("""
            UPDATE EVENTOS
            SET TITULO = ?, FECHA = ?, HORA = ?, LUGAR = ?, DESCRIPCION = ?, ASIGNADO_A = ?
            WHERE ID_EVENTO = ?
        """, (titulo, fecha, hora, lugar, descripcion, asignado_a, id_evento))
        self.connection.commit()

    def delete_evento(self, id_evento):
        self.cursor.execute("DELETE FROM EVENTOS WHERE ID_EVENTO = ?", (id_evento,))
        self.connection.commit()

    #   TAREAS
    def insert_faq(self, id_faq, pregunta, respuesta, categoria, ultima_act):
        try:
            self.cursor.execute("""
                INSERT INTO FAQ (ID_FAQ, PREGUNTA, RESPUESTA, CATEGORIA, ULTIMA_ACTUALIZACION)
                VALUES (?, ?, ?, ?, ?)
            """, (id_faq, pregunta, respuesta, categoria, ultima_act))
            self.connection.commit()
        except Exception as e:
            print(f"Error al insertar la FAQ: {str(e)}")

    def get_all_faqs(self):
        self.cursor.execute("SELECT * FROM FAQ")
        return self.cursor.fetchall()

    def search_faqs_by_keyword(self, keyword):
        # Busca pregunta o respuesta que contenga la palabra clave en PREGUNTA o RESPUESTA
        search_pattern = f"%{keyword}%"
        self.cursor.execute("""
            SELECT * FROM FAQ
            WHERE PREGUNTA LIKE ? OR RESPUESTA LIKE ?
        """, (search_pattern, search_pattern))
        return self.cursor.fetchall()

    def get_faq_by_id(self, id_faq):
        self.cursor.execute("SELECT * FROM FAQ WHERE ID_FAQ = ?", (id_faq,))
        return self.cursor.fetchone()

    def update_faq(self, id_faq, pregunta, respuesta, categoria, ultima_act):
        self.cursor.execute("""
            UPDATE FAQ
            SET PREGUNTA = ?, RESPUESTA = ?, CATEGORIA = ?, ULTIMA_ACTUALIZACION = ?
            WHERE ID_FAQ = ?
        """, (pregunta, respuesta, categoria, ultima_act, id_faq))
        self.connection.commit()

    def delete_faq(self, id_faq):
        self.cursor.execute("DELETE FROM FAQ WHERE ID_FAQ = ?", (id_faq,))
        self.connection.commit()

    # Oportunidades
    def get_oportunidades_por_fecha(self, fecha_str):
        query = "SELECT id_oportunidad, nombre, fecha_asignada, lugar, descripcion, asignado_a FROM oportunidades WHERE fecha_asignada = ?"
        self.cursor.execute(query, (fecha_str,))
        return self.cursor.fetchall()

    def get_oportunidad(self, id_oportunidad):
        query = "SELECT id_oportunidad, nombre, fecha_asignada, lugar, descripcion, asignado_a FROM oportunidades WHERE id_oportunidad = ?"
        self.cursor.execute(query, (id_oportunidad,))
        return self.cursor.fetchone()

    # Presupuestos
    def get_presupuestos_por_fecha(self, fecha_str):
        query = "SELECT id_presupuesto, nombre, fecha_creacion, fecha_expiracion FROM presupuestos WHERE fecha_expiracion = ?"
        self.cursor.execute(query, (fecha_str,))
        return self.cursor.fetchall()

    def get_presupuesto(self, id_presupuesto):
        query = "SELECT id_presupuesto, nombre, fecha_creacion, fecha_expiracion FROM presupuestos WHERE id_presupuesto = ?"
        self.cursor.execute(query, (id_presupuesto,))
        return self.cursor.fetchone()

    # Tareas
    def get_tareas_por_fecha(self, fecha_str):
        query = "SELECT id_tarea, nombre, fecha_vencimiento, hora_vencimiento, lugar, descripcion, asignado_a FROM tareas WHERE fecha_vencimiento = ?"
        self.cursor.execute(query, (fecha_str,))
        return self.cursor.fetchall()

    def get_tarea(self, id_tarea):
        query = "SELECT id_tarea, nombre, fecha_vencimiento, hora_vencimiento, lugar, descripcion, asignado_a FROM tareas WHERE id_tarea = ?"
        self.cursor.execute(query, (id_tarea,))
        return self.cursor.fetchone()