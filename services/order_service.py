"""
Servicio de Pedidos
Lógica de negocio para gestión de pedidos
"""
from database.models import Order
from datetime import datetime


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
        try:
            if not description.strip():
                return False, "La descripción no puede estar vacía", None
            
            order = Order(
                user_id=user_id,
                description=description,
                status="pendiente",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            # Aquí iría la lógica para guardar en BD
            return True, "Pedido creado correctamente", order
        except Exception as e:
            return False, f"Error al crear pedido: {e}", None
    
    def get_user_orders(self, user_id: int) -> list[Order]:
        """Obtiene los pedidos de un usuario"""
        # Aquí iría la lógica para obtener de BD
        return []
    
    def update_order_status(self, order_id: int, status: str) -> tuple[bool, str]:
        """Actualiza el estado de un pedido"""
        try:
            valid_statuses = ["pendiente", "confirmado", "enviado", "entregado", "cancelado"]
            if status not in valid_statuses:
                return False, f"Estado no válido. Opciones: {', '.join(valid_statuses)}"
            
            # Aquí iría la lógica para actualizar en BD
            return True, "Estado actualizado correctamente"
        except Exception as e:
            return False, f"Error al actualizar: {e}"
