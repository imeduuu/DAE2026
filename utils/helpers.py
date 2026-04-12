"""
Funciones auxiliares de seguridad
Hashing de contraseñas y utilidades criptográficas
"""
import hashlib
import hmac


def hash_password(password: str, salt: str = "default_salt") -> str:
    """
    Genera un hash de la contraseña
    
    Args:
        password: Contraseña en texto plano
        salt: Salt para el hash
        
    Returns:
        Hash de la contraseña
    """
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()


def verify_password(password: str, password_hash: str, salt: str = "default_salt") -> bool:
    """
    Verifica si una contraseña coincide con su hash
    
    Args:
        password: Contraseña en texto plano
        password_hash: Hash almacenado
        salt: Salt utilizado
        
    Returns:
        True si coincide, False de lo contrario
    """
    return hmac.compare_digest(hash_password(password, salt), password_hash)
