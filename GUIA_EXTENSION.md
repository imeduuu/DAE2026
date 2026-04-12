"""
Guía Rápida - Cómo extender el proyecto

Este archivo contiene ejemplos de cómo agregar nuevas funcionalidades
siguiendo la arquitectura modular del proyecto.
"""

# ============================================================================
# 1. AGREGAR UN NUEVO SERVICIO
# ============================================================================
# Archivo: services/product_service.py

"""
from database.models import Product
from repositories.product_repository import ProductRepository
from typing import Optional, List

class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repo = product_repository
    
    def get_all_products(self) -> List[Product]:
        return self.product_repo.find_all()
    
    def create_product(self, name: str, price: float) -> Product:
        # Lógica de negocio aquí
        pass
"""

# Luego agregar en mediator/app_mediator.py:
"""
from services.product_service import ProductService

class AppMediator:
    def __init__(self, db_path: str = "data/orders.db"):
        # ... código existente ...
        
        # Agregar nuevo repositorio
        self.product_repository = ProductRepository(self.db_connection)
        
        # Agregar nuevo servicio
        self.product_service = ProductService(self.product_repository)
"""

# ============================================================================
# 2. AGREGAR UN NUEVO MODELO
# ============================================================================
# Archivo: database/models.py - Agregar al final:

"""
@dataclass
class Product:
    name: str
    price: float
    stock: int
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "created_at": self.created_at
        }
"""

# ============================================================================
# 3. AGREGAR UN NUEVO REPOSITORIO
# ============================================================================
# Archivo: repositories/product_repository.py

"""
from database.connection import DatabaseConnection
from database.models import Product
from typing import Optional, List

class ProductRepository:
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    def create(self, product: Product) -> Product:
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO products (name, price, stock)
                VALUES (?, ?, ?)
            """, (product.name, product.price, product.stock))
            product.id = cursor.lastrowid
            return product
    
    def find_all(self) -> List[Product]:
        with self.db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM products")
            rows = cursor.fetchall()
            return [self._row_to_product(row) for row in rows]
    
    def _row_to_product(self, row) -> Product:
        return Product(
            id=row["id"],
            name=row["name"],
            price=row["price"],
            stock=row["stock"],
            created_at=row["created_at"]
        )
"""

# ============================================================================
# 4. ACTUALIZAR EL ESQUEMA DE BASE DE DATOS
# ============================================================================
# Archivo: database/connection.py - En método _create_schema():

"""
def _create_schema(self, cursor: sqlite3.Cursor):
    # ... tablas existentes ...
    
    # Agregar nueva tabla
    cursor.execute(\"\"\"
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    \"\"\")
    
    print("✓ Esquema de base de datos actualizado")
"""

# ============================================================================
# 5. USAR EL MEDIADOR EN LA LÓGICA
# ============================================================================

"""
from mediator.app_mediator import AppMediator

mediator = AppMediator()

# Usar cualquier servicio desde el mediador
user_success, msg, user = mediator.auth_service.login("usuario", "pass")
products = mediator.product_service.get_all_products()
"""

# ============================================================================
# 6. AGREGAR VALIDACIONES PERSONALIZADAS
# ============================================================================
# Archivo: utils/validators.py - Agregar al final:

"""
def validate_product_price(price: float) -> Tuple[bool, str]:
    if price <= 0:
        return False, "El precio debe ser mayor a 0"
    if price > 999999:
        return False, "El precio es demasiado alto"
    return True, ""
"""

# ============================================================================
# 7. FLUJO DE CREACIÓN DE UNA NUEVA CARACTERÍSTICA
# ============================================================================
"""
1. Crear el modelo en database/models.py
2. Actualizar el esquema en database/connection.py
3. Crear el repositorio en repositories/
4. Crear el servicio en services/
5. Registrar en mediator/app_mediator.py
6. Usar desde main.py o GUI
7. Agregar validaciones en utils/validators.py si es necesario

Ejemplo completo: Agregar gestión de categorías
"""

# ============================================================================
# 8. MANEJO DE EXCEPCIONES
# ============================================================================

"""
try:
    with mediator.db_connection.get_cursor() as cursor:
        # Operación con BD
        pass
except ValueError as e:
    print(f"Error de validación: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")
"""

# ============================================================================
# RECORDAR
# ============================================================================
"""
✓ Mantener la lógica de negocio en services/
✓ Base de datos solo en database/ y repositories/
✓ Validaciones centralizadas en utils/
✓ Usar el mediador para acceder a los servicios
✓ Inyectar dependencias (no crear instancias dentro)
✓ Separar preocupaciones (responsabilidad única)
"""
