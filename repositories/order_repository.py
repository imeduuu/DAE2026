"""
Repositorio de Pedidos
Capa de acceso a datos para la entidad Order
"""

from datetime import datetime
from typing import Optional, List

from database.connection import DatabaseConnection
from database.models import Order


class OrderRepository:
    """Repositorio para gestionar operaciones con pedidos"""
    
    def __init__(self, db_connection: DatabaseConnection):
        """
        Inicializa el repositorio
        
        Args:
            db_connection: Instancia de DatabaseConnection
        """
        self.db = db_connection
    
    def create(self, order: Order) -> Order:
        """Crea un pedido en la base de datos"""
        with self.db.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO orders (user_id, description, status)
                VALUES (?, ?, ?)
                """,
                (order.user_id, order.description, order.status)
            )
            order.id = cursor.lastrowid
            cursor.execute("SELECT * FROM orders WHERE id = ?", (order.id,))
            row = cursor.fetchone()
            return self._row_to_order(row)

    def find_by_id(self, order_id: int) -> Optional[Order]:
        """Busca un pedido por su ID"""
        with self.db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            row = cursor.fetchone()
            return self._row_to_order(row) if row else None

    def find_by_user_id(self, user_id: int) -> List[Order]:
        """Obtiene todos los pedidos de un usuario"""
        with self.db.get_cursor() as cursor:
            cursor.execute(
                "SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,)
            )
            rows = cursor.fetchall()
            return [self._row_to_order(row) for row in rows]

    def find_all(self) -> List[Order]:
        """Obtiene todos los pedidos"""
        with self.db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM orders ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [self._row_to_order(row) for row in rows]

    def update_status(self, order_id: int, status: str) -> bool:
        """Actualiza el estado de un pedido"""
        with self.db.get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE orders
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (status, order_id)
            )
            return cursor.rowcount > 0

    def _to_datetime(self, value):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

    def _row_to_order(self, row) -> Order:
        """Convierte una fila de la base de datos a un objeto Order"""
        return Order(
            id=row["id"],
            user_id=row["user_id"],
            description=row["description"],
            status=row["status"],
            created_at=self._to_datetime(row["created_at"]),
            updated_at=self._to_datetime(row["updated_at"])
        )
