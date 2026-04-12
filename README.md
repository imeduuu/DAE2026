# Gestor de Pedidos - Aplicación Desktop

## Descripción
Aplicación de escritorio modular para gestión de pedidos con sistema de usuarios, autenticación y roles.

## Características
- ✓ Login y registro de usuarios
- ✓ Sistema de roles (Cliente y Administrador)
- ✓ Base de datos SQLite
- ✓ Arquitectura modular y escalable
- 🔄 Gestión de pedidos (próximamente)
- 🔄 Interfaz gráfica Tkinter (próximamente)

## Estructura del Proyecto

```
DAE2026/
├── gui/                    # Interfaz gráfica Tkinter
│   ├── __init__.py
│   ├── main_window.py
│   ├── login_window.py
│   └── dashboard.py
├── services/               # Lógica de negocio
│   ├── __init__.py
│   ├── auth_service.py
│   ├── order_service.py
│   └── user_service.py
├── repositories/           # Acceso a datos
│   ├── __init__.py
│   ├── user_repository.py
│   └── order_repository.py
├── database/              # Modelos y conexión
│   ├── __init__.py
│   ├── connection.py
│   ├── models.py
│   └── schema.sql
├── utils/                 # Funciones auxiliares
│   ├── __init__.py
│   ├── validators.py
│   ├── helpers.py
│   └── constants.py
├── mediator/              # Coordinador de capas
│   ├── __init__.py
│   └── app_mediator.py
├── data/                  # Base de datos SQLite
│   └── orders.db (generado al ejecutar)
├── main.py                # Punto de entrada
├── requirements.txt       # Dependencias
└── README.md             # Este archivo
```

## Principios de Arquitectura

### Separación de Capas
- **Database**: Conexión, modelos y persistencia
- **Repositories**: Acceso a datos (DAO pattern)
- **Services**: Lógica de negocio
- **GUI**: Interfaz de usuario (por implementar)
- **Mediator**: Coordinación entre capas

### Características de Diseño
- ✓ Inyección de dependencias
- ✓ Validaciones robustas
- ✓ Seguridad (hashing de contraseñas)
- ✓ Manejo de errores centralizado
- ✓ Código modular y reutilizable

## Instalación

### Requisitos
- Python 3.8+
- pip (gestor de paquetes)

### Paso 1: Clonar el repositorio
```bash
git clone <url-repositorio>
cd DAE2026
```

### Paso 2: Crear ambiente virtual (opcional pero recomendado)
```bash
# Windows
python -m venv venv
venv\\Scripts\\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

## Uso

### Ejecutar la aplicación
```bash
python main.py
```

### Opciones del menú principal
1. **Registrar nuevo usuario**: Crea una nueva cuenta
2. **Login**: Inicia sesión con usuario existente
3. **Ver usuarios**: Lista todos los usuarios (demuestra acceso a BD)
4. **Salir**: Cierra la aplicación

### Ejemplo de uso
```
1. Selecciona "Registrar nuevo usuario"
   - Usuario: juan
   - Email: juan@example.com
   - Contraseña: password123
   - Rol: Cliente

2. Selecciona "Login"
   - Usuario: juan
   - Contraseña: password123
   → ¡Login exitoso!
```

## Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje de programación
- **SQLite3**: Base de datos
- **Tkinter**: Framework GUI (próximamente)
- **Dataclasses**: Modelos de datos

## Próximos Pasos para Desarrollo

1. Implementar interfaz gráfica Tkinter
2. Crear servicio y repository de pedidos
3. Agregar gestión de pedidos (CRUD completo)
4. Implementar dashboard para usuarios
5. Agregar exportación de datos (PDF, CSV)
6. Mejorar validaciones y seguridad
7. Agregar logging centralizado
8. Crear pruebas unitarias

## Estructura de Carpetas Detallada

### `database/`
- **connection.py**: Gestiona conexión SQLite y contextos
- **models.py**: Define modelos de datos (User, Order)

### `repositories/`
- **user_repository.py**: CRUD de usuarios
- **order_repository.py**: CRUD de pedidos (por completar)

### `services/`
- **auth_service.py**: Autenticación y registro
- **user_service.py**: Gestión de usuario (por completar)
- **order_service.py**: Gestión de pedidos (por completar)

### `gui/`
- **main_window.py**: Ventana principal (por implementar)
- **login_window.py**: Ventana de login (por implementar)
- **dashboard.py**: Dashboard de usuario (por implementar)

### `utils/`
- **validators.py**: Validaciones de entrada
- **helpers.py**: Funciones de seguridad
- **constants.py**: Constantes de la aplicación

## Modelado de Datos

### User
- id: INT (PK)
- username: TEXT (UNIQUE)
- email: TEXT (UNIQUE)
- password_hash: TEXT
- role: TEXT ('cliente' o 'administrador')
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

### Order
- id: INT (PK)
- user_id: INT (FK)
- description: TEXT
- status: TEXT ('pendiente', 'confirmado', 'enviado', 'entregado', 'cancelado')
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

## Contribuciones

Para contribuir al proyecto:
1. Crea una rama nueva (`git checkout -b feature/nombre-feature`)
2. Realiza tus cambios
3. Haz commit (`git commit -m 'Agrega feature'`)
4. Sube tu rama (`git push origin feature/nombre-feature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo licencia MIT.

---

**Última actualización**: Abril 2026
**Estado**: Desarrollo inicial
