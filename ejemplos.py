"""
Ejemplos de Uso - Demostración de Funcionalidades

Este archivo contiene ejemplos de cómo usar la aplicación programáticamente.
"""

from mediator.app_mediator import AppMediator
from utils.constants import ROLE_ADMIN, ROLE_CLIENT


def ejemplo_1_registro_y_login():
    """Ejemplo 1: Registro de usuario y login"""
    print("=" * 60)
    print("EJEMPLO 1: Registro y Login")
    print("=" * 60)
    
    mediator = AppMediator()
    
    # Registrar un nuevo usuario
    print("\n[1] Registrando usuario...")
    success, msg, user = mediator.auth_service.register(
        username="juan_perez",
        email="juan@example.com",
        password="mi_contraseña_segura",
        role=ROLE_CLIENT
    )
    
    if success:
        print(f"✓ Registro exitoso: {msg}")
        print(f"  Detalles: ID={user.id}, Usuario={user.username}, Email={user.email}")
    else:
        print(f"✗ Error: {msg}")
    
    # Intentar login
    print("\n[2] Iniciando sesión...")
    success, msg, user = mediator.auth_service.login("juan_perez", "mi_contraseña_segura")
    
    if success:
        print(f"✓ Login exitoso: {msg}")
        print(f"  Bienvenido {user.username}, tu rol es: {user.role}")
    else:
        print(f"✗ Error: {msg}")


def ejemplo_2_validaciones():
    """Ejemplo 2: Validaciones en registro"""
    print("\n" + "=" * 60)
    print("EJEMPLO 2: Validaciones y Manejo de Errores")
    print("=" * 60)
    
    mediator = AppMediator()
    
    # Intentar registrar con email inválido
    print("\n[1] Intentando registrar con email inválido...")
    success, msg, user = mediator.auth_service.register(
        username="usuario_test",
        email="invalid-email",  # Email inválido
        password="password123",
        role=ROLE_CLIENT
    )
    print(f"Resultado: {msg}")
    
    # Intentar registrar con contraseña corta
    print("\n[2] Intentando registrar con contraseña corta...")
    success, msg, user = mediator.auth_service.register(
        username="usuario_test2",
        email="test@example.com",
        password="123",  # Contraseña muy corta
        role=ROLE_CLIENT
    )
    print(f"Resultado: {msg}")
    
    # Intentar usuario duplicado
    print("\n[3] Registrando primer usuario...")
    mediator.auth_service.register(
        username="usuario_duplicado",
        email="duplicado@example.com",
        password="password123",
        role=ROLE_CLIENT
    )
    
    print("\n[4] Intentando crear usuario con mismo nombre...")
    success, msg, user = mediator.auth_service.register(
        username="usuario_duplicado",  # Mismo nombre
        email="otro@example.com",
        password="password123",
        role=ROLE_CLIENT
    )
    print(f"Resultado: {msg}")


def ejemplo_3_consulta_usuarios():
    """Ejemplo 3: Consultar usuarios de la base de datos"""
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Consulta de Usuarios")
    print("=" * 60)
    
    mediator = AppMediator()
    
    # Registrar varios usuarios para demostración
    print("\n[1] Registrando usuarios de ejemplo...")
    usuarios_demo = [
        ("carlos", "carlos@company.com", "pass123", ROLE_CLIENT),
        ("ana", "ana@company.com", "pass456", ROLE_CLIENT),
        ("admin", "admin@company.com", "admin123", ROLE_ADMIN),
    ]
    
    for username, email, password, role in usuarios_demo:
        mediator.auth_service.register(username, email, password, role)
        print(f"  ✓ {username} registrado como {role}")
    
    # Obtener todos los usuarios
    print("\n[2] Lista de todos los usuarios:")
    usuarios = mediator.user_repository.find_all()
    
    for user in usuarios:
        print(f"  ID={user.id} | {user.username:<15} | {user.email:<25} | {user.role}")
    
    # Buscar usuario específico
    print("\n[3] Buscando usuario específico...")
    user = mediator.user_repository.find_by_username("carlos")
    if user:
        print(f"  Encontrado: {user.username} ({user.email})")
        print(f"  Rol: {user.role}")
        print(f"  Es administrador: {user.is_admin()}")
    
    # Buscar por email
    print("\n[4] Buscando por email...")
    user = mediator.user_repository.find_by_email("admin@company.com")
    if user:
        print(f"  Encontrado: {user.username} es: {user.role}")


def ejemplo_4_actualizacion_usuario():
    """Ejemplo 4: Actualizar datos de usuario"""
    print("\n" + "=" * 60)
    print("EJEMPLO 4: Actualización de Usuario")
    print("=" * 60)
    
    mediator = AppMediator()
    
    # Crear un usuario inicial
    print("\n[1] Creando usuario...")
    success, msg, user = mediator.auth_service.register(
        username="usuario_editable",
        email="original@example.com",
        password="password123",
        role=ROLE_CLIENT
    )
    print(f"  Creado: {user.username} ({user.email})")
    
    # Modificar el usuario
    print("\n[2] Modificando datos del usuario...")
    user.email = "nuevo_email@example.com"
    user.role = ROLE_ADMIN
    
    actualizado = mediator.user_repository.update(user)
    
    if actualizado:
        print(f"  ✓ Usuario actualizado correctamente")
        
        # Verificar cambios
        user_actualizado = mediator.user_repository.find_by_username("usuario_editable")
        print(f"  Email: {user_actualizado.email}")
        print(f"  Rol: {user_actualizado.role}")
    
    # Eliminar usuario
    print("\n[3] Eliminando usuario...")
    if user_actualizado:
        eliminado = mediator.user_repository.delete(user_actualizado.id)
        if eliminado:
            print(f"  ✓ Usuario eliminado")


def ejemplo_5_seguridad():
    """Ejemplo 5: Demostración de seguridad (hashing)"""
    print("\n" + "=" * 60)
    print("EJEMPLO 5: Seguridad - Hashing de Contraseñas")
    print("=" * 60)
    
    mediator = AppMediator()
    
    # Crear usuario y verificar hash
    print("\n[1] Registrando usuario...")
    success, msg, user = mediator.auth_service.register(
        username="usuario_seguro",
        email="seguro@example.com",
        password="MiContraseñaSegura123",
        role=ROLE_CLIENT
    )
    
    print(f"  Usuario: {user.username}")
    print(f"  Contraseña original: MiContraseñaSegura123")
    print(f"  Hash almacenado: {user.password_hash[:40]}...")
    print(f"  ✓ La contraseña NO se almacena en texto plano")
    
    # Intentar login con contraseña incorrecta
    print("\n[2] Intentando login con contraseña incorrecta...")
    success, msg, _ = mediator.auth_service.login("usuario_seguro", "contraseña_incorrecta")
    print(f"  Resultado: {msg} (✓ Seguridad funcionando)")
    
    # Login correcto
    print("\n[3] Login con contraseña correcta...")
    success, msg, user = mediator.auth_service.login("usuario_seguro", "MiContraseñaSegura123")
    print(f"  Resultado: {msg}")


if __name__ == "__main__":
    # Descomentar el ejemplo que desees ejecutar
    
    ejemplo_1_registro_y_login()
    # ejemplo_2_validaciones()
    # ejemplo_3_consulta_usuarios()
    # ejemplo_4_actualizacion_usuario()
    # ejemplo_5_seguridad()
    
    print("\n" + "=" * 60)
    print("Ejemplos completados")
    print("=" * 60)
