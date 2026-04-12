"""
Aplicación principal
Punto de entrada de la aplicación
"""
import sys
from mediator.app_mediator import AppMediator
from database.models import User
from utils.constants import ROLE_ADMIN, ROLE_CLIENT


def main():
    """Función principal"""
    print("=" * 60)
    print("Gestor de Pedidos - Inicialización")
    print("=" * 60)
    
    try:
        # Inicializar mediador (configura la BD y todas las capas)
        mediator = AppMediator()
        print("✓ Aplicación inicializada correctamente\n")
        
        # Menú principal
        while True:
            print("\n--- MENÚ PRINCIPAL ---")
            print("1. Registrar nuevo usuario")
            print("2. Login")
            print("3. Ver usuarios (admin)")
            print("4. Salir")
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                register_user(mediator)
            elif opcion == "2":
                login_user(mediator)
            elif opcion == "3":
                list_users(mediator)
            elif opcion == "4":
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida")
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


def register_user(mediator: AppMediator):
    """Registra un nuevo usuario"""
    print("\n--- REGISTRO DE USUARIO ---")
    
    username = input("Nombre de usuario: ").strip()
    email = input("Correo electrónico: ").strip()
    password = input("Contraseña: ").strip()
    
    # Seleccionar rol
    print("\nSeleccione rol:")
    print("1. Cliente")
    print("2. Administrador")
    rol_opcion = input("Seleccione (1-2): ").strip()
    
    role = ROLE_ADMIN if rol_opcion == "2" else ROLE_CLIENT
    
    # Registrar
    success, message, user = mediator.auth_service.register(
        username, email, password, role
    )
    
    if success:
        print(f"✓ {message}")
        print(f"  ID: {user.id}")
        print(f"  Usuario: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Rol: {user.role}")
    else:
        print(f"❌ {message}")


def login_user(mediator: AppMediator):
    """Inicia sesión con un usuario"""
    print("\n--- LOGIN ---")
    
    username = input("Nombre de usuario: ").strip()
    password = input("Contraseña: ").strip()
    
    success, message, user = mediator.auth_service.login(username, password)
    
    if success:
        print(f"✓ {message}")
        print(f"\n  Bienvenido {user.username}!")
        print(f"  Rol: {user.role}")
        print(f"  Email: {user.email}")
    else:
        print(f"❌ {message}")


def list_users(mediator: AppMediator):
    """Lista todos los usuarios registrados"""
    print("\n--- LISTA DE USUARIOS ---")
    
    users = mediator.user_repository.find_all()
    
    if not users:
        print("No hay usuarios registrados")
        return
    
    print(f"\nTotal de usuarios: {len(users)}\n")
    for user in users:
        print(f"  ID: {user.id} | Usuario: {user.username:<15} | " + 
              f"Email: {user.email:<25} | Rol: {user.role}")


if __name__ == "__main__":
    main()
