"""
Servicio de Pedidos (placeholder)
Lógica de negocio para gestión de pedidos
"""


class OrderService:
    """Servicio de gestión de pedidos"""
    
    def __init__(self, order_repository):
        """
        Inicializa el servicio
        
        Args:
            order_repository: Repositorio de pedidos
        """
        self.order_repo = order_repository
