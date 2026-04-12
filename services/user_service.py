"""
Servicio de Usuario (placeholder)
Lógica de negocio para gestión de usuarios
"""


class UserService:
    """Servicio de gestión de usuarios"""
    
    def __init__(self, user_repository):
        """
        Inicializa el servicio
        
        Args:
            user_repository: Repositorio de usuarios
        """
        self.user_repo = user_repository
