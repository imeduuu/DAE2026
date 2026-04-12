"""
Servicio de Usuario
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
    
    def get_all_users(self):
        """Obtiene todos los usuarios"""
        return self.user_repo.find_all()
    
    def get_user_by_id(self, user_id: int):
        """Obtiene un usuario por ID"""
        return self.user_repo.find_by_id(user_id)
    
    def get_user_by_username(self, username: str):
        """Obtiene un usuario por nombre de usuario"""
        return self.user_repo.find_by_username(username)
    
    def delete_user(self, user_id: int) -> tuple[bool, str]:
        """Elimina un usuario"""
        try:
            # Aquí iría la lógica para eliminar de BD
            return True, "Usuario eliminado correctamente"
        except Exception as e:
            return False, f"Error al eliminar: {e}"
