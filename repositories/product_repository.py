"""
Repositorio de Productos
Gestiona el acceso a datos de categorías y productos
"""
from typing import List, Optional, Dict, Any
from database.models import Category, Product, OrderItem
from database.connection import DatabaseConnection


class ProductRepository:
    """Repositorio para operaciones CRUD de productos"""
    
    def __init__(self, db_connection: DatabaseConnection):
        """
        Inicializa el repositorio
        
        Args:
            db_connection: Instancia de conexión a BD
        """
        self.db = db_connection
    
    # ============ CATEGORÍAS ============
    
    def find_all_categories(self) -> List[Category]:
        """Obtiene todas las categorías"""
        with self.db.get_cursor() as cursor:
            cursor.execute("SELECT id, name, description FROM categories ORDER BY name")
            return [
                Category(
                    id=row[0],
                    name=row[1],
                    description=row[2]
                )
                for row in cursor.fetchall()
            ]
    
    def find_category_by_id(self, category_id: int) -> Optional[Category]:
        """Obtiene una categoría por ID"""
        with self.db.get_cursor() as cursor:
            cursor.execute(
                "SELECT id, name, description FROM categories WHERE id = ?",
                (category_id,)
            )
            row = cursor.fetchone()
            if row:
                return Category(id=row[0], name=row[1], description=row[2])
            return None
    
    # ============ PRODUCTOS ============
    
    def find_all_products(self) -> List[Product]:
        """Obtiene todos los productos"""
        with self.db.get_cursor() as cursor:
            cursor.execute(
                """SELECT id, category_id, name, model, price, stock, description 
                   FROM products ORDER BY category_id, name"""
            )
            return [
                Product(
                    id=row[0],
                    category_id=row[1],
                    name=row[2],
                    model=row[3],
                    price=row[4],
                    stock=row[5],
                    description=row[6]
                )
                for row in cursor.fetchall()
            ]
    
    def find_products_by_category(self, category_id: int) -> List[Product]:
        """Obtiene productos de una categoría específica"""
        with self.db.get_cursor() as cursor:
            cursor.execute(
                """SELECT id, category_id, name, model, price, stock, description 
                   FROM products WHERE category_id = ? ORDER BY name""",
                (category_id,)
            )
            return [
                Product(
                    id=row[0],
                    category_id=row[1],
                    name=row[2],
                    model=row[3],
                    price=row[4],
                    stock=row[5],
                    description=row[6]
                )
                for row in cursor.fetchall()
            ]
    
    def find_product_by_id(self, product_id: int) -> Optional[Product]:
        """Obtiene un producto por ID"""
        with self.db.get_cursor() as cursor:
            cursor.execute(
                """SELECT id, category_id, name, model, price, stock, description 
                   FROM products WHERE id = ?""",
                (product_id,)
            )
            row = cursor.fetchone()
            if row:
                return Product(
                    id=row[0],
                    category_id=row[1],
                    name=row[2],
                    model=row[3],
                    price=row[4],
                    stock=row[5],
                    description=row[6]
                )
            return None
    
    def create_product(self, product: Product) -> int:
        """Crea un nuevo producto"""
        with self.db.get_cursor() as cursor:
            cursor.execute(
                """INSERT INTO products (category_id, name, model, price, stock, description)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (product.category_id, product.name, product.model, 
                 product.price, product.stock, product.description)
            )
            return cursor.lastrowid
    
    def update_product(self, product: Product) -> bool:
        """Actualiza un producto existente"""
        with self.db.get_cursor() as cursor:
            cursor.execute(
                """UPDATE products 
                   SET category_id = ?, name = ?, model = ?, price = ?, stock = ?, description = ?
                   WHERE id = ?""",
                (product.category_id, product.name, product.model, 
                 product.price, product.stock, product.description, product.id)
            )
            return cursor.rowcount > 0
    
    def get_products_tree(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Obtiene productos organizados en árbol por categoría
        
        Returns:
            {
                "Tarjetas Gráficas": [
                    {"id": 1, "name": "RTX 4090", "model": "NVIDIA", "price": 1600, "stock": 4},
                    ...
                ],
                ...
            }
        """
        tree = {}
        categories = self.find_all_categories()
        
        for category in categories:
            products = self.find_products_by_category(category.id)
            if products:  # Solo agregar categorías con productos
                tree[category.name] = [
                    {
                        "id": p.id,
                        "name": p.name,
                        "model": p.model,
                        "price": p.price,
                        "stock": p.stock,
                        "description": p.description
                    }
                    for p in products
                ]
        
        return tree
    
    # ============ ITEMS DE PEDIDOS ============
    
    def create_order_item(self, order_item: OrderItem) -> int:
        """Crea un item en un pedido"""
        with self.db.get_cursor() as cursor:
            cursor.execute(
                """INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                   VALUES (?, ?, ?, ?)""",
                (order_item.order_id, order_item.product_id, 
                 order_item.quantity, order_item.unit_price)
            )
            return cursor.lastrowid
    
    def find_order_items(self, order_id: int) -> List[Dict[str, Any]]:
        """Obtiene todos los items de un pedido con info de productos"""
        with self.db.get_cursor() as cursor:
            cursor.execute(
                """SELECT oi.id, oi.product_id, oi.quantity, oi.unit_price,
                          p.name, p.model, c.name as category
                   FROM order_items oi
                   JOIN products p ON oi.product_id = p.id
                   JOIN categories c ON p.category_id = c.id
                   WHERE oi.order_id = ?
                   ORDER BY c.name, p.name""",
                (order_id,)
            )
            return [
                {
                    "id": row[0],
                    "product_id": row[1],
                    "quantity": row[2],
                    "unit_price": row[3],
                    "product_name": row[4],
                    "product_model": row[5],
                    "category": row[6],
                    "total": row[2] * row[3]
                }
                for row in cursor.fetchall()
            ]
    
    def delete_order_item(self, item_id: int) -> bool:
        """Elimina un item de un pedido"""
        with self.db.get_cursor() as cursor:
            cursor.execute("DELETE FROM order_items WHERE id = ?", (item_id,))
            return cursor.rowcount > 0
