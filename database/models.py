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
class Category:
    """Modelo de Categoría de Productos"""
    name: str
    description: Optional[str] = None
    id: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


@dataclass
class Product:
    """Modelo de Producto"""
    category_id: int
    name: str
    model: str
    price: float
    stock: int
    description: Optional[str] = None
    id: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario"""
        return {
            "id": self.id,
            "category_id": self.category_id,
            "name": self.name,
            "model": self.model,
            "price": self.price,
            "stock": self.stock,
            "description": self.description
        }


@dataclass
class OrderItem:
    """Modelo de Item en un Pedido"""
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    id: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario"""
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price
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
