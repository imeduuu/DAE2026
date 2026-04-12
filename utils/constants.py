"""
Constantes de la aplicación
"""

# Roles de usuario (3 tipos)
ROLE_ADMIN = "administrador"      # Acceso total, ve todos los usuarios
ROLE_MANAGER = "gerente"           # Acceso intermedio, puede gestionar pedidos
ROLE_CLIENT = "cliente"            # Acceso limitado, solo ve sus datos

# Diccionario de roles con descripciones
ROLES = {
    ROLE_ADMIN: "Administrador",
    ROLE_MANAGER: "Gerente",
    ROLE_CLIENT: "Cliente"
}

# Jerarquía de permisos
ROLE_HIERARCHY = {
    ROLE_ADMIN: 3,      # Máximo nivel
    ROLE_MANAGER: 2,    # Nivel intermedio
    ROLE_CLIENT: 1      # Nivel mínimo
}

# Estados de pedido
ORDER_STATUS_PENDING = "pendiente"
ORDER_STATUS_CONFIRMED = "confirmado"
ORDER_STATUS_SHIPPED = "enviado"
ORDER_STATUS_DELIVERED = "entregado"
ORDER_STATUS_CANCELLED = "cancelado"

# Configuración de aplicación
APP_NAME = "Gestor de Pedidos"
APP_VERSION = "1.0.0"
DATABASE_PATH = "data/orders.db"
