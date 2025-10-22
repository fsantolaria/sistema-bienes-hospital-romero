# 🏗️ Arquitectura del Backend - Sistema de Bienes Patrimoniales

## 📊 Diagrama de Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENTE                               │
│                    (Navegador Web)                           │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    DJANGO APPLICATION                        │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │   URLs     │  │   Views    │  │  Templates │            │
│  │ (Routing)  │→ │  (Logic)   │→ │   (HTML)   │            │
│  └────────────┘  └─────┬──────┘  └────────────┘            │
│                        │                                     │
│                        ▼                                     │
│  ┌────────────────────────────────────────────┐             │
│  │           Models (ORM)                     │             │
│  │  • BienPatrimonial                         │             │
│  │  • Expediente                              │             │
│  │  • Usuario                                 │             │
│  │  • Operador                                │             │
│  └──────────────────┬─────────────────────────┘             │
└────────────────────┼─────────────────────────────────────────┘
                     │ SQL
                     ▼
         ┌──────────────────────┐
         │   SQLite Database    │
         │     db.sqlite3       │
         └──────────────────────┘
```

---

## 🗂️ Diagrama de Modelos de Datos

```
┌──────────────────────────────────────────────────────────────┐
│                     USUARIO (AbstractUser)                    │
├──────────────────────────────────────────────────────────────┤
│ PK │ id                                                       │
│    │ username                                                 │
│    │ email                                                    │
│    │ password                                                 │
│    │ tipo_usuario (admin/empleado)                           │
│    │ groups                                                   │
│    │ user_permissions                                         │
└────┬─────────────────────────────────────────────────────────┘
     │ 1:1
     │
┌────▼─────────────────────────────────────────────────────────┐
│                        OPERADOR                               │
├──────────────────────────────────────────────────────────────┤
│ PK │ id                                                       │
│ FK │ usuario_id                                               │
│    │ nombre_completo                                          │
│    │ telefono                                                 │
│    │ direccion                                                │
│    │ fecha_creacion                                           │
│    │ fecha_actualizacion                                      │
└──────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────┐
│                        EXPEDIENTE                             │
├──────────────────────────────────────────────────────────────┤
│ PK │ id                                                       │
│    │ numero_expediente (unique)                               │
│    │ organismo_origen                                         │
│    │ numero_compra                                            │
│    │ proveedor                                                │
└────┬─────────────────────────────────────────────────────────┘
     │ 1:N
     │
┌────▼─────────────────────────────────────────────────────────┐
│                    BIEN PATRIMONIAL                           │
├──────────────────────────────────────────────────────────────┤
│ PK │ clave_unica (BigAutoField)                               │
│ FK │ expediente_id (nullable)                                 │
│    │                                                           │
│    │ -- Datos principales --                                  │
│    │ nombre                                                    │
│    │ descripcion                                               │
│    │ cantidad                                                  │
│    │                                                           │
│    │ -- Clasificación --                                      │
│    │ cuenta_codigo                                             │
│    │ nomenclatura_bienes                                       │
│    │ servicios                                                 │
│    │                                                           │
│    │ -- Estado --                                             │
│    │ origen (COMPRA/DONACION/TRANSFERENCIA/OMISION)          │
│    │ estado (ACTIVO/MANTENIMIENTO/INACTIVO/BAJA)             │
│    │                                                           │
│    │ -- Identificadores --                                    │
│    │ numero_serie                                              │
│    │ numero_identificacion (unique)                            │
│    │                                                           │
│    │ -- Económico --                                          │
│    │ valor_adquisicion                                         │
│    │                                                           │
│    │ -- Fechas --                                             │
│    │ fecha_adquisicion                                         │
│    │ fecha_baja                                                │
│    │                                                           │
│    │ -- Información de baja --                                │
│    │ expediente_baja                                           │
│    │ descripcion_baja                                          │
│    │ observaciones                                             │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Datos - CRUD de Bienes

### 1. Crear Bien (Carga Masiva)

```
[Excel File] 
    │
    ▼
┌──────────────────┐
│ Vista:           │
│ carga_masiva_    │
│ bienes()         │
└────┬─────────────┘
     │ 1. Valida archivo
     │ 2. Lee con pandas
     │ 3. Normaliza datos
     ▼
┌──────────────────┐
│ Procesa cada     │
│ fila del Excel   │
└────┬─────────────┘
     │ Para cada fila:
     │ • Mapea valores
     │ • Valida datos
     │ • Crea/Actualiza Expediente
     ▼
┌──────────────────┐
│ Modelo:          │
│ BienPatrimonial  │
│ .update_or_      │
│  create()        │
└────┬─────────────┘
     │
     ▼
[Base de Datos]
     │
     ▼
[Redirección a /lista-bienes/]
```

### 2. Leer Bienes (Lista con Filtros)

```
[Request: GET /lista-bienes/?q=monitor&f_estado=ACTIVO]
    │
    ▼
┌──────────────────┐
│ Vista:           │
│ lista_bienes()   │
└────┬─────────────┘
     │ 1. Obtiene parámetros GET
     │ 2. Construye QuerySet
     ▼
┌──────────────────┐
│ QuerySet con:    │
│ • select_related │
│ • Q() filters    │
│ • order_by()     │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Base de Datos    │
│ Ejecuta SQL      │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Template:        │
│ lista_bienes.html│
└────┬─────────────┘
     │
     ▼
[HTML Response con tabla de bienes]
```

### 3. Actualizar Bien

```
[Request: POST /bienes/5/editar/]
    │
    ▼
┌──────────────────┐
│ Vista:           │
│ editar_bien(pk)  │
└────┬─────────────┘
     │ 1. get_object_or_404()
     │ 2. Valida formulario
     ▼
┌──────────────────┐
│ Form:            │
│ BienPatrimonial  │
│ Form             │
└────┬─────────────┘
     │ clean()
     │ validate()
     ▼
┌──────────────────┐
│ Modelo:          │
│ bien.save()      │
└────┬─────────────┘
     │
     ▼
[Base de Datos: UPDATE]
     │
     ▼
[Redirección + mensaje de éxito]
```

### 4. Eliminar Bien

```
[Request: POST /bienes/5/eliminar/]
    │
    ▼
┌──────────────────┐
│ Vista:           │
│ eliminar_bien()  │
└────┬─────────────┘
     │ 1. get_object_or_404()
     │ 2. bien.delete()
     ▼
[Base de Datos: DELETE]
     │
     ▼
[Redirección + mensaje]
```

---

## 🔐 Flujo de Autenticación

```
[Login Form]
    │ usuario + contraseña
    ▼
┌──────────────────┐
│ Vista:           │
│ login_view()     │
└────┬─────────────┘
     │ 1. authenticate()
     │ 2. Verifica credenciales
     ▼
┌──────────────────┐
│ Django Auth      │
│ Backend          │
└────┬─────────────┘
     │ Success?
     ├── NO ──► [Error message + retry]
     │
     └── SÍ ──▼
┌──────────────────┐
│ login(request,   │
│       user)      │
└────┬─────────────┘
     │ Crea sesión
     ▼
┌──────────────────┐
│ Verifica rol:    │
│ • admin →        │
│   home_admin     │
│ • empleado →     │
│   operadores     │
└────┬─────────────┘
     │
     ▼
[Redirección al dashboard correspondiente]
     │
     ▼
[Cookie: sessionid creada]
```

---

## 🔄 Flujo de Sistema de Bajas

```
[Bien ACTIVO]
    │
    ▼
[POST /bienes/5/dar-baja/]
    │ fecha_baja
    │ expediente_baja
    │ descripcion_baja
    ▼
┌──────────────────┐
│ Vista:           │
│ dar_baja_bien()  │
└────┬─────────────┘
     │ 1. Cambia estado a BAJA
     │ 2. Guarda datos de baja
     ▼
[Bien BAJA]
    │
    ├──► [Listado en /bienes/bajas/]
    │
    ├──► [POST /bienes/5/restablecer/]
    │    │
    │    ▼
    │    [Bien ACTIVO nuevamente]
    │
    └──► [POST /bienes/5/eliminar-definitivo/]
         │
         ▼
         [Eliminación física - NO REVERSIBLE]
```

---

## 📦 Estructura de Paquetes

```
sistema_bienes/
│
├── settings/              # Configuraciones
│   ├── base.py           # Config base
│   ├── development.py    # Dev
│   ├── testing.py        # Testing
│   └── production.py     # Producción
│
├── urls.py               # URLs principales
├── wsgi.py              # WSGI server
└── admin.py             # Admin customizado

core/                     # App principal
│
├── models/              # Modelos de datos
│   ├── bien_patrimonial.py
│   ├── expediente.py
│   ├── usuario.py
│   └── operador.py
│
├── views.py             # Lógica de negocio
├── urls.py              # URLs de la app
├── forms.py             # Formularios
├── admin.py             # Configuración admin
├── constants.py         # Constantes
└── tests/               # Tests unitarios
```

---

## 🔧 Componentes Clave

### 1. ORM (Object-Relational Mapping)

Django ORM traduce operaciones Python a SQL:

```python
# Python
bienes = BienPatrimonial.objects.filter(estado='ACTIVO')

# SQL generado
SELECT * FROM core_bienpatrimonial WHERE estado = 'ACTIVO';
```

### 2. Middleware Stack

```
Request ──┐
          │
          ├─► SecurityMiddleware (seguridad)
          │
          ├─► SessionMiddleware (sesiones)
          │
          ├─► CommonMiddleware (procesamiento común)
          │
          ├─► CsrfViewMiddleware (CSRF protection)
          │
          ├─► AuthenticationMiddleware (autenticación)
          │
          ├─► MessageMiddleware (mensajes flash)
          │
          └─► ClickjackingMiddleware (anti-clickjacking)
                │
                ▼
              [View]
                │
                ▼
             Response
```

### 3. Template Engine

```
Vista (Context Data)
        │
        ▼
┌─────────────────┐
│ Django Template │
│     Engine      │
└────────┬────────┘
         │ Renderiza con:
         │ • Variables: {{ variable }}
         │ • Tags: {% tag %}
         │ • Filters: {{ var|filter }}
         ▼
      [HTML]
```

---

## 🚀 Ciclo de Request/Response

```
1. [Browser] ──HTTP Request──► [Django URLs]
                                      │
2.                                    │ URL matching
                                      ▼
                              [View Function]
                                      │
3.                                    │ Procesa lógica
                                      │ Consulta DB si es necesario
                                      ▼
                              [Context Data]
                                      │
4.                                    │ Renderiza
                                      ▼
                              [Template]
                                      │
5.                                    │ HTML generado
                                      ▼
   [Browser] ◄──HTTP Response──  [Response]
```

---

## 📈 Optimizaciones Implementadas

### 1. Database Queries

```python
# Uso de select_related() para evitar N+1 queries
bienes = BienPatrimonial.objects.select_related("expediente")

# Esto genera:
# SELECT * FROM core_bienpatrimonial 
# LEFT JOIN core_expediente ON ...
# (1 query en vez de N+1)
```

### 2. Índices de Base de Datos

```python
class Meta:
    indexes = [
        models.Index(fields=['clave_unica']),
        models.Index(fields=['estado']),
    ]
```

### 3. Transacciones Atómicas

```python
@transaction.atomic
def operacion_critica():
    # Si algo falla, hace rollback automático
    pass
```

---

## 🔍 Patrones de Diseño Utilizados

### 1. MVT (Model-View-Template)
- **Model**: Lógica de datos y BD
- **View**: Lógica de negocio
- **Template**: Presentación

### 2. Repository Pattern (implícito en ORM)
- Abstracción de acceso a datos
- `objects.filter()`, `objects.get()`, etc.

### 3. Decorator Pattern
- `@login_required`
- `@require_POST`
- `@transaction.atomic`

### 4. Factory Pattern (Forms)
- Django Forms genera HTML y valida datos

---

## 📚 Referencias

- **Django Documentation**: https://docs.djangoproject.com/
- **Django ORM**: https://docs.djangoproject.com/en/4.2/topics/db/
- **Django Views**: https://docs.djangoproject.com/en/4.2/topics/http/views/
- **Django Security**: https://docs.djangoproject.com/en/4.2/topics/security/

---

**Última actualización**: Octubre 2024
