# 🔧 GUÍA COMPLETA DEL BACKEND - Sistema de Bienes Hospital Romero

## 📋 Tabla de Contenidos
1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Modelos de Datos](#modelos-de-datos)
4. [Vistas y Lógica de Negocio](#vistas-y-lógica-de-negocio)
5. [URLs y Rutas](#urls-y-rutas)
6. [Autenticación y Permisos](#autenticación-y-permisos)
7. [Flujo de Datos](#flujo-de-datos)
8. [APIs y Endpoints](#apis-y-endpoints)
9. [Carga Masiva de Datos](#carga-masiva-de-datos)
10. [Configuración y Ambientes](#configuración-y-ambientes)

---

## 🎯 Introducción

El **Sistema de Gestión de Bienes Patrimoniales del Hospital Melchor Romero** es una aplicación web construida con **Django 4.2.7** que permite gestionar el inventario de bienes patrimoniales del hospital.

### Características Principales del Backend:
- ✅ **ORM Django**: Manejo de base de datos SQLite mediante modelos
- ✅ **Autenticación personalizada**: Sistema de usuarios con roles (Admin/Empleado)
- ✅ **CRUD completo**: Crear, leer, actualizar y eliminar bienes patrimoniales
- ✅ **Carga masiva**: Importación de datos desde archivos Excel
- ✅ **Sistema de bajas**: Gestión de bienes dados de baja con trazabilidad
- ✅ **Filtros y búsquedas**: Búsqueda avanzada de bienes
- ✅ **Validaciones robustas**: Validación de datos a nivel modelo y formulario

---

## 🏗️ Arquitectura del Sistema

### Estructura del Proyecto

```
sistema-bienes-hospital-romero/
├── core/                          # Aplicación principal
│   ├── models/                    # Modelos de datos
│   │   ├── __init__.py
│   │   ├── bien_patrimonial.py   # Modelo principal de bienes
│   │   ├── expediente.py         # Expedientes de compra
│   │   ├── operador.py           # Operadores del sistema
│   │   └── usuario.py            # Usuarios personalizados
│   ├── views.py                   # Controladores/Vistas
│   ├── urls.py                    # Rutas de la app
│   ├── forms.py                   # Formularios
│   ├── admin.py                   # Configuración del admin
│   ├── constants.py               # Constantes del sistema
│   └── tests/                     # Tests unitarios
│       ├── test_models.py
│       └── test_login_y_permisos.py
├── sistema_bienes/                # Configuración del proyecto
│   ├── settings/                  # Configuración por ambiente
│   │   ├── base.py               # Configuración base
│   │   ├── development.py        # Desarrollo
│   │   ├── testing.py            # Testing
│   │   └── production.py         # Producción
│   ├── urls.py                    # URLs principales
│   ├── wsgi.py                    # Servidor WSGI
│   └── asgi.py                    # Servidor ASGI
├── templates/                     # Plantillas HTML
├── static/                        # Archivos estáticos (CSS, JS, imágenes)
├── requirements/                  # Dependencias por ambiente
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
└── manage.py                      # CLI de Django

```

### Patrón de Arquitectura: MTV (Model-Template-View)

Django utiliza el patrón **MTV** (Model-Template-View), una variación del MVC:

```
┌─────────────┐      ┌──────────────┐      ┌────────────┐
│   Browser   │ ───> │   URL Conf   │ ───> │   View     │
│  (Cliente)  │      │  (urls.py)   │      │ (views.py) │
└─────────────┘      └──────────────┘      └────────────┘
       ↑                                           │
       │                                           ↓
       │                                    ┌────────────┐
       │                                    │   Model    │
       │                                    │ (models/)  │
       │                                    └────────────┘
       │                                           │
       │                ┌──────────────┐          │
       └────────────────│   Template   │ <────────┘
                        │ (templates/) │
                        └──────────────┘
```

---

## 📊 Modelos de Datos

Los modelos definen la estructura de la base de datos. Cada modelo es una clase Python que hereda de `django.db.models.Model`.

### 1. Usuario (`core/models/usuario.py`)

**Propósito**: Gestiona la autenticación y autorización de usuarios del sistema.

```python
class Usuario(AbstractUser):
    TIPO_USUARIO = [
        ('admin', 'Administrador'),
        ('empleado', 'Empleado Hospital'),
    ]
    
    tipo_usuario = models.CharField(
        max_length=10,
        choices=TIPO_USUARIO,
        default='empleado'
    )
```

**Campos clave**:
- `username`: Usuario para login (heredado de AbstractUser)
- `email`: Email del usuario (heredado)
- `password`: Contraseña hasheada (heredado)
- `tipo_usuario`: Rol del usuario (admin o empleado)
- `is_active`: Estado activo/inactivo (heredado)
- `is_staff`: Puede acceder al admin (heredado)
- `is_superuser`: Superusuario con todos los permisos (heredado)

**Características**:
- Extiende `AbstractUser` de Django
- Incluye sistema de grupos y permisos personalizados
- Relación con modelo `Operador` (OneToOne)

---

### 2. Operador (`core/models/operador.py`)

**Propósito**: Extiende el modelo Usuario con información adicional del operador.

```python
class Operador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=300, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
```

**Relación con Usuario**:
```
Usuario (1) ←──── (1) Operador
```

**Propiedades computadas**:
- `email`: Retorna el email del usuario asociado
- `username`: Retorna el username del usuario asociado

---

### 3. Expediente (`core/models/expediente.py`)

**Propósito**: Representa expedientes de compra o trámites administrativos.

```python
class Expediente(models.Model):
    numero_expediente = models.CharField(max_length=50, unique=True)
    organismo_origen = models.CharField(max_length=120, blank=True)
    numero_compra = models.CharField(max_length=50, blank=True)
    proveedor = models.CharField(max_length=200, blank=True)
```

**Campos**:
- `numero_expediente`: Identificador único del expediente (ej: "EXP-2024-001")
- `organismo_origen`: Organismo que origina la compra
- `numero_compra`: Número de orden de compra
- `proveedor`: Nombre del proveedor

**Uso**: Los bienes patrimoniales se relacionan con expedientes para mantener trazabilidad.

---

### 4. BienPatrimonial (`core/models/bien_patrimonial.py`) ⭐

**Propósito**: Modelo principal del sistema que representa cada bien patrimonial del hospital.

```python
class BienPatrimonial(models.Model):
    # Identificador principal
    clave_unica = models.BigAutoField(primary_key=True)
    
    # Datos básicos
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    cantidad = models.PositiveIntegerField(default=1)
    
    # Relación con Expediente
    expediente = models.ForeignKey(
        "Expediente",
        on_delete=models.SET_NULL,
        null=True,
        related_name="bienes"
    )
    
    # Identificaciones
    numero_serie = models.CharField(max_length=100, blank=True)
    numero_identificacion = models.CharField(max_length=50, unique=True, null=True)
    cuenta_codigo = models.CharField(max_length=20, blank=True)
    nomenclatura_bienes = models.CharField(max_length=200, blank=True)
    
    # Fechas
    fecha_adquisicion = models.DateField(null=True, blank=True)
    
    # Origen y Estado
    origen = models.CharField(
        max_length=15,
        choices=ORIGEN_CHOICES,
        default=ORIGEN_COMPRA
    )
    estado = models.CharField(
        max_length=50,
        choices=ESTADO_CHOICES,
        default=ESTADO_ACTIVO
    )
    
    # Valor económico
    valor_adquisicion = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True
    )
    
    # Otros datos
    servicios = models.CharField(max_length=200, blank=True)
    observaciones = models.TextField(blank=True)
    
    # Campos de BAJA
    fecha_baja = models.DateField(null=True, blank=True)
    expediente_baja = models.CharField(max_length=100, null=True, blank=True)
    descripcion_baja = models.TextField(blank=True)
```

#### Estados Posibles (constantes en `core/constants.py`):

```python
ESTADO_CHOICES = (
    ('ACTIVO', 'Activo'),
    ('INACTIVO', 'Inactivo'),
    ('MANTENIMIENTO', 'En mantenimiento'),
    ('BAJA', 'Dado de baja'),
)
```

#### Orígenes Posibles:

```python
ORIGEN_CHOICES = (
    ('DONACION', 'Donación'),
    ('OMISION', 'Omisión'),
    ('TRANSFERENCIA', 'Transferencia/Traslado'),
    ('COMPRA', 'Compra'),
)
```

#### Validaciones Personalizadas:

El método `clean()` realiza validaciones de negocio:

```python
def clean(self):
    # 1. Precio no negativo
    if self.valor_adquisicion is not None and self.valor_adquisicion < 0:
        raise ValidationError("El precio no puede ser negativo")
    
    # 2. Fecha de alta no futura
    if self.fecha_adquisicion and self.fecha_adquisicion > date.today():
        raise ValidationError("La fecha no puede ser futura")
    
    # 3. Si no es compra, no debe tener precio
    if self.origen != ORIGEN_COMPRA:
        self.valor_adquisicion = None
```

#### Relaciones:

```
Expediente (1) ←───── (N) BienPatrimonial
```

Un expediente puede tener múltiples bienes asociados.

---

## 🎮 Vistas y Lógica de Negocio

Las vistas en Django son funciones (o clases) que procesan las peticiones HTTP y devuelven respuestas.

### Estructura de una Vista en Django:

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required  # Decorador: requiere autenticación
def mi_vista(request):
    # 1. Procesar datos de entrada
    if request.method == 'POST':
        # Manejar formulario
        pass
    
    # 2. Lógica de negocio
    datos = Model.objects.all()
    
    # 3. Preparar contexto
    context = {'datos': datos}
    
    # 4. Renderizar template
    return render(request, 'template.html', context)
```

### Vistas Principales del Sistema (`core/views.py`):

#### 1. Autenticación

```python
def login_view(request):
    """Vista de login"""
    if request.user.is_authenticated:
        # Ya está logueado, redireccionar
        return redirect(_role_route_name(request.user))
    
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')
        
        # Autenticar
        user = authenticate(request, username=usuario, password=contrasena)
        
        if user is not None:
            login(request, user)  # Crear sesión
            return redirect(_role_route_name(user))
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

def logout_view(request):
    """Cerrar sesión"""
    logout(request)
    return redirect('inicio')
```

**Flujo de autenticación**:
1. Usuario ingresa credenciales
2. `authenticate()` verifica contra la base de datos
3. Si es válido, `login()` crea una sesión
4. Redirección según el rol del usuario

---

#### 2. Vistas de Dashboard

```python
@login_required
def home_admin(request):
    """Dashboard para administradores"""
    if request.user.tipo_usuario != 'admin':
        return redirect('operadores')
    return render(request, 'home_admin.html')

@login_required
def operadores(request):
    """Dashboard para operadores/empleados"""
    return render(request, 'operadores.html')
```

**Control de acceso por rol**: Las vistas verifican `tipo_usuario` para autorizar.

---

#### 3. Lista de Bienes con Filtros

```python
@login_required
def lista_bienes(request):
    # Parámetros de búsqueda/filtro desde GET
    q = request.GET.get("q", "").strip()           # Búsqueda general
    f_origen = request.GET.get("f_origen", "")     # Filtro por origen
    f_estado = request.GET.get("f_estado", "")     # Filtro por estado
    f_desde = request.GET.get("f_desde", "")       # Fecha desde
    f_hasta = request.GET.get("f_hasta", "")       # Fecha hasta
    orden = request.GET.get("orden", "-fecha")     # Ordenamiento
    
    # QuerySet base con relaciones optimizadas
    bienes = BienPatrimonial.objects.select_related("expediente")
    
    # Búsqueda en múltiples campos
    if q:
        bienes = bienes.filter(
            Q(clave_unica__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(numero_identificacion__icontains=q) |
            Q(expediente__numero_expediente__icontains=q)
        )
    
    # Filtros específicos
    if f_origen:
        bienes = bienes.filter(origen=f_origen)
    if f_estado:
        bienes = bienes.filter(estado=f_estado)
    
    # Rango de fechas
    if f_desde:
        bienes = bienes.filter(fecha_adquisicion__gte=parse_date(f_desde))
    if f_hasta:
        bienes = bienes.filter(fecha_adquisicion__lte=parse_date(f_hasta))
    
    # Ordenamiento
    if orden == "-fecha":
        bienes = bienes.order_by("-fecha_adquisicion")
    
    return render(request, "bienes/lista_bienes.html", {"bienes": bienes})
```

**Conceptos clave**:
- **QuerySet**: Conjunto de consultas lazy (se ejecutan cuando se necesitan)
- **select_related()**: Optimización que hace JOIN para evitar N+1 queries
- **Q objects**: Permiten crear consultas OR complejas
- **Filtros encadenados**: `filter().filter()` crea AND automáticamente

---

#### 4. CRUD de Bienes

**Editar Bien**:
```python
@login_required
def editar_bien(request, pk):
    bien = get_object_or_404(BienPatrimonial, pk=pk)
    
    if request.method == 'POST':
        form = BienPatrimonialForm(request.POST, instance=bien)
        if form.is_valid():
            form.save()
            messages.success(request, "Bien actualizado correctamente.")
            return redirect('lista_bienes')
    else:
        form = BienPatrimonialForm(instance=bien)
    
    return render(request, 'bienes/editar_bien.html', {
        'form': form,
        'bien': bien
    })
```

**Eliminar Bien**:
```python
@login_required
def eliminar_bien(request, pk):
    bien = get_object_or_404(BienPatrimonial, pk=pk)
    bien.delete()
    messages.success(request, "Bien eliminado correctamente.")
    return redirect('lista_bienes')
```

---

#### 5. Sistema de Bajas

```python
@login_required
@require_POST
def dar_baja_bien(request, pk):
    """Dar de baja un bien (no lo elimina físicamente)"""
    bien = get_object_or_404(BienPatrimonial, pk=pk)
    
    # Obtener datos de la baja
    fecha_baja = parse_date(request.POST.get("fecha_baja")) or date.today()
    expediente_baja = request.POST.get("expediente_baja", "").strip()
    descripcion_baja = request.POST.get("descripcion_baja", "").strip()
    
    # Actualizar bien
    bien.estado = "BAJA"
    bien.fecha_baja = fecha_baja
    bien.expediente_baja = expediente_baja
    bien.descripcion_baja = descripcion_baja
    bien.save()
    
    messages.success(request, f"Bien {bien.clave_unica} dado de baja.")
    return redirect("lista_baja_bienes")

@login_required
@require_POST
@transaction.atomic
def restablecer_bien(request, pk):
    """Restablecer un bien dado de baja"""
    bien = get_object_or_404(BienPatrimonial, pk=pk)
    
    bien.estado = "ACTIVO"
    bien.fecha_baja = None
    bien.expediente_baja = None
    bien.descripcion_baja = ""
    bien.save()
    
    messages.success(request, f"Bien {bien.clave_unica} restablecido.")
    return redirect("lista_bienes")
```

**Conceptos**:
- **Baja lógica**: El registro no se elimina, solo cambia su estado
- **@require_POST**: Solo acepta peticiones POST (seguridad)
- **@transaction.atomic**: Garantiza atomicidad de la operación

---

## 🛣️ URLs y Rutas

Las URLs mapean las peticiones HTTP a las vistas correspondientes.

### Archivo `core/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboards
    path('home_admin/', views.home_admin, name='home_admin'),
    path('operadores/', views.operadores, name='operadores'),
    
    # Lista de bienes
    path("lista-bienes/", views.lista_bienes, name="lista_bienes"),
    
    # CRUD
    path("bienes/<int:pk>/editar/", views.editar_bien, name="editar_bien"),
    path("bienes/<int:pk>/eliminar/", views.eliminar_bien, name="eliminar_bien"),
    
    # Carga masiva
    path("carga-masiva/", views.carga_masiva_bienes, name="carga_masiva"),
    
    # Bajas
    path("bienes/bajas/", views.lista_baja_bienes, name="lista_baja_bienes"),
    path("bienes/<int:pk>/dar-baja/", views.dar_baja_bien, name="dar_baja_bien"),
    path("bienes/<int:pk>/restablecer/", views.restablecer_bien, name="restablecer_bien"),
]
```

### Parámetros en URLs:

- `<int:pk>`: Captura un número entero y lo pasa como parámetro `pk` a la vista
- `name='lista_bienes'`: Nombre de la ruta para usar en `reverse()` y templates

### Uso en Templates:

```html
<a href="{% url 'editar_bien' bien.pk %}">Editar</a>
```

---

## 🔐 Autenticación y Permisos

### Sistema de Autenticación Django:

1. **Modelo de Usuario personalizado** (`Usuario`):
   - Extiende `AbstractUser`
   - Agrega campo `tipo_usuario`

2. **Configuración en `settings/base.py`**:
```python
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
```

3. **Decorador `@login_required`**:
```python
from django.contrib.auth.decorators import login_required

@login_required
def mi_vista_protegida(request):
    # Solo usuarios autenticados pueden acceder
    pass
```

### Control de Acceso por Rol:

```python
def _role_route_name(user):
    """Determina la ruta según el rol del usuario"""
    if hasattr(user, 'tipo_usuario'):
        return 'home_admin' if user.tipo_usuario == 'admin' else 'operadores'
    return 'home_admin' if user.is_superuser else 'operadores'

@login_required
def home_admin(request):
    """Solo administradores"""
    if request.user.tipo_usuario != 'admin':
        messages.error(request, 'No tienes permisos')
        return redirect('operadores')
    return render(request, 'home_admin.html')
```

### Permisos en el Sistema:

| Rol          | Permisos                                      |
|--------------|-----------------------------------------------|
| Admin        | Acceso total al sistema                       |
| Empleado     | Ver bienes, crear, editar (según permisos)    |
| Superuser    | Acceso al admin de Django + permisos totales  |

---

## 🔄 Flujo de Datos

### Ejemplo: Crear un Bien Patrimonial

```
1. Usuario llena formulario
   ↓
2. POST a /bienes/ con datos
   ↓
3. Vista recibe request
   ↓
4. Crear Form con request.POST
   ↓
5. Validar form.is_valid()
   ↓
6. Si válido: form.save() → BD
   ↓
7. Redireccionar a lista_bienes
   ↓
8. Mostrar mensaje de éxito
```

### Diagrama de Flujo Completo:

```
┌──────────┐
│ Usuario  │
│ (Chrome) │
└────┬─────┘
     │ GET /lista-bienes/
     ↓
┌────────────────┐
│   urls.py      │  → Busca ruta 'lista_bienes'
└────┬───────────┘
     │
     ↓
┌────────────────┐
│   views.py     │  → Ejecuta lista_bienes(request)
│ lista_bienes() │
└────┬───────────┘
     │
     ↓ BienPatrimonial.objects.filter(...)
┌────────────────┐
│   models.py    │  → Consulta BD
│ BienPatrimonial│
└────┬───────────┘
     │ QuerySet de bienes
     ↓
┌────────────────┐
│   views.py     │  → Prepara contexto
│ context = {...}│
└────┬───────────┘
     │
     ↓ render(request, 'lista_bienes.html', context)
┌────────────────┐
│ templates/     │  → Renderiza HTML
│ lista_bienes   │
└────┬───────────┘
     │ HTML completo
     ↓
┌────────────────┐
│ Usuario recibe │
│ página HTML    │
└────────────────┘
```

---

## 🌐 APIs y Endpoints

### Listado de Endpoints Disponibles:

| Método | URL                                   | Vista                          | Descripción                    |
|--------|---------------------------------------|--------------------------------|--------------------------------|
| GET/POST | `/login/`                           | `login_view`                   | Login de usuario               |
| GET    | `/logout/`                            | `logout_view`                  | Logout de usuario              |
| GET    | `/inicio/`                            | `inicio`                       | Página inicial                 |
| GET    | `/home_admin/`                        | `home_admin`                   | Dashboard admin                |
| GET    | `/operadores/`                        | `operadores`                   | Dashboard empleados            |
| GET    | `/lista-bienes/`                      | `lista_bienes`                 | Lista de bienes (con filtros)  |
| GET/POST | `/bienes/<pk>/editar/`              | `editar_bien`                  | Editar bien                    |
| POST   | `/bienes/<pk>/eliminar/`              | `eliminar_bien`                | Eliminar bien                  |
| GET/POST | `/carga-masiva/`                    | `carga_masiva_bienes`          | Carga masiva Excel             |
| GET    | `/bienes/bajas/`                      | `lista_baja_bienes`            | Listar bienes de baja          |
| POST   | `/bienes/<pk>/dar-baja/`              | `dar_baja_bien`                | Dar de baja un bien            |
| POST   | `/bienes/<pk>/restablecer/`           | `restablecer_bien`             | Restablecer bien dado de baja  |
| POST   | `/bienes/<pk>/eliminar-definitivo/`   | `eliminar_bien_definitivo`     | Eliminación física definitiva  |

### Parámetros de Búsqueda en `/lista-bienes/`:

| Parámetro  | Tipo   | Descripción                     |
|------------|--------|---------------------------------|
| `q`        | string | Búsqueda general en todos los campos |
| `f_origen` | string | Filtrar por origen (COMPRA, DONACION, etc.) |
| `f_estado` | string | Filtrar por estado (ACTIVO, BAJA, etc.) |
| `f_desde`  | date   | Filtrar por fecha desde         |
| `f_hasta`  | date   | Filtrar por fecha hasta         |
| `orden`    | string | Ordenar por fecha, precio, etc. |

**Ejemplo**:
```
GET /lista-bienes/?q=computadora&f_estado=ACTIVO&orden=-fecha
```

---

## 📦 Carga Masiva de Datos

Una de las funcionalidades más importantes del backend es la **carga masiva de bienes desde Excel**.

### Proceso de Carga Masiva:

```python
@login_required
def carga_masiva_bienes(request):
    if request.method != 'POST':
        return render(request, 'carga_masiva.html', {'form': CargaMasivaForm()})
    
    # 1. Validar formulario
    form = CargaMasivaForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, 'carga_masiva.html', {'form': form})
    
    # 2. Leer archivo Excel
    archivo = request.FILES['archivo_excel']
    df = pd.read_excel(archivo, dtype=str)
    
    # 3. Procesar cada fila
    with transaction.atomic():
        for i, row in df.iterrows():
            # Extraer datos de la fila
            numero_id = get_first(row, ['n de id', 'numero_identificacion'])
            descripcion = get_first(row, ['descripcion', 'descripción'])
            # ... más campos
            
            # Crear o actualizar bien
            if numero_id:
                bien, created = BienPatrimonial.objects.update_or_create(
                    numero_identificacion=numero_id,
                    defaults={
                        'nombre': nombre,
                        'descripcion': descripcion,
                        # ... más campos
                    }
                )
    
    return redirect('lista_bienes')
```

### Características de la Carga Masiva:

1. **Lectura con Pandas**: Usa `pd.read_excel()` para leer archivos Excel
2. **Mapeo flexible de columnas**: Busca columnas por varios nombres posibles
3. **Validación de datos**: Convierte y valida cada campo
4. **Transacción atómica**: Si una fila falla, se deshacen todos los cambios
5. **Update o Create**: Si el bien existe (por `numero_identificacion`), lo actualiza; si no, lo crea
6. **Feedback al usuario**: Muestra mensajes de éxito/error

### Funciones Helper:

```python
def parse_money(v):
    """Convierte strings con formato monetario a Decimal"""
    txt = s(v).replace('$', '').replace(' ', '')
    return Decimal(txt)

def map_origen(v):
    """Mapea texto a constantes de origen"""
    t = s(v).lower()
    if 'compra' in t:
        return 'COMPRA'
    if 'donac' in t:
        return 'DONACION'
    return None

def parse_date_any(v):
    """Parsea fecha en múltiples formatos"""
    return pd.to_datetime(txt, errors='coerce', dayfirst=True).date()
```

### Formato de Excel Esperado:

| N° de ID | Descripción    | Cantidad | Origen  | Estado  | Precio    | Fecha de Alta |
|----------|----------------|----------|---------|---------|-----------|---------------|
| ID-001   | Computadora HP | 1        | COMPRA  | ACTIVO  | $1500.00  | 01/01/2024    |
| ID-002   | Silla Oficina  | 5        | COMPRA  | ACTIVO  | $250.00   | 15/01/2024    |

---

## ⚙️ Configuración y Ambientes

El proyecto utiliza **configuración modular por ambiente**.

### Estructura de Settings:

```
sistema_bienes/settings/
├── __init__.py
├── base.py           # Configuración común
├── development.py    # Desarrollo
├── testing.py        # Testing
└── production.py     # Producción
```

### `base.py` - Configuración Base:

```python
# Apps instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'core',  # App principal
]

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Idioma y zona horaria
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Usuario personalizado
AUTH_USER_MODEL = 'core.Usuario'
```

### `development.py` - Desarrollo:

```python
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
```

### `production.py` - Producción:

```python
from .base import *

DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
SECRET_KEY = config('SECRET_KEY')  # Obligatorio desde .env

# Seguridad adicional
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Variables de Entorno (.env):

```bash
# Development
DJANGO_ENV=development
DEBUG=True
SECRET_KEY=mi-clave-secreta-desarrollo

# Testing
DJANGO_ENV=testing
DEBUG=True

# Production
DJANGO_ENV=production
DEBUG=False
SECRET_KEY=clave-super-segura-produccion
ALLOWED_HOSTS=misitioweb.com,www.misitioweb.com
```

### Selección de Ambiente en `manage.py`:

```python
from decouple import config

def main():
    environment = config('DJANGO_ENV', default='development')
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        f'sistema_bienes.settings.{environment}'
    )
```

---

## 🧪 Testing

### Estructura de Tests:

```python
from django.test import TestCase
from core.models import BienPatrimonial, Expediente

class BienModelTest(TestCase):
    def setUp(self):
        """Se ejecuta antes de cada test"""
        self.expediente = Expediente.objects.create(
            numero_expediente="EXP-001"
        )
        self.bien = BienPatrimonial.objects.create(
            nombre="Test Bien",
            descripcion="Descripción test"
        )
    
    def test_creacion_bien(self):
        """Test: crear un bien correctamente"""
        bien = BienPatrimonial.objects.get(nombre="Test Bien")
        self.assertEqual(bien.estado, "ACTIVO")
        self.assertIsNotNone(bien.clave_unica)
    
    def test_validacion_precio_negativo(self):
        """Test: precio no puede ser negativo"""
        bien = BienPatrimonial(
            nombre="Bien",
            valor_adquisicion=-100
        )
        with self.assertRaises(ValidationError):
            bien.full_clean()
```

### Ejecutar Tests:

```bash
# Todos los tests
python manage.py test

# Tests de una app específica
python manage.py test core

# Tests de un módulo específico
python manage.py test core.tests.test_models

# Con ambiente de testing
python manage.py test --settings=sistema_bienes.settings.testing
```

---

## 📚 Resumen de Conceptos Clave

### 1. ORM de Django:

```python
# Crear
bien = BienPatrimonial.objects.create(nombre="Nuevo")

# Leer
bienes = BienPatrimonial.objects.all()
bien = BienPatrimonial.objects.get(pk=1)
bienes = BienPatrimonial.objects.filter(estado="ACTIVO")

# Actualizar
bien.nombre = "Nuevo nombre"
bien.save()

# Eliminar
bien.delete()
```

### 2. QuerySets:

- **Lazy**: No se ejecutan hasta que se necesitan
- **Encadenables**: `filter().filter().order_by()`
- **Optimizables**: `select_related()`, `prefetch_related()`

### 3. Migraciones:

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ver SQL de migración
python manage.py sqlmigrate core 0001
```

### 4. Django Admin:

```python
from django.contrib import admin
from .models import BienPatrimonial

@admin.register(BienPatrimonial)
class BienPatrimonialAdmin(admin.ModelAdmin):
    list_display = ['clave_unica', 'nombre', 'estado', 'origen']
    list_filter = ['estado', 'origen']
    search_fields = ['nombre', 'descripcion']
```

---

## 🔧 Comandos Útiles

```bash
# Servidor de desarrollo
python manage.py runserver

# Shell interactivo
python manage.py shell

# Crear superusuario
python manage.py createsuperuser

# Colectar archivos estáticos
python manage.py collectstatic

# Verificar proyecto
python manage.py check

# Ver todas las migraciones
python manage.py showmigrations
```

---

## 📖 Recursos Adicionales

- **Documentación Django**: https://docs.djangoproject.com/
- **Django ORM**: https://docs.djangoproject.com/en/4.2/topics/db/queries/
- **Django Auth**: https://docs.djangoproject.com/en/4.2/topics/auth/
- **Django Testing**: https://docs.djangoproject.com/en/4.2/topics/testing/

---

## 🎯 Próximos Pasos para el Equipo Backend

1. **Familiarízate con los modelos**: Explora `core/models/`
2. **Entiende el flujo de vistas**: Lee `core/views.py`
3. **Prueba el sistema**: Crea bienes, busca, filtra, da de baja
4. **Experimenta con el shell**: `python manage.py shell`
5. **Lee y ejecuta los tests**: `python manage.py test`
6. **Explora el admin de Django**: http://127.0.0.1:8000/admin/

---

**¡Bienvenido al equipo de backend del Sistema de Bienes Hospital Romero! 🚀**
