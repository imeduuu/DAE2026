"""
Servicio de Autenticación
Lógica de negocio para login y registro
"""
from database.models import User
from repositories.user_repository import UserRepository
from utils.validators import validate_username, validate_email, validate_password
from utils.helpers import hash_password, verify_password
from typing import Tuple, Optional


class AuthService:
    """Servicio de autenticación"""
    
    def __init__(self, user_repository: UserRepository):
        """
        Inicializa el servicio
        
        Args:
            user_repository: Repositorio de usuarios
        """
        self.user_repo = user_repository
    
    def register(self, username: str, email: str, password: str, 
                 role: str = "cliente") -> Tuple[bool, str, Optional[User]]:
        """
        Registra un nuevo usuario
        
        Args:
            username: Nombre de usuario
            email: Correo electrónico
            password: Contraseña
            role: Rol del usuario ('cliente' o 'administrador')
            
        Returns:
            (éxito, mensaje, usuario_creado)
        """
        # Validaciones
        is_valid, msg = validate_username(username)
        if not is_valid:
            return False, msg, None
        
        is_valid, msg = validate_email(email)
        if not is_valid:
            return False, msg, None
        
        is_valid, msg = validate_password(password)
        if not is_valid:
            return False, msg, None
        
        # Verificar que no exista el usuario
        if self.user_repo.find_by_username(username):
            return False, "El nombre de usuario ya existe", None
        
        if self.user_repo.find_by_email(email):
            return False, "El correo ya está registrado", None
        
        # Crear usuario
        try:
            password_hash = hash_password(password)
            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                role=role
            )
            created_user = self.user_repo.create(user)
            return True, "Usuario registrado exitosamente", created_user
        except Exception as e:
            return False, f"Error al registrar usuario: {str(e)}", None
    
    def login(self, username: str, password: str) -> Tuple[bool, str, Optional[User]]:
        """
        Autentica un usuario
        
        Args:
            username: Nombre de usuario
            password: Contraseña
            
        Returns:
            (éxito, mensaje, usuario_autenticado)
        """
        if not username or not password:
            return False, "Usuario y contraseña son requeridos", None
        
        # Buscar usuario
        user = self.user_repo.find_by_username(username)
        if not user:
            return False, "Usuario o contraseña incorrectos", None
        
        # Verificar contraseña
        if not verify_password(password, user.password_hash):
            return False, "Usuario o contraseña incorrectos", None
        
        return True, "Login exitoso", user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """
        Obtiene un usuario por ID
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Usuario o None si no existe
        """
        return self.user_repo.find_by_id(user_id)
