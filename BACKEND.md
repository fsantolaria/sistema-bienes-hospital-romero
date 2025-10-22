# 🔧 Documentación del Backend - Sistema de Gestión de Bienes Patrimoniales

## 📋 Tabla de Contenidos
1. [Arquitectura General](#arquitectura-general)
2. [Stack Tecnológico](#stack-tecnológico)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Modelos de Datos](#modelos-de-datos)
5. [Vistas y URLs](#vistas-y-urls)
6. [Autenticación y Permisos](#autenticación-y-permisos)
7. [Base de Datos](#base-de-datos)
8. [Configuración del Backend](#configuración-del-backend)
9. [API Endpoints](#api-endpoints)

---

## 🏗️ Arquitectura General

El backend del sistema está construido con **Django 4.2.7** siguiendo el patrón **MVT (Model-View-Template)**. La arquitectura está diseñada para ser modular, escalable y mantenible.

### Características Principales:
- ✅ **Separación de ambientes**: Development, Testing, Production
- ✅ **Gestión de configuración**: Variables de entorno con python-decouple
- ✅ **ORM Django**: Abstracción de base de datos
- ✅ **Autenticación personalizada**: Sistema de usuarios con roles
- ✅ **Admin personalizado**: Interfaz administrativa mejorada
- ✅ **Validaciones robustas**: A nivel de modelo y formulario
- ✅ **Carga masiva de datos**: Importación desde Excel

---

## 💻 Stack Tecnológico

### Core Framework
```
Django==4.2.7               # Framework web principal
python-decouple==3.8        # Gestión de configuración
whitenoise==6.6.0          # Servir archivos estáticos
```

### Forms y UI
```
django-crispy-forms==2.0    # Formularios mejorados
crispy_bootstrap5           # Integración Bootstrap 5
django-filter==23.3         # Filtros avanzados
```

### Procesamiento de Datos
```
Pillow                      # Procesamiento de imágenes
pandas                      # Análisis y manipulación de datos
openpyxl                    # Lectura/escritura de Excel
```

### Base de Datos
```
SQLite3                     # Base de datos (todos los ambientes)
```

---

## 📁 Estructura del Proyecto

```
sistema-bienes-hospital-romero/
│
├── sistema_bienes/              # Proyecto Django principal
│   ├── __init__.py
│   ├── admin.py                # Admin site personalizado
│   ├── asgi.py                 # Configuración ASGI
│   ├── wsgi.py                 # Configuración WSGI
│   ├── urls.py                 # URLs principales
│   └── settings/               # Configuraciones por ambiente
│       ├── __init__.py
│       ├── base.py            # Configuración base
│       ├── development.py     # Desarrollo
│       ├── testing.py         # Testing
│       └── production.py      # Producción
│
├── core/                       # Aplicación principal
│   ├── models/                # Modelos de datos
│   │   ├── __init__.py
│   │   ├── bien_patrimonial.py    # Modelo principal
│   │   ├── expediente.py          # Expedientes
│   │   ├── usuario.py             # Usuarios custom
│   │   └── operador.py            # Operadores del sistema
│   ├── migrations/            # Migraciones de BD
│   ├── admin.py              # Configuración del admin
│   ├── views.py              # Lógica de vistas
│   ├── urls.py               # URLs de la app
│   ├── forms.py              # Formularios
│   ├── constants.py          # Constantes del sistema
│   └── tests/                # Tests unitarios
│
├── templates/                 # Plantillas HTML
├── static/                    # Archivos estáticos
├── media/                     # Archivos subidos
├── logs/                      # Archivos de log
├── requirements/              # Dependencias
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── enviroment/               # Archivos .env de ejemplo
├── manage.py                 # CLI de Django
└── db.sqlite3               # Base de datos SQLite
```

---

## 🗄️ Modelos de Datos

### 1. BienPatrimonial

**Archivo**: `core/models/bien_patrimonial.py`

Modelo principal del sistema que representa un bien patrimonial del hospital.

```python
class BienPatrimonial(models.Model):
    # Identificador único
    clave_unica = models.BigAutoField(primary_key=True)
    
    # Datos principales
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    cantidad = models.PositiveIntegerField(default=1)
    
    # Relaciones
    expediente = models.ForeignKey('Expediente', on_delete=models.SET_NULL, 
                                   null=True, blank=True)
    
    # Clasificación
    cuenta_codigo = models.CharField(max_length=20, blank=True)
    nomenclatura_bienes = models.CharField(max_length=200, blank=True)
    
    # Fechas
    fecha_adquisicion = models.DateField(null=True, blank=True)
    fecha_baja = models.DateField(null=True, blank=True)
    
    # Estado y origen
    origen = models.CharField(max_length=15, choices=ORIGEN_CHOICES)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES)
    
    # Identificadores adicionales
    numero_serie = models.CharField(max_length=100, blank=True)
    numero_identificacion = models.CharField(max_length=50, unique=True, 
                                            null=True, blank=True)
    
    # Valor económico
    valor_adquisicion = models.DecimalField(max_digits=12, decimal_places=2,
                                           null=True, blank=True)
    
    # Información complementaria
    servicios = models.CharField(max_length=200, blank=True)
    observaciones = models.TextField(blank=True)
    
    # Información de baja
    expediente_baja = models.CharField(max_length=100, null=True, blank=True)
    descripcion_baja = models.TextField(blank=True)
```

**Constantes de Estado**:
- `ACTIVO`: Bien en uso
- `MANTENIMIENTO`: En reparación
- `INACTIVO`: Fuera de servicio
- `BAJA`: Dado de baja

**Constantes de Origen**:
- `COMPRA`: Adquirido por compra
- `DONACION`: Recibido como donación
- `TRANSFERENCIA`: Transferido desde otra área
- `OMISION`: Registro de omisión anterior

**Validaciones**:
- `clean()`: Valida precio no negativo, fecha no futura, precio solo si origen es COMPRA
- Índices en: `clave_unica`, `estado`

---

### 2. Expediente

**Archivo**: `core/models/expediente.py`

Representa un expediente administrativo asociado a compras o trámites.

```python
class Expediente(models.Model):
    numero_expediente = models.CharField(max_length=50, unique=True)
    organismo_origen = models.CharField(max_length=120, blank=True)
    numero_compra = models.CharField(max_length=50, blank=True)
    proveedor = models.CharField(max_length=200, blank=True)
```

**Relaciones**:
- Un expediente puede tener múltiples bienes patrimoniales (`bienes`)

---

### 3. Usuario

**Archivo**: `core/models/usuario.py`

Modelo de usuario personalizado que extiende AbstractUser de Django.

```python
class Usuario(AbstractUser):
    TIPO_USUARIO = [
        ('admin', 'Administrador'),
        ('empleado', 'Empleado Hospital'),
    ]
    
    tipo_usuario = models.CharField(max_length=10, 
                                   choices=TIPO_USUARIO, 
                                   default='empleado')
```

**Características**:
- Hereda campos de `AbstractUser`: username, email, password, etc.
- Campo adicional `tipo_usuario` para roles
- Gestión de grupos y permisos personalizada

---

### 4. Operador

**Archivo**: `core/models/operador.py`

Perfil extendido para usuarios operadores del sistema.

```python
class Operador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=300, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
```

**Properties**:
- `email`: Retorna el email del usuario asociado
- `username`: Retorna el username del usuario asociado

---

## 🌐 Vistas y URLs

### Arquitectura de Vistas

El sistema utiliza **vistas basadas en funciones (FBV)** con decoradores para control de acceso.

**Archivo principal**: `core/views.py`

### Categorías de Vistas

#### 1. Autenticación

```python
# Login/Logout
path('login/', views.login_view, name='login')
path('logout/', views.logout_view, name='logout')
path('registro/', views.registro, name='registro')
path('recuperar-password/', views.recuperar_password, name='recuperar_password')
```

**Funcionalidad de Login**:
- Verifica si el usuario ya está autenticado
- Usa `authenticate()` de Django
- Previene redirecciones infinitas con validación de `next`
- Redirige según rol (admin/operador)

#### 2. Dashboards

```python
# Dashboards protegidos con @login_required
path('home_admin/', views.home_admin, name='home_admin')
path('operadores/', views.operadores, name='operadores')
```

**Control de acceso**:
- `home_admin`: Solo para usuarios admin o superusuarios
- `operadores`: Acceso general para usuarios autenticados

#### 3. Gestión de Bienes (CRUD)

**Lista y Búsqueda**:
```python
path('lista-bienes/', views.lista_bienes, name='lista_bienes')
```

**Funcionalidades de lista_bienes**:
- Búsqueda por múltiples campos (Q objects)
- Filtros: origen, estado, rango de fechas
- Ordenamiento: fecha, precio, clave
- Paginación automática
- Uso de `select_related()` para optimización

**Edición y Eliminación**:
```python
path('bienes/<int:pk>/editar/', views.editar_bien, name='editar_bien')
path('bienes/<int:pk>/eliminar/', views.eliminar_bien, name='eliminar_bien')
path('bienes/eliminar-seleccionados/', views.eliminar_bienes_seleccionados, 
     name='eliminar_bienes_seleccionados')
```

#### 4. Carga Masiva

```python
path('carga-masiva/', views.carga_masiva_bienes, name='carga_masiva')
```

**Proceso de carga masiva**:
1. Lectura de archivo Excel con pandas
2. Normalización de nombres de columnas
3. Mapeo de valores (origen, estado)
4. Parseo de fechas y montos
5. Creación/actualización con `update_or_create()`
6. Manejo de transacciones atómicas
7. Reporte de errores detallado

**Campos soportados**:
- N° de ID, N° de Expediente, N° de Compra
- N° de Serie, Descripción, Cantidad
- Servicios, Cuenta Código, Nomenclatura
- Origen, Estado, Precio
- Fecha de Alta, Fecha de Baja
- Observaciones

#### 5. Sistema de Bajas

```python
path('bienes/bajas/', views.lista_baja_bienes, name='lista_baja_bienes')
path('bienes/<int:pk>/dar-baja/', views.dar_baja_bien, name='dar_baja_bien')
path('bienes/<int:pk>/restablecer/', views.restablecer_bien, name='restablecer_bien')
path('bienes/<int:pk>/eliminar-definitivo/', views.eliminar_bien_definitivo, 
     name='eliminar_bien_definitivo')
```

**Workflow de bajas**:
1. **Dar de baja**: Cambia estado a BAJA, registra fecha, expediente y motivo
2. **Lista de bajas**: Muestra solo bienes con estado BAJA
3. **Restablecer**: Vuelve el bien a estado ACTIVO
4. **Eliminar definitivo**: Eliminación física de la BD (no reversible)

---

## 🔐 Autenticación y Permisos

### Sistema de Autenticación

**Modelo de Usuario**: `Usuario (AbstractUser)`

**Configuración en settings**:
```python
AUTH_USER_MODEL = 'core.Usuario'  # Implícito por el modelo
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
```

### Decoradores de Protección

**@login_required**:
- Protege vistas que requieren autenticación
- Redirige a LOGIN_URL si no está autenticado
- Soporta parámetro `next` para redirección post-login

**@require_POST**:
- Asegura que la vista solo acepta método POST
- Usado en acciones destructivas (eliminar, dar de baja)

**@transaction.atomic**:
- Envuelve operaciones en transacción de BD
- Rollback automático en caso de error
- Usado en bajas y eliminaciones

### Control de Roles

```python
def _role_route_name(user) -> str:
    """Devuelve la ruta según el rol del usuario."""
    if hasattr(user, 'tipo_usuario'):
        return 'home_admin' if user.tipo_usuario == 'admin' else 'operadores'
    return 'home_admin' if user.is_superuser else 'operadores'
```

**Verificación en vistas**:
```python
@login_required
def home_admin(request):
    if hasattr(request.user, 'tipo_usuario'):
        if request.user.tipo_usuario != 'admin':
            messages.error(request, 'No tienes permisos')
            return redirect('operadores')
    elif not request.user.is_superuser:
        messages.error(request, 'No tienes permisos')
        return redirect('operadores')
    # ...
```

### Seguridad en Redirecciones

**Función de validación**:
```python
def _safe_next(request) -> str:
    """Devuelve un 'next' válido (mismo host) que NO apunte al login."""
    nxt = request.GET.get('next') or request.POST.get('next') or ''
    if not nxt:
        return ''
    if url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}):
        login_path = reverse('login')
        if nxt.startswith(login_path):
            return ''
        return nxt
    return ''
```

---

## 💾 Base de Datos

### Diagrama de Relaciones

```
┌─────────────────┐
│    Usuario      │
│ (AbstractUser)  │
└────────┬────────┘
         │ 1:1
         │
┌────────▼────────┐
│    Operador     │
│                 │
└─────────────────┘

┌─────────────────┐         ┌─────────────────┐
│   Expediente    │ 1:N     │ BienPatrimonial │
│                 ├────────▶│                 │
│ • numero_exp    │         │ • clave_unica   │
│ • org_origen    │         │ • nombre        │
│ • numero_compra │         │ • descripcion   │
│ • proveedor     │         │ • estado        │
└─────────────────┘         │ • origen        │
                            │ • fecha_alta    │
                            │ • fecha_baja    │
                            │ • valor         │
                            └─────────────────┘
```

### Migraciones

**Comando para crear migraciones**:
```bash
python manage.py makemigrations
```

**Comando para aplicar migraciones**:
```bash
python manage.py migrate
```

**Ver estado de migraciones**:
```bash
python manage.py showmigrations
```

### Índices y Optimización

**Índices definidos**:
- `BienPatrimonial.clave_unica`: Clave primaria con índice automático
- `BienPatrimonial.estado`: Índice para filtros frecuentes
- `BienPatrimonial.numero_identificacion`: Unique constraint

**Optimización de queries**:
```python
# Uso de select_related para JOINs eficientes
bienes = BienPatrimonial.objects.select_related("expediente")

# Filtros con Q objects para búsquedas complejas
bienes = bienes.filter(
    Q(clave_unica__icontains=q) |
    Q(descripcion__icontains=q) |
    Q(expediente__numero_expediente__icontains=q)
)
```

---

## ⚙️ Configuración del Backend

### Estructura de Settings

El proyecto usa **configuración por ambiente** con archivos separados:

**Base (`settings/base.py`)**:
- Configuración común a todos los ambientes
- INSTALLED_APPS, MIDDLEWARE, TEMPLATES
- Configuración de archivos estáticos y media
- Logging básico

**Development (`settings/development.py`)**:
```python
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

# Debug Toolbar (opcional)
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

**Testing (`settings/testing.py`)**:
```python
from .base import *

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_testing.sqlite3',
    }
}
```

**Production (`settings/production.py`)**:
```python
from .base import *

DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
SECRET_KEY = config('SECRET_KEY')

# Seguridad adicional
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Variables de Entorno

**Archivo**: `.env` (ejemplo en `enviroment/env_development`)

```bash
# Ambiente
DJANGO_ENV=development

# Seguridad
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True

# Base de datos (para producción con PostgreSQL/MySQL)
# DATABASE_URL=postgres://user:pass@localhost/dbname

# Hosts permitidos
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Logging

**Configuración en `base.py`**:
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(BASE_DIR, 'logs', 'app.log')),
        logging.StreamHandler()
    ]
)
```

**Ubicación de logs**: `logs/app.log`

---

## 🔌 API Endpoints

### Endpoints Disponibles

#### Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET/POST | `/login/` | Login de usuario | No |
| GET | `/logout/` | Logout de usuario | Sí |
| GET/POST | `/registro/` | Registro de usuario | No |
| GET | `/recuperar-password/` | Recuperar contraseña | No |

#### Dashboards

| Método | Endpoint | Descripción | Auth | Rol |
|--------|----------|-------------|------|-----|
| GET | `/home_admin/` | Dashboard admin | Sí | Admin |
| GET | `/operadores/` | Dashboard operadores | Sí | Cualquiera |

#### Bienes Patrimoniales

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/lista-bienes/` | Lista de bienes con filtros | Sí |
| GET | `/lista-bienes/?q=busqueda` | Búsqueda de bienes | Sí |
| GET | `/lista-bienes/?f_origen=COMPRA` | Filtrar por origen | Sí |
| GET | `/lista-bienes/?f_estado=ACTIVO` | Filtrar por estado | Sí |
| GET | `/lista-bienes/?f_desde=2023-01-01&f_hasta=2023-12-31` | Filtrar por fechas | Sí |
| GET/POST | `/bienes/<pk>/editar/` | Editar bien | Sí |
| POST | `/bienes/<pk>/eliminar/` | Eliminar bien | Sí |
| POST | `/bienes/eliminar-seleccionados/` | Eliminar múltiples | Sí |

#### Carga Masiva

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET/POST | `/carga-masiva/` | Cargar bienes desde Excel | Sí |

#### Sistema de Bajas

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/bienes/bajas/` | Lista de bienes dados de baja | Sí |
| POST | `/bienes/<pk>/dar-baja/` | Dar de baja un bien | Sí |
| POST | `/bienes/<pk>/restablecer/` | Restablecer bien dado de baja | Sí |
| POST | `/bienes/<pk>/eliminar-definitivo/` | Eliminar definitivamente | Sí |

#### Reportes

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/reportes/` | Generación de reportes | Sí |

### Parámetros de Query String

**Lista de bienes** (`/lista-bienes/`):
- `q`: Búsqueda general (texto)
- `f_origen`: Filtro por origen (COMPRA, DONACION, etc.)
- `f_estado`: Filtro por estado (ACTIVO, BAJA, etc.)
- `f_desde`: Fecha desde (YYYY-MM-DD)
- `f_hasta`: Fecha hasta (YYYY-MM-DD)
- `orden`: Ordenamiento (fecha, -fecha, precio, -precio)

**Lista de bajas** (`/bienes/bajas/`):
- `q`: Búsqueda general
- `orden`: Ordenamiento (fecha_baja, -fecha_baja, precio, -precio)

### Respuestas

**Redirecciones**:
- Después de POST exitoso: Redirección a lista correspondiente
- Error de permisos: Redirección con mensaje de error
- Login requerido: Redirección a `/login/` con parámetro `next`

**Mensajes**:
El sistema usa Django Messages Framework:
- `messages.success()`: Operaciones exitosas
- `messages.error()`: Errores
- `messages.warning()`: Advertencias
- `messages.info()`: Información general

---

## 📝 Ejemplo de Uso

### 1. Crear un Bien Patrimonial mediante Admin

```python
# Acceder al admin: http://localhost:8000/admin/
# Login con superusuario
# Ir a: Bienes Patrimoniales > Agregar bien patrimonial

# El formulario valida:
# - Precio no negativo
# - Fecha no futura
# - Precio solo si origen es COMPRA
```

### 2. Carga Masiva desde Excel

**Formato de Excel esperado**:

| N de ID | Descripcion | Cantidad | Origen | Estado | Precio | Fecha de Alta | Servicios |
|---------|------------|----------|--------|--------|--------|---------------|-----------|
| B001 | Computadora | 1 | Compra | Activo | 50000 | 2023-01-15 | Informática |
| B002 | Silla de ruedas | 5 | Donación | Activo | | 2023-02-20 | Traumatología |

**Código de carga**:
```python
# Vista: carga_masiva_bienes
# 1. Sube archivo Excel
# 2. Sistema procesa cada fila
# 3. Crea/actualiza bienes
# 4. Retorna estadísticas: creados, actualizados, errores
```

### 3. Búsqueda Avanzada

```python
# URL: /lista-bienes/?q=computadora&f_origen=COMPRA&f_desde=2023-01-01

# Query resultante:
bienes = BienPatrimonial.objects.filter(
    Q(descripcion__icontains='computadora') |
    Q(observaciones__icontains='computadora'),
    origen='COMPRA',
    fecha_adquisicion__gte='2023-01-01'
)
```

### 4. Dar de Baja un Bien

```python
# POST a /bienes/<pk>/dar-baja/
# Datos:
{
    'fecha_baja': '2024-01-15',
    'expediente_baja': 'EXP-2024-001',
    'descripcion_baja': 'Obsolescencia tecnológica'
}

# Resultado:
# - estado cambia a 'BAJA'
# - Se registran los datos de baja
# - El bien aparece en /bienes/bajas/
```

---

## 🚀 Comandos de Django Útiles

### Gestión de Base de Datos
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ver SQL de migraciones
python manage.py sqlmigrate core 0001

# Shell interactivo con modelos
python manage.py shell

# DbShell (SQLite)
python manage.py dbshell
```

### Gestión de Usuarios
```bash
# Crear superusuario
python manage.py createsuperuser

# Cambiar password
python manage.py changepassword username
```

### Desarrollo
```bash
# Ejecutar servidor
python manage.py runserver

# Ejecutar en puerto específico
python manage.py runserver 8001

# Colectar archivos estáticos
python manage.py collectstatic

# Tests
python manage.py test
python manage.py test core.tests
```

### Datos
```bash
# Exportar datos (backup)
python manage.py dumpdata > backup.json
python manage.py dumpdata core > core_backup.json

# Importar datos
python manage.py loaddata backup.json

# Limpiar base de datos
python manage.py flush
```

---

## 🔍 Debugging y Troubleshooting

### Logs
```bash
# Ver logs en tiempo real
tail -f logs/app.log

# Buscar errores
grep ERROR logs/app.log

# Logs de consultas SQL (en settings)
LOGGING['loggers']['django.db.backends'] = {
    'level': 'DEBUG',
    'handlers': ['console'],
}
```

### Shell de Django
```python
# python manage.py shell

from core.models import BienPatrimonial, Expediente

# Ver todos los bienes
bienes = BienPatrimonial.objects.all()
print(bienes.count())

# Buscar por criterio
bien = BienPatrimonial.objects.get(clave_unica=1)
print(bien.nombre, bien.estado)

# Crear expediente
exp = Expediente.objects.create(numero_expediente='EXP-2024-001')

# Asociar bien a expediente
bien.expediente = exp
bien.save()
```

### Problemas Comunes

**Error: No module named 'core'**
```bash
# Verificar INSTALLED_APPS en settings
# Verificar que estés en el directorio correcto
# Reinstalar dependencias
pip install -r requirements/base.txt
```

**Error: CSRF verification failed**
```python
# En templates, asegurar {% csrf_token %} en forms
# Verificar MIDDLEWARE incluye CsrfViewMiddleware
```

**Error: OperationalError: no such table**
```bash
# Aplicar migraciones
python manage.py migrate
```

---

## 📚 Recursos Adicionales

### Documentación Django
- [Django Documentation](https://docs.djangoproject.com/)
- [Django Models](https://docs.djangoproject.com/en/4.2/topics/db/models/)
- [Django Views](https://docs.djangoproject.com/en/4.2/topics/http/views/)
- [Django Admin](https://docs.djangoproject.com/en/4.2/ref/contrib/admin/)

### Herramientas Útiles
- **Django Debug Toolbar**: Perfilado de queries
- **django-extensions**: Comandos útiles adicionales
- **django-silk**: Profiling y monitoreo

---

## 👥 Equipo de Desarrollo Backend

- **Docentes**: Karina Alvarez, Alejandra, Felipe Morales, Fernando Diego Santolaria
- **Estudiantes**: ISFDyT 210

---

## 📄 Licencia

Este proyecto es desarrollado para el Hospital Melchor Romero con fines educativos y administrativos.

---

**Última actualización**: Octubre 2024
