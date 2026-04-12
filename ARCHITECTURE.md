# 🏗️ Clean Architecture - Gestor de Pedidos

## Estructura del Proyecto

```
DAE2026/
├── main.py                    # 🎯 PUNTO DE ENTRADA ÚNICO
│                              # Detecta GUI vs CLI automáticamente
│
├── config.py                  # ⚙️ Configuración global
│
├── database/                  # 📦 CAPA DE DATOS
│   ├── connection.py         # Conexión a BD
│   ├── models.py             # Modelos de datos (Entidades)
│   └── __init__.py
│
├── repositories/              # 📚 CAPA DE REPOSITORIOS
│   ├── user_repository.py    # Acceso a datos de usuarios
│   ├── order_repository.py   # Acceso a datos de pedidos
│   └── __init__.py
│
├── services/                  # 🔧 CAPA DE LÓGICA DE NEGOCIO
│   ├── auth_service.py       # Autenticación
│   ├── user_service.py       # Operaciones de usuarios
│   ├── order_service.py      # Operaciones de pedidos
│   └── __init__.py
│
├── mediator/                  # 🔗 COORDINADOR CENTRAL
│   ├── app_mediator.py       # Inyección de dependencias
│   └── __init__.py
│
├── gui/                       # 🎨 CAPA DE PRESENTACIÓN (GUI)
│   ├── styles.py             # Estilos CSS oscuros
│   ├── login_window.py       # Ventana de login/registro
│   ├── main_window.py        # Ventana principal
│   └── __init__.py
│
├── utils/                     # 🛠️ UTILIDADES
│   ├── constants.py          # Constantes globales
│   ├── helpers.py            # Funciones auxiliares
│   ├── validators.py         # Validadores
│   └── __init__.py
│
├── requirements.txt           # 📋 Dependencias
├── README.md                  # Documentación principal
└── GUI_README.md             # Documentación de la GUI
```

## Principios de Clean Architecture Implementados

### 1. **Separación de Capas**
- **Capa de Datos**: `database/` - Gestiona BD y modelos
- **Capa de Repositorios**: `repositories/` - Acceso a datos abstraído
- **Capa de Servicios**: `services/` - Lógica de negocio pura
- **Capa de Presentación**: `gui/` - Interfaz de usuario
- **Mediador**: `mediator/` - Inyección de dependencias

### 2. **Inversión de Control (IoC)**
- El `AppMediator` gestiona todas las dependencias
- Los servicios reciben dependencias inyectadas
- Desacoplamiento total entre capas

### 3. **Punto de Entrada Único**
- `main.py` es el único punto de entrada
- Detecta automáticamente modo GUI o CLI
- Manejo centralizado de errores

### 4. **Responsabilidad Única**
- Cada clase tiene una única razón para cambiar
- Funciones pequeñas y específicas
- Separación clara de responsabilidades

### 5. **Independencia de Frameworks**
- Lógica de negocio pura (sin dependencias de GUI)
- Fácil cambiar de PyQt6 a otro framework
- Servicios reutilizables

## Flujo de Ejecución

```
main.py
  ├─ ¿PyQt6 disponible?
  │  ├─ SÍ → run_gui()
  │  │  ├─ QApplication (PyQt6)
  │  │  ├─ AppMediator
  │  │  └─ MainWindow
  │  │
  │  └─ NO → run_cli()
  │     ├─ AppMediator
  │     └─ Menú de consola
  │
  └─ AppMediator
     ├─ DatabaseConnection
     ├─ UserRepository
     ├─ OrderRepository
     ├─ AuthService
     ├─ UserService
     └─ OrderService
```

## Inicio de la Aplicación

### Modo Automático (Recomendado)
```bash
python main.py
```
- Detecta PyQt6 automáticamente
- Inicia GUI si está disponible
- Si no, usa CLI

### Modo GUI Explícito
```bash
python main.py --gui
```

### Modo CLI Explícito
```bash
python main.py --cli
```

## Ventajas de esta Arquitectura

✅ **Mantenibilidad**: Código organizado y fácil de modificar
✅ **Escalabilidad**: Agregar nuevas funcionalidades es simple
✅ **Testabilidad**: Componentes desacoplados, fáciles de probar
✅ **Reutilización**: Servicios reutilizables en múltiples interfaces
✅ **Flexibilidad**: Cambiar de GUI sin afectar la lógica
✅ **Claridad**: Cada archivo tiene un propósito claro

## Dependencias por Capa

```
Presentación (GUI)
    ↓ importa
Servicios (Lógica de Negocio)
    ↓ importa
Repositorios (Acceso a Datos)
    ↓ importa
Base de Datos (Persistencia)

⬆️ Las capas inferiores NO conocen de las superiores
⬇️ Las capas superiores SÍ conocen de las inferiores
```

## Próximos Pasos de Mejora

1. **Agregar Logging**: Sistema de logs centralizado
2. **Testing**: Tests unitarios para servicios
3. **Validación**: Más validadores en utils/
4. **Caché**: Sistema de caché en repositorios
5. **API REST**: Exponer servicios vía API
6. **Autenticación JWT**: Tokens para API
7. **Migrations**: Sistema de versionado de BD

---

**Clean Architecture = Código que crece sin enredarse 🎯**
