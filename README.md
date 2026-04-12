# 🎯 Gestor de Pedidos - Clean Architecture

Aplicación moderna de escritorio para gestión de pedidos con interfaz gráfica oscura y arquitectura limpia.

## ✨ Características

- 🎨 **GUI Moderna**: Interfaz oscura profesional con PyQt6
- 🔐 **Autenticación**: Login y registro con 3 tipos de roles
- 👥 **3 Tipos de Usuarios**: Admin, Gerente, Cliente
- 📦 **Gestión de Pedidos**: Ver y crear pedidos
- 🏗️ **Clean Architecture**: Código organizado en capas desacopladas
- 💾 **Base de Datos**: SQLite con patrón Repositorio

## 🚀 Inicio Rápido

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar
```bash
python main.py
```

## 👥 Sistema de Roles

| Rol | Permisos |
|-----|----------|
| **Admin** | Acceso total, ve todos los usuarios |
| **Gerente** | Gestiona pedidos, ve usuarios |
| **Cliente** | Solo ve sus propios datos |

**Nota**: Solo admin puede crear otras cuentas de admin/gerente. Nuevos registros se crean como cliente por seguridad.

## 📁 Estructura

```
DAE2026/
├── main.py                 # Punto de entrada
├── config.py              # Configuración
├── database/              # Modelos y conexión BD
├── repositories/          # Acceso a datos
├── services/              # Lógica de negocio
├── gui/                   # Interfaz gráfica
├── mediator/              # Inyección de dependencias
├── utils/                 # Utilidades y constantes
└── data/orders.db         # Base de datos
```

### Capas de la Aplicación

- **database/** - Capa de acceso a datos
  - Conexión a SQLite
  - Definición de modelos (User, Order)
  
- **repositories/** - Patrones de acceso a datos
  - Implementa CRUD para cada entidad
  - UserRepository, OrderRepository
  
- **services/** - Lógica de negocio
  - AuthService: Autenticación y validaciones
  - UserService: Operaciones con usuarios
  - OrderService: Operaciones con pedidos
  
- **gui/** - Interfaz gráfica
  - main_window.py: Ventana principal
  - login_window.py: Login y registro
  - styles.py: Estilos CSS oscuros
  
- **mediator/** - Coordinador de capas
  - Inyección de dependencias
  - Coordinación entre componentes
  
- **utils/** - Utilidades generales
  - Validadores de entrada
  - Funciones de seguridad
  - Constantes de la aplicación

## 📋 Procedimiento de Registro

1. Ejecuta: `python main.py`
2. Haz click en el botón **"Registrarse"**
3. Completa los campos:
   - **Nombre de usuario**: Mínimo 3 caracteres (letras, números, guiones)
   - **Correo electrónico**: Email válido
   - **Contraseña**: Mínimo 6 caracteres
   - **Tipo de usuario**: 
     - Cliente (acceso básico - recomendado)
     - Gerente (acceso intermedio - por seguridad se convierte a Cliente)
     - Admin (acceso total - por seguridad se convierte a Cliente)
4. Click en **"Registrarse"**
5. Se confirmará si fue exitoso

**Nota**: Por seguridad, nuevos registros se crean como Cliente. Solo Admin puede cambiar roles después.

## 📋 Procedimiento de Login

1. Ejecuta: `python main.py`
2. Ingresa tu **nombre de usuario**
3. Ingresa tu **contraseña**
4. Click en **"Iniciar Sesión"**
5. Si las credenciales son correctas:
   - Se abre el panel principal
   - Se muestra tu rol y permisos
   - Puedes navegar por las pestañas

## 🎨 Tema

- Fondo oscuro: `#1e1e1e`
- Azul principal: `#2196f3`
- Rojo peligro: `#d32f2f`
- Verde éxito: `#388e3c`

## 📋 Uso

1. **Ejecuta**: `python main.py`
2. **Registra** o **inicia sesión**
3. Navega por las pestañas del panel

### Usuarios de Prueba

```
Usuario: admin
Email: admin@example.com
Contraseña: admin123
Rol: Administrador
```

## 📖 Documentación

- `ARCHITECTURE.md` - Detalles de arquitectura
- `DIAGRAMS.py` - Visualizar diagramas
- `run.py` - Menú interactivo

## 🔧 Requisitos

- Python 3.8+
- PyQt6 (se instala con requirements.txt)

---

**Última actualización**: Abril 2026
