"""
Módulo de modelos de datos
Define las clases que representan las entidades del sistema
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Modelo de Usuario"""
    username: str
    email: str
    password_hash: str
    role: str = "cliente"  # 'cliente' o 'administrador'
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def is_admin(self) -> bool:
        """Verifica si el usuario es administrador"""
        return self.role == "administrador"
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


@dataclass
class Order:
    """Modelo de Pedido"""
    user_id: int
    description: str
    status: str = "pendiente"  # 'pendiente', 'confirmado', 'enviado', 'entregado', 'cancelado'
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
