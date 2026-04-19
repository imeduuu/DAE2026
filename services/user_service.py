"""
Servicio de Usuario
Lógica de negocio para gestión de usuarios
"""
from utils.constants import ROLE_ADMIN
from datetime import datetime
import os
import logging


# Configurar logging para auditoría
log_file = "data/audit.log"
os.makedirs(os.path.dirname(log_file) if os.path.dirname(log_file) else ".", exist_ok=True)
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


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
    
    def count_admins(self) -> int:
        """
        Cuenta cuántos administradores hay en el sistema
        
        Returns:
            Número de administradores
        """
        users = self.user_repo.find_all()
        return sum(1 for user in users if user.role == ROLE_ADMIN)
    
    def change_user_role(self, user_id: int, new_role: str, 
                        admin_user_id: int = None, reason: str = "") -> tuple[bool, str]:
        """
        Cambia el rol de un usuario con validaciones de seguridad
        
        Args:
            user_id: ID del usuario a cambiar de rol
            new_role: Nuevo rol a asignar
            admin_user_id: ID del admin que realiza el cambio (para auditoría)
            reason: Motivo del cambio (opcional)
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Validación: No cambiar el rol a si mismo
            if user_id == admin_user_id:
                return False, "No puedes cambiar tu propio rol"
            
            # Obtener usuario a cambiar
            target_user = self.user_repo.find_by_id(user_id)
            if not target_user:
                return False, "Usuario no encontrado"
            
            # Validación: Mantener al menos 1 administrador
            if target_user.role == ROLE_ADMIN and new_role != ROLE_ADMIN:
                admin_count = self.count_admins()
                if admin_count <= 1:
                    return False, "No se puede remover el último administrador del sistema"
            
            # Cambiar el rol
            old_role = target_user.role
            target_user.role = new_role
            
            # Actualizar en BD
            if self.user_repo.update(target_user):
                # Registrar en auditoría
                admin_name = self.user_repo.find_by_id(admin_user_id).username if admin_user_id else "Sistema"
                log_message = (
                    f"CAMBIO DE ROL | Usuario: {target_user.username} (ID: {user_id}) | "
                    f"Rol anterior: {old_role} | Rol nuevo: {new_role} | "
                    f"Realizado por: {admin_name}"
                )
                if reason:
                    log_message += f" | Motivo: {reason}"
                logging.info(log_message)
                
                return True, f"Rol actualizado correctamente: {old_role} → {new_role}"
            else:
                return False, "Error al actualizar el rol en la base de datos"
                
        except Exception as e:
            return False, f"Error al cambiar rol: {str(e)}"
