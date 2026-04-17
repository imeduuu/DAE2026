"""
Servicio de Pedidos
Lógica de negocio para gestión de pedidos
"""
from database.models import Order
from typing import List
from utils.constants import (
    ORDER_STATUS_PENDING,
    ORDER_STATUS_CONFIRMED,
    ORDER_STATUS_SHIPPED,
    ORDER_STATUS_DELIVERED,
    ORDER_STATUS_CANCELLED,
    ROLE_ADMIN,
    ROLE_MANAGER,
)


class OrderService:
    """Servicio de gestión de pedidos"""
    
    def __init__(self, order_repository):
        """
        Inicializa el servicio
        
        Args:
            order_repository: Repositorio de pedidos
        """
        self.order_repo = order_repository
    
    def create_order(self, user_id: int, description: str) -> tuple[bool, str, Order | None]:
        """
        Crea un nuevo pedido
        
        Args:
            user_id: ID del usuario
            description: Descripción del pedido
        
        Returns:
            Tupla (éxito, mensaje, pedido)
        """
        if not description or not description.strip():
            return False, "La descripción no puede estar vacía", None
        
        try:
            order = Order(
                user_id=user_id,
                description=description.strip(),
                status=ORDER_STATUS_PENDING
            )
            created_order = self.order_repo.create(order)
            return True, "Pedido creado correctamente", created_order
        except Exception as e:
            return False, f"Error al crear pedido: {e}", None
    
    def get_user_orders(self, user_id: int, role: str = "cliente") -> List[Order]:
        """Obtiene los pedidos visibles para el usuario"""
        if role in [ROLE_ADMIN, ROLE_MANAGER]:
            return self.order_repo.find_all()
        return self.order_repo.find_by_user_id(user_id)
    
    def update_order_status(self, order_id: int, status: str) -> tuple[bool, str]:
        """Actualiza el estado de un pedido"""
        valid_statuses = [
            ORDER_STATUS_PENDING,
            ORDER_STATUS_CONFIRMED,
            ORDER_STATUS_SHIPPED,
            ORDER_STATUS_DELIVERED,
            ORDER_STATUS_CANCELLED,
        ]
        if status not in valid_statuses:
            return False, f"Estado no válido. Opciones: {', '.join(valid_statuses)}"
        
        try:
            updated = self.order_repo.update_status(order_id, status)
            if not updated:
                return False, "Pedido no encontrado"
            return True, "Estado actualizado correctamente"
        except Exception as e:
            return False, f"Error al actualizar: {e}"
