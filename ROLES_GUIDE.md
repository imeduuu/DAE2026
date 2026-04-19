# 👥 Sistema de Roles - Guía Completa

## 3 Tipos de Roles

### 1. 👨‍💼 ADMINISTRADOR (Admin)
**Nivel de acceso**: Máximo (3)

**Permisos:**
- ✅ Ver todos los usuarios registrados
- ✅ Ver todos los pedidos
- ✅ Crear, editar y eliminar usuarios
- ✅ Crear, editar y eliminar pedidos
- ✅ Cambiar roles de usuarios
- ✅ Ver estadísticas generales

**Cómo crear un Admin:**
- Solo otro Admin puede crear cuentas Admin
- En el registro, selecciona "Administrador"
- El sistema valida que sea autorizado

---

### 2. 📊 GERENTE (Manager)
**Nivel de acceso**: Intermedio (2)

**Permisos:**
- ✅ Ver usuarios del sistema
- ✅ Ver todos los pedidos
- ✅ Crear y editar pedidos
- ✅ Generar reportes
- ❌ Crear otros Gerentes o Admins
- ❌ Eliminar usuarios

**Cómo crear un Gerente:**
- Solo Admin puede asignar rol Gerente
- En el registro, selecciona "Gerente"
- El sistema lo convierte a Cliente por seguridad
- Admin debe cambiar manualmente desde la BD

---

### 3. 👤 CLIENTE (Client)
**Nivel de acceso**: Básico (1)

**Permisos:**
- ✅ Ver sus propios datos
- ✅ Ver sus propios pedidos
- ✅ Crear pedidos
- ❌ Ver otros usuarios
- ❌ Ver pedidos de otros
- ❌ Crear usuarios

**Cómo crear un Cliente:**
- Cualquiera puede registrarse como Cliente
- Es el rol por defecto
- Opción más segura para nuevos usuarios

---

## 🔐 Seguridad en Asignación de Roles

### Restricciones Implementadas

```
┌─────────────────────────────────────┐
│   INTENTO DE REGISTRO               │
├─────────────────────────────────────┤
│                                     │
│  ¿Seleccionó Admin o Gerente?       │
│    ├─ SÍ → Se crea como CLIENTE     │
│    │        (Validación de seguridad)│
│    └─ NO → Se crea normalmente      │
│            con rol seleccionado      │
└─────────────────────────────────────┘
```

### Protecciones

✅ **Prevención de escalada**: Nuevos usuarios no pueden ser Admin/Gerente
✅ **Validación de identidad**: Solo Admin puede cambiar roles
✅ **Auditoría**: Se registra quién cambió qué rol
✅ **Contraseña encriptada**: Máxima seguridad

---

## 📝 Cómo Asignar/Cambiar Roles

### Opción 1: Mediante Registro
1. Click en "Registrarse"
2. Completa los datos
3. Selecciona rol en el ComboBox:
   - Cliente (por defecto)
   - Gerente (no permite)
   - Admin (no permite)
4. Click "Registrarse" → Se crea como **Cliente** (por seguridad)

### Opción 2: Admin Cambia Rol (En BD)
Para usuarios ya registrados:

```sql
-- Cambiar a Gerente
UPDATE users SET role = 'gerente' WHERE username = 'juan';

-- Cambiar a Admin
UPDATE users SET role = 'administrador' WHERE username = 'juan';

-- Cambiar a Cliente
UPDATE users SET role = 'cliente' WHERE username = 'juan';
```

### Opción 3: Desde Panel Admin (GUI) ✅ IMPLEMENTADO
Ahora disponible en la pestaña "⚙️ Gestión de Roles":

**Pasos:**
1. Inicia sesión como Administrador
2. En la barra de navegación, haz click en "⚙️ Gestión de Roles"
3. Verás una tabla con todos los usuarios (ID, Usuario, Email, Rol, Fecha)
4. Usar la búsqueda para filtrar por usuario, email o rol
5. Click en "Cambiar Rol" para seleccionar el nuevo rol
6. Confirmar el cambio (se solicita confirmación adicional)
7. Se registra automáticamente en logs (data/audit.log)

**Validaciones de Seguridad:**
- ✅ No puedes cambiar tu propio rol
- ✅ No se puede dejar sin Administrador (mínimo 1 activo)
- ✅ Se confirma antes de aplicar cambios
- ✅ Se registra en auditoría quién cambió qué rol y cuándo
- ✅ Campo opcional de motivo del cambio

---

## 📊 Tabla de Permisos por Rol

| Funcionalidad | Admin | Gerente | Cliente |
|---|---|---|---|
| Ver dashboard | ✅ | ✅ | ✅ |
| Ver sus datos | ✅ | ✅ | ✅ |
| Ver todos usuarios | ✅ | ✅ | ❌ |
| Crear usuario | ✅ | ❌ | ❌ |
| Editar usuario | ✅ | ❌ | ❌ |
| Eliminar usuario | ✅ | ❌ | ❌ |
| Cambiar roles | ✅ | ❌ | ❌ |
| Ver todos pedidos | ✅ | ✅ | ❌ |
| Ver sus pedidos | ✅ | ✅ | ✅ |
| Crear pedido | ✅ | ✅ | ✅ |
| Editar pedido | ✅ | ✅ | Solo propio |
| Eliminar pedido | ✅ | ❌ | ❌ |
| Ver reportes | ✅ | ✅ | ❌ |
| Exportar datos | ✅ | ✅ | ❌ |

---

## 🎯 Flujo Recomendado

### Primer Usuario (Administrador)
```
1. Ejecuta: python main.py
2. Click "Registrarse"
3. Datos:
   - Usuario: admin
   - Email: admin@example.com
   - Contraseña: admin123
   - Rol: Administrador
4. Sistema lo detecta como primer usuario
5. Se crea como ADMIN (excepción)
```

### Segundo Usuario (Gerente)
```
1. Admin inicia sesión
2. Va a: Usuarios → Crear
3. Datos del usuario
4. Asigna rol: Gerente
5. Click "Crear" → Se asigna Gerente
```

### Tercero en Adelante (Cliente)
```
1. Cualquiera puede registrarse
2. Click "Registrarse"
3. Se crea como Cliente por defecto
4. Admin puede cambiar rol si es necesario
```

---

## 🔍 Ver Rol de Usuarios

### En la GUI
```
Panel Principal
  ├─ Información usuario (arriba derecha)
  │  └─ Muestra: "👤 username (rol)"
  └─ Pestaña "Usuarios"
     └─ Tabla con rol de cada usuario
```

### En la Base de Datos
```sql
-- Ver todos los usuarios con su rol
SELECT id, username, email, role, created_at FROM users;

-- Contar usuarios por rol
SELECT role, COUNT(*) FROM users GROUP BY role;
```

---

## ⚠️ Consideraciones Importantes

1. **Seguridad**: Los nuevos registros siempre son Cliente
   - Previene ataques de escalada
   - Solo Admin puede promover usuarios

2. **Primera Ejecución**: El primer admin se crea directamente
   - Sin esta excepción, nadie podría crear el primer admin
   - Excepción de seguridad justificada

3. **Cambios de Rol**: Requieren autenticación
   - Se registran en auditoría (próximamente)
   - Validación de permisos en cada operación

4. **Eliminación**: Los admins no se pueden eliminar fácilmente
   - Validación para mantener al menos 1 admin
   - Implementado en próxima versión

---

## 💡 Tips de Uso

✓ **Crea primero un admin** para controlar el sistema
✓ **Promueve usuarios confiables** a Gerente
✓ **Mantén la mayoría como Cliente** (menos riesgos)
✓ **Revisa regularmente** la lista de usuarios
✓ **Cambia contraseñas** de cuentas no usadas

---

**Para más información**, revisa:
- `README.md` - Inicio rápido
- `ARCHITECTURE.md` - Detalles técnicos
- `GUI_README.md` - Guía de interfaz
