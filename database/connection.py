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
        
        print("✓ Esquema de base de datos inicializado correctamente")
