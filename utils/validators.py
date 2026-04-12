"""
Validadores de entrada
Funciones para validar datos de entrada
"""
import re
from typing import Tuple


def validate_username(username: str) -> Tuple[bool, str]:
    """
    Valida el nombre de usuario
    
    Args:
        username: Nombre de usuario a validar
        
    Returns:
        (es_válido, mensaje_error)
    """
    if not username or len(username) < 3:
        return False, "El usuario debe tener al menos 3 caracteres"
    
    if len(username) > 30:
        return False, "El usuario no puede exceder 30 caracteres"
    
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return False, "El usuario solo puede contener letras, números y guiones bajos"
    
    return True, ""


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Valida el correo electrónico
    
    Args:
        email: Email a validar
        
    Returns:
        (es_válido, mensaje_error)
    """
    if not email:
        return False, "El correo es requerido"
    
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return False, "El correo no es válido"
    
    return True, ""


def validate_password(password: str) -> Tuple[bool, str]:
    """
    Valida la contraseña
    
    Args:
        password: Contraseña a validar
        
    Returns:
        (es_válido, mensaje_error)
    """
    if not password or len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres"
    
    if len(password) > 128:
        return False, "La contraseña no puede exceder 128 caracteres"
    
    return True, ""
