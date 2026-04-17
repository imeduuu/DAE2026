"""
Aplicación principal - Gestor de Pedidos
Punto de entrada único de la aplicación
Soporta modo GUI (PyQt6) y modo CLI (consola)
"""
import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_gui():
    """Ejecuta la aplicación en modo GUI"""
    try:
        from PyQt6.QtWidgets import QApplication
        from mediator.app_mediator import AppMediator
        from gui.main_window import MainWindow
        from gui.styles import DARK_STYLESHEET
        
        print("🎨 Iniciando interfaz gráfica...")
        
        # Inicializar aplicación PyQt
        app = QApplication(sys.argv)
        
        # Aplicar estilos globales
        app.setStyle('Fusion')
        app.setStyleSheet(DARK_STYLESHEET)
        
        # Inicializar mediador
        mediator = AppMediator()
        
        # Crear y mostrar ventana principal
        window = MainWindow(mediator)
        
        sys.exit(app.exec())
    
    except ImportError as e:
        print(f"⚠️  PyQt6 no está instalado: {e}")
        print("Instala con: pip install PyQt6==6.6.1")
        print("\nFallando a modo CLI...")
        run_cli()
    except Exception as e:
        print(f"❌ Error al iniciar GUI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


from mediator.app_mediator import AppMediator
from utils.constants import (
    ROLE_ADMIN,
    ROLE_CLIENT,
    ROLE_MANAGER,
    ORDER_STATUS_PENDING,
    ORDER_STATUS_CONFIRMED,
    ORDER_STATUS_SHIPPED,
    ORDER_STATUS_DELIVERED,
    ORDER_STATUS_CANCELLED,
)


def run_cli():
    """Ejecuta la aplicación en modo consola (CLI)"""
    print("=" * 60)
    print("Gestor de Pedidos - Modo Consola")
    print("=" * 60)
    
    try:
        # Inicializar mediador
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
                register_user_cli(mediator)
            elif opcion == "2":
                login_user_cli(mediator)
            elif opcion == "3":
                list_users_cli(mediator)
            elif opcion == "4":
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida")
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


def register_user_cli(mediator):
    """Registra un nuevo usuario en modo CLI"""
    print("\n--- REGISTRO DE USUARIO ---")
    
    username = input("Nombre de usuario: ").strip()
    email = input("Correo electrónico: ").strip()
    password = input("Contraseña: ").strip()
    
    # Seleccionar rol
    print("\nSeleccione rol:")
    print("1. Cliente")
    print("2. Administrador")
    rol_opcion = input("Seleccione (1-2): ").strip()
    
    from utils.constants import ROLE_ADMIN, ROLE_CLIENT
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


def login_user_cli(mediator):
    """Inicia sesión en modo CLI"""
    print("\n--- LOGIN ---")
    
    username = input("Nombre de usuario: ").strip()
    password = input("Contraseña: ").strip()
    
    success, message, user = mediator.auth_service.login(username, password)
    
    if success:
        print(f"✓ {message}")
        print(f"\n  Bienvenido {user.username}!")
        print(f"  Rol: {user.role}")
        print(f"  Email: {user.email}")
        user_dashboard_cli(mediator, user)
    else:
        print(f"❌ {message}")


def user_dashboard_cli(mediator, user):
    """Muestra el menú de usuario después del login"""
    while True:
        print("\n--- MENÚ DE USUARIO ---")
        print("1. Crear nuevo pedido")
        print("2. Ver mis pedidos")
        if user.role in [ROLE_ADMIN, ROLE_MANAGER]:
            print("3. Ver todos los pedidos")
            print("4. Cambiar estado de pedido")
            print("5. Cerrar sesión")
        else:
            print("3. Cerrar sesión")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            create_order_cli(mediator, user)
        elif opcion == "2":
            list_orders_cli(mediator, user)
        elif opcion == "3" and user.role in [ROLE_ADMIN, ROLE_MANAGER]:
            list_all_orders_cli(mediator)
        elif opcion == "4" and user.role in [ROLE_ADMIN, ROLE_MANAGER]:
            change_order_status_cli(mediator)
        elif opcion == "5" and user.role in [ROLE_ADMIN, ROLE_MANAGER]:
            print("Cerrando sesión...")
            break
        elif opcion == "3" and user.role not in [ROLE_ADMIN, ROLE_MANAGER]:
            print("Cerrando sesión...")
            break
        else:
            print("Opción no válida")


def create_order_cli(mediator, user):
    """Crea un pedido desde la línea de comandos"""
    print("\n--- CREAR PEDIDO ---")
    description = input("Descripción del pedido: ").strip()
    success, message, order = mediator.order_service.create_order(user.id, description)
    if success:
        print(f"✓ {message}")
        print(f"  Pedido ID: {order.id}")
        print(f"  Estado: {order.status}")
    else:
        print(f"❌ {message}")


def list_orders_cli(mediator, user):
    """Lista los pedidos del usuario"""
    print("\n--- MIS PEDIDOS ---")
    orders = mediator.order_service.get_user_orders(user.id, user.role)
    if not orders:
        print("No hay pedidos registrados")
        return
    for order in orders:
        print(f"  ID: {order.id} | Usuario ID: {order.user_id} | Estado: {order.status} | Descripción: {order.description}")


def list_all_orders_cli(mediator):
    """Lista todos los pedidos (admin)"""
    print("\n--- TODOS LOS PEDIDOS ---")
    orders = mediator.order_service.get_user_orders(0, ROLE_ADMIN)
    if not orders:
        print("No hay pedidos registrados")
        return
    for order in orders:
        print(f"  ID: {order.id} | Usuario ID: {order.user_id} | Estado: {order.status} | Descripción: {order.description}")


def change_order_status_cli(mediator):
    """Permite actualizar el estado de un pedido desde CLI"""
    print("\n--- ACTUALIZAR ESTADO DE PEDIDO ---")
    order_id = input("ID del pedido: ").strip()
    new_status = input(f"Nuevo estado ({ORDER_STATUS_PENDING}, {ORDER_STATUS_CONFIRMED}, {ORDER_STATUS_SHIPPED}, {ORDER_STATUS_DELIVERED}, {ORDER_STATUS_CANCELLED}): ").strip()
    if not order_id.isdigit():
        print("ID inválido")
        return
    success, message = mediator.order_service.update_order_status(int(order_id), new_status)
    if success:
        print(f"✓ {message}")
    else:
        print(f"❌ {message}")


def list_users_cli(mediator):
    """Lista todos los usuarios en modo CLI"""
    print("\n--- LISTA DE USUARIOS ---")
    
    users = mediator.user_repository.find_all()
    
    if not users:
        print("No hay usuarios registrados")
        return
    
    print(f"\nTotal de usuarios: {len(users)}\n")
    for user in users:
        print(f"  ID: {user.id} | Usuario: {user.username:<15} | " + 
              f"Email: {user.email:<25} | Rol: {user.role}")


def main():
    """
    Función principal
    Detecta si PyQt6 está disponible para usar GUI
    Si no, ejecuta el modo CLI
    """
    print("=" * 60)
    print("🚀 Gestor de Pedidos - Inicialización")
    print("=" * 60)
    
    # Verificar si PyQt6 está disponible
    try:
        import PyQt6
        print("✅ PyQt6 disponible - Modo GUI activado\n")
        run_gui()
    except ImportError:
        print("⚠️  PyQt6 no disponible - Usando modo CLI\n")
        run_cli()


if __name__ == "__main__":
    main()
