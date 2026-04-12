"""
Mediador de Aplicación
Actúa como coordinador entre las diferentes capas de la aplicación
"""
from database.connection import DatabaseConnection
from repositories.user_repository import UserRepository
from services.auth_service import AuthService


class AppMediator:
    """Mediador central de la aplicación"""
    
    def __init__(self, db_path: str = "data/orders.db"):
        """
        Inicializa el mediador y todas las dependencias
        
        Args:
            db_path: Ruta de la base de datos
        """
        # Capa de datos
        self.db_connection = DatabaseConnection(db_path)
        
        # Repositorios
        self.user_repository = UserRepository(self.db_connection)
        
        # Servicios
        self.auth_service = AuthService(self.user_repository)
    
    def shutdown(self):
        """Limpia recursos al cerrar la aplicación"""
        # Aquí puedes agregar limpieza de recursos si es necesario
        pass
