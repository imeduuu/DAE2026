"""
Módulo de conexión a base de datos SQLite
Gestiona la conexión y la creación del esquema
"""
import sqlite3
import os
from contextlib import contextmanager
from typing import Iterator


class DatabaseConnection:
    """Clase para gestionar la conexión a SQLite"""
    
    def __init__(self, db_path: str = "data/orders.db"):
        """
        Inicializa la conexión a la base de datos
        
        Args:
            db_path: Ruta del archivo de base de datos
        """
        self.db_path = db_path
        self._ensure_db_directory()
        self._initialize_schema()
    
    def _ensure_db_directory(self):
        """Crea el directorio de datos si no existe"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Obtiene una conexión a la base de datos
        
        Returns:
            sqlite3.Connection: Conexión activa a la BD
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
        return conn
    
    @contextmanager
    def get_cursor(self) -> Iterator[sqlite3.Cursor]:
        """
        Context manager para obtener un cursor
        
        Yields:
            sqlite3.Cursor: Cursor para ejecutar comandos SQL
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _initialize_schema(self):
        """Inicializa el esquema de la base de datos en la primera ejecución"""
        try:
            with self.get_cursor() as cursor:
                # Verificar si las tablas ya existen
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
                )
                if not cursor.fetchone():
                    # Crear tablas
                    self._create_schema(cursor)
        except Exception as e:
            print(f"Error al inicializar esquema: {e}")
            raise
    
    def _create_schema(self, cursor: sqlite3.Cursor):
        """Crea el esquema de las tablas"""
        
        # Tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'cliente',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de categorías de productos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT
            )
        """)
        
        # Tabla de productos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                model TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                description TEXT,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)
        
        # Tabla de pedidos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pendiente',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Tabla de items en pedidos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)
        
        # Insertar datos iniciales de categorías y productos
        self._insert_initial_products(cursor)
        
        print("✓ Esquema de base de datos inicializado correctamente")
    
    def _insert_initial_products(self, cursor: sqlite3.Cursor):
        """Inserta categorías y productos iniciales"""
        # Verificar si ya hay categorías
        cursor.execute("SELECT COUNT(*) FROM categories")
        if cursor.fetchone()[0] > 0:
            return
        
        # Categorías
        categories = [
            ("Computadoras", "PCs de escritorio y portátiles"),
            ("Placas Base", "Motherboards para diferentes plataformas"),
            ("Procesadores", "CPUs Intel y AMD"),
            ("Tarjetas Gráficas", "GPUs NVIDIA y AMD"),
            ("Memoria RAM", "Módulos de RAM DDR4 y DDR5"),
            ("Almacenamiento", "SSDs y HDDs"),
            ("Periféricos", "Teclados, ratones, monitores"),
            ("Accesorios", "Cables, adaptadores, soportes"),
        ]
        
        for cat_name, cat_desc in categories:
            cursor.execute(
                "INSERT INTO categories (name, description) VALUES (?, ?)",
                (cat_name, cat_desc)
            )
        
        # Obtener IDs de categorías
        cursor.execute("SELECT id, name FROM categories")
        cat_map = {row[1]: row[0] for row in cursor.fetchall()}
        
        # Productos
        products = [
            # Computadoras
            (cat_map["Computadoras"], "PC Gamer High-End", "RTX 4090 Edition", 3500.00, 5),
            (cat_map["Computadoras"], "PC Profesional", "Workstation", 2800.00, 3),
            (cat_map["Computadoras"], "Laptop Gaming", "ASUS ROG", 2200.00, 8),
            
            # Placas Base
            (cat_map["Placas Base"], "Motherboard AM5", "ASUS ROG STRIX", 450.00, 12),
            (cat_map["Placas Base"], "Motherboard LGA1700", "GIGABYTE Z790", 480.00, 10),
            
            # Procesadores
            (cat_map["Procesadores"], "CPU Intel", "Intel i9-13900K", 680.00, 7),
            (cat_map["Procesadores"], "CPU AMD", "Ryzen 9 7950X", 650.00, 9),
            (cat_map["Procesadores"], "CPU AMD", "Ryzen 5 7600X", 280.00, 15),
            
            # Tarjetas Gráficas
            (cat_map["Tarjetas Gráficas"], "GPU NVIDIA", "RTX 4090", 1600.00, 4),
            (cat_map["Tarjetas Gráficas"], "GPU NVIDIA", "RTX 4070", 850.00, 8),
            (cat_map["Tarjetas Gráficas"], "GPU NVIDIA", "RTX 4060", 350.00, 20),
            (cat_map["Tarjetas Gráficas"], "GPU AMD", "RX 7900 XTX", 900.00, 6),
            
            # Memoria RAM
            (cat_map["Memoria RAM"], "RAM DDR5", "Corsair 32GB 6000MHz", 180.00, 25),
            (cat_map["Memoria RAM"], "RAM DDR5", "Kingston 16GB 5800MHz", 95.00, 30),
            (cat_map["Memoria RAM"], "RAM DDR4", "G.Skill 16GB 3600MHz", 75.00, 40),
            
            # Almacenamiento
            (cat_map["Almacenamiento"], "SSD NVMe", "Samsung 980 Pro 1TB", 120.00, 20),
            (cat_map["Almacenamiento"], "SSD NVMe", "WD Black 2TB", 180.00, 15),
            (cat_map["Almacenamiento"], "HDD", "Seagate 4TB", 90.00, 10),
            
            # Periféricos
            (cat_map["Periféricos"], "Monitor", "LG 27\" 144Hz IPS", 400.00, 5),
            (cat_map["Periféricos"], "Teclado Gaming", "Corsair K95", 200.00, 12),
            (cat_map["Periféricos"], "Micrófono", "Blue Yeti", 120.00, 18),
        ]
        
        for cat_id, name, model, price, stock in products:
            cursor.execute(
                """INSERT INTO products (category_id, name, model, price, stock)
                   VALUES (?, ?, ?, ?, ?)""",
                (cat_id, name, model, price, stock)
            )
