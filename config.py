"""
Configuración de la aplicación
Define las constantes y configuraciones globales
"""
import os
from pathlib import Path

# Rutas
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "orders.db"

# Base de datos
DB_PATH = str(DATABASE_PATH)

# Modos de ejecución
MODE_GUI = "gui"
MODE_CLI = "cli"

# Configuración de GUI
GUI_CONFIG = {
    "THEME": "dark",
    "WINDOW_WIDTH": 1000,
    "WINDOW_HEIGHT": 700,
    "APP_NAME": "Gestor de Pedidos",
    "APP_VERSION": "1.0.0"
}

# Configuración de aplicación
APP_CONFIG = {
    "debug": False,
    "log_level": "INFO"
}

# Crear directorios necesarios si no existen
DATA_DIR.mkdir(exist_ok=True)
