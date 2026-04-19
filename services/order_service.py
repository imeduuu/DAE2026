"""
Servicio de Pedidos
Lógica de negocio para gestión de pedidos
"""
from database.models import Order
from typing import List
from datetime import datetime, timedelta
from utils.constants import (
    ORDER_STATUS_PENDING,
    ORDER_STATUS_CONFIRMED,
    ORDER_STATUS_SHIPPED,
    ORDER_STATUS_DELIVERED,
    ORDER_STATUS_CANCELLED,
    ROLE_ADMIN,
    ROLE_MANAGER,
)
import logging
import os

# Configurar logging para auditoría de transiciones
log_file = "data/order_transitions.log"
os.makedirs(os.path.dirname(log_file) if os.path.dirname(log_file) else ".", exist_ok=True)
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Configuración de tiempos para transiciones automáticas (en minutos)
TRANSITION_CONFIG = {
    ORDER_STATUS_PENDING: {
        "next_status": ORDER_STATUS_CONFIRMED,
        "wait_minutes": 2,
        "description": "Confirmado automáticamente"
    },
    ORDER_STATUS_CONFIRMED: {
        "next_status": ORDER_STATUS_SHIPPED,
        "wait_minutes": 5,
        "description": "Enviado automáticamente"
    },
    ORDER_STATUS_SHIPPED: {
        "next_status": ORDER_STATUS_DELIVERED,
        "wait_minutes": 8,
        "description": "Entregado automáticamente"
    }
}


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
    
    def process_automatic_transitions(self) -> int:
        """
        Procesa transiciones automáticas de pedidos basadas en tiempo transcurrido
        Se ejecuta periódicamente (cada 30 segundos aprox)
        
        Returns:
            Número de pedidos que fueron transicionados
        """
        transitions_count = 0
        
        try:
            # Obtener todos los pedidos
            all_orders = self.order_repo.find_all()
            
            for order in all_orders:
                # Skip si ya está en estado final
                if order.status == ORDER_STATUS_DELIVERED or order.status == ORDER_STATUS_CANCELLED:
                    continue
                
                # Verificar si este estado tiene transición automática configurada
                if order.status not in TRANSITION_CONFIG:
                    continue
                
                config = TRANSITION_CONFIG[order.status]
                required_minutes = config["wait_minutes"]
                
                # Calcular tiempo transcurrido desde creación del pedido
                if not order.created_at:
                    continue
                
                time_elapsed = datetime.now() - order.created_at
                minutes_elapsed = time_elapsed.total_seconds() / 60
                
                # Si ha pasado el tiempo requerido, hacer la transición
                if minutes_elapsed >= required_minutes:
                    new_status = config["next_status"]
                    
                    # Actualizar en BD
                    if self.order_repo.update_status(order.id, new_status):
                        # Registrar en auditoría
                        log_msg = (
                            f"TRANSICIÓN AUTOMÁTICA | Pedido ID: {order.id} | "
                            f"Usuario ID: {order.user_id} | "
                            f"{order.status} → {new_status} | "
                            f"{config['description']} | "
                            f"Tiempo transcurrido: {minutes_elapsed:.1f} min"
                        )
                        logging.info(log_msg)
                        transitions_count += 1
        
        except Exception as e:
            logging.error(f"Error procesando transiciones automáticas: {e}")
        
        return transitions_count
