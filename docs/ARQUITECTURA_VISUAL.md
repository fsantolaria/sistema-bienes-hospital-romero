# 🏗️ ARQUITECTURA VISUAL DEL SISTEMA

## 📊 Diagrama de Arquitectura General

```
┌─────────────────────────────────────────────────────────────────┐
│                        NAVEGADOR (Cliente)                       │
│                     http://localhost:8000                        │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP Request
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                         DJANGO SERVER                            │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      urls.py                              │  │
│  │  URL Router - Mapea URLs a vistas                         │  │
│  └──────────────────────┬───────────────────────────────────┘  │
│                         │                                        │
│                         ↓                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     views.py                              │  │
│  │  Lógica de Negocio - Procesa peticiones                   │  │
│  └──────┬───────────────────────────────────┬───────────────┘  │
│         │                                    │                   │
│         ↓                                    ↓                   │
│  ┌─────────────┐                    ┌──────────────┐           │
│  │  models.py  │ ←─────ORM──────→  │   SQLite     │           │
│  │  (Modelos)  │                    │ (Base Datos) │           │
│  └─────────────┘                    └──────────────┘           │
│         │                                                        │
│         ↓                                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   templates/                              │  │
│  │  HTML + Django Template Language                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP Response (HTML)
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    NAVEGADOR (Renderizado)                       │
│                      Página web visible                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ Estructura de la Base de Datos

```
┌─────────────────────┐
│      Usuario        │
│  ──────────────     │
│  • id (PK)          │
│  • username         │
│  • password         │
│  • email            │
│  • tipo_usuario     │
│  • is_active        │
└──────────┬──────────┘
           │ 1
           │
           │ OneToOne
           │
           │ 1
┌──────────▼──────────┐
│     Operador        │
│  ──────────────     │
│  • id (PK)          │
│  • usuario_id (FK)  │
│  • nombre_completo  │
│  • telefono         │
│  • direccion        │
└─────────────────────┘


┌─────────────────────┐
│    Expediente       │
│  ──────────────     │
│  • id (PK)          │
│  • numero_expediente│ (UNIQUE)
│  • organismo_origen │
│  • numero_compra    │
│  • proveedor        │
└──────────┬──────────┘
           │ 1
           │
           │ tiene
           │
           │ N
┌──────────▼──────────────────┐
│    BienPatrimonial          │
│  ──────────────────         │
│  • clave_unica (PK)         │
│  • nombre                   │
│  • descripcion              │
│  • cantidad                 │
│  • expediente_id (FK)       │
│  • numero_serie             │
│  • numero_identificacion    │
│  • cuenta_codigo            │
│  • nomenclatura_bienes      │
│  • fecha_adquisicion        │
│  • origen (CHOICE)          │
│  • estado (CHOICE)          │
│  • valor_adquisicion        │
│  • servicios                │
│  • observaciones            │
│  • fecha_baja               │
│  • expediente_baja          │
│  • descripcion_baja         │
└─────────────────────────────┘

Leyenda:
PK = Primary Key (Clave Primaria)
FK = Foreign Key (Clave Foránea)
1 = Uno
N = Muchos
```

---

## 🔄 Flujo de Datos Completo

### Ejemplo: Usuario lista bienes patrimoniales

```
┌──────────┐
│ Usuario  │ 1. Abre navegador y va a /lista-bienes/
└────┬─────┘
     │
     ↓ GET http://localhost:8000/lista-bienes/
     │
┌────▼──────────────────────────────────────────────┐
│ Django recibe petición                            │
└────┬──────────────────────────────────────────────┘
     │
     ↓ 2. Django busca en urls.py
     │
┌────▼──────────────────────────────────────────────┐
│ urls.py                                           │
│ path('lista-bienes/', views.lista_bienes, ...)    │
└────┬──────────────────────────────────────────────┘
     │
     ↓ 3. Ejecuta función lista_bienes()
     │
┌────▼──────────────────────────────────────────────┐
│ views.py - lista_bienes(request)                  │
│                                                   │
│ 1. Obtiene parámetros: q, filtros                │
│ 2. Consulta modelos                              │
└────┬──────────────────────────────────────────────┘
     │
     ↓ 4. BienPatrimonial.objects.filter(...)
     │
┌────▼──────────────────────────────────────────────┐
│ models.py - BienPatrimonial                       │
│                                                   │
│ Django ORM traduce a SQL                          │
└────┬──────────────────────────────────────────────┘
     │
     ↓ 5. SELECT * FROM core_bienpatrimonial WHERE...
     │
┌────▼──────────────────────────────────────────────┐
│ Base de Datos SQLite                              │
│                                                   │
│ Ejecuta query y retorna resultados                │
└────┬──────────────────────────────────────────────┘
     │
     ↓ 6. QuerySet con bienes
     │
┌────▼──────────────────────────────────────────────┐
│ views.py                                          │
│                                                   │
│ context = {'bienes': bienes}                      │
│ return render(request, 'lista.html', context)    │
└────┬──────────────────────────────────────────────┘
     │
     ↓ 7. Renderiza template
     │
┌────▼──────────────────────────────────────────────┐
│ templates/lista_bienes.html                       │
│                                                   │
│ {% for bien in bienes %}                          │
│   <tr><td>{{ bien.nombre }}</td></tr>            │
│ {% endfor %}                                      │
└────┬──────────────────────────────────────────────┘
     │
     ↓ 8. HTML generado
     │
┌────▼──────────────────────────────────────────────┐
│ HTTP Response                                     │
│                                                   │
│ <html>                                            │
│   <table>...datos de bienes...</table>           │
│ </html>                                           │
└────┬──────────────────────────────────────────────┘
     │
     ↓ 9. Navegador recibe HTML
     │
┌────▼──────────┐
│ Usuario ve    │ ✅ Tabla con lista de bienes
│ página        │
└───────────────┘
```

---

## 🎯 Flujo de Autenticación

```
┌──────────┐
│ Usuario  │ Ingresa usuario y contraseña
└────┬─────┘
     │
     ↓ POST /login/ con credenciales
     │
┌────▼──────────────────────────────────────┐
│ views.login_view(request)                 │
│                                           │
│ usuario = request.POST.get('usuario')     │
│ password = request.POST.get('contrasena') │
└────┬──────────────────────────────────────┘
     │
     ↓ authenticate(username, password)
     │
┌────▼──────────────────────────────────────┐
│ Django Auth Backend                       │
│                                           │
│ 1. Busca usuario en BD                    │
│ 2. Verifica password hasheado             │
└────┬──────────────────────────────────────┘
     │
     ├─────────┬──────────────┐
     │         │              │
     ↓         ↓              ↓
 ❌ None   ✅ User       ❌ Error
     │         │              │
     │         ↓              │
     │    login(request, user)│
     │         │              │
     │         ↓              │
     │    Crea sesión         │
     │    (Cookie)            │
     │         │              │
     │         ↓              │
     │    Redirige según rol  │
     │         │              │
     ↓         ↓              ↓
  Error   ✅ Success      Error
     │         │              │
     └─────────┴──────────────┘
               │
               ↓
     ┌─────────────────┐
     │ Dashboard según │
     │ tipo_usuario    │
     └─────────────────┘
          /        \
         /          \
    Admin        Empleado
   Dashboard     Dashboard
```

---

## 📦 Estructura del Proyecto Django

```
sistema-bienes-hospital-romero/
│
├── 📂 core/                        ← App principal
│   ├── 📂 models/
│   │   ├── __init__.py
│   │   ├── usuario.py              ← Modelo Usuario
│   │   ├── operador.py             ← Modelo Operador
│   │   ├── expediente.py           ← Modelo Expediente
│   │   └── bien_patrimonial.py     ← Modelo BienPatrimonial ⭐
│   │
│   ├── 📂 migrations/              ← Historial de cambios BD
│   │   ├── 0001_initial.py
│   │   └── ...
│   │
│   ├── 📂 tests/                   ← Tests unitarios
│   │   ├── test_models.py
│   │   └── test_login_y_permisos.py
│   │
│   ├── views.py                    ← Lógica de negocio ⭐
│   ├── urls.py                     ← Rutas de la app
│   ├── forms.py                    ← Formularios
│   ├── admin.py                    ← Config admin Django
│   └── constants.py                ← Constantes (estados, orígenes)
│
├── 📂 sistema_bienes/              ← Configuración proyecto
│   ├── 📂 settings/
│   │   ├── base.py                 ← Config común
│   │   ├── development.py          ← Config desarrollo
│   │   ├── testing.py              ← Config testing
│   │   └── production.py           ← Config producción
│   │
│   ├── urls.py                     ← URLs principales
│   ├── wsgi.py                     ← WSGI server
│   └── asgi.py                     ← ASGI server
│
├── 📂 templates/                   ← Plantillas HTML
│   ├── base.html
│   ├── login.html
│   ├── 📂 bienes/
│   │   ├── lista_bienes.html
│   │   ├── editar_bien.html
│   │   └── ...
│   └── ...
│
├── 📂 static/                      ← Archivos estáticos
│   ├── 📂 css/
│   ├── 📂 js/
│   └── 📂 img/
│
├── 📂 docs/                        ← Documentación
│   ├── BACKEND.md
│   ├── PRESENTACION_BACKEND.md
│   ├── QUICK_REFERENCE.md
│   └── ARQUITECTURA_VISUAL.md
│
├── 📂 requirements/                ← Dependencias
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
│
├── manage.py                       ← CLI Django
├── db.sqlite3                      ← Base de datos
└── README.md                       ← Documentación principal
```

---

## 🔄 Ciclo de Vida de una Petición HTTP

```
1. USUARIO HACE REQUEST
   ↓
   http://localhost:8000/bienes/5/editar/
   
2. DJANGO MIDDLEWARE (Autenticación, CSRF, etc.)
   ↓
   ✅ Usuario autenticado
   
3. URL DISPATCHER (urls.py)
   ↓
   path('bienes/<int:pk>/editar/', views.editar_bien)
   
4. VIEW FUNCTION (views.py)
   ↓
   def editar_bien(request, pk):
       bien = BienPatrimonial.objects.get(pk=5)
       ...
   
5. DJANGO ORM
   ↓
   SELECT * FROM core_bienpatrimonial WHERE clave_unica = 5
   
6. DATABASE
   ↓
   Retorna fila con datos del bien
   
7. VIEW PROCESA DATOS
   ↓
   form = BienForm(instance=bien)
   context = {'form': form, 'bien': bien}
   
8. TEMPLATE ENGINE
   ↓
   Renderiza editar_bien.html con contexto
   
9. MIDDLEWARE RESPONSE
   ↓
   Procesa respuesta
   
10. HTTP RESPONSE
    ↓
    HTML completo enviado al navegador
    
11. NAVEGADOR
    ↓
    Renderiza página visible al usuario
```

---

## 🎨 Patrón MTV en Acción

```
MODEL (Datos)
┌─────────────────────────┐
│  models.py              │
│                         │
│  class BienPatrimonial: │
│    nombre = ...         │
│    estado = ...         │
└───────┬─────────────────┘
        │
        │ ORM
        ↓
┌─────────────────────────┐
│  Base de Datos          │
│  (SQLite)               │
└───────┬─────────────────┘
        │
        │ QuerySet
        ↓
VIEW (Lógica)
┌─────────────────────────┐
│  views.py               │
│                         │
│  def lista_bienes:      │
│    bienes = Bien...all()│
│    return render(...)   │
└───────┬─────────────────┘
        │
        │ Context
        ↓
TEMPLATE (Presentación)
┌─────────────────────────┐
│  lista_bienes.html      │
│                         │
│  {% for bien in bienes%}│
│    {{ bien.nombre }}    │
│  {% endfor %}           │
└─────────────────────────┘
        │
        ↓
    HTML Final
```

---

## 🔐 Sistema de Autenticación y Permisos

```
┌──────────────┐
│   Usuario    │
│   Login      │
└──────┬───────┘
       │
       ↓ POST credenciales
       │
┌──────▼───────────────────┐
│  authenticate()          │
│  Verifica usuario/pass   │
└──────┬───────────────────┘
       │
       ├──────────┬──────────┐
       │          │          │
    ❌ None   ✅ User    ❌ Error
       │          │          │
       │          ↓          │
       │    login(user)      │
       │          │          │
       │          ↓          │
       │   Crea Sesión       │
       │   (Session ID)      │
       │          │          │
       │          ↓          │
       │   Cookie enviado    │
       │          │          │
       └──────────┴──────────┘
                  │
                  ↓
       Peticiones futuras incluyen cookie
                  │
                  ↓
       ┌──────────────────────┐
       │ @login_required      │
       │ Verifica sesión      │
       └──────┬───────────────┘
              │
              ├──────────┬──────────┐
              │          │          │
          ✅ OK      ❌ No    ⚠️ Expired
              │          │          │
              │          │          │
           Vista    Redirect    Redirect
         protegida   a login    a login
```

---

## 📊 Estados y Transiciones de un Bien

```
                    FLUJO DE ESTADOS
                    
     [NUEVO]
        │
        ↓ Crear bien
        │
    ┌───▼────┐
    │ ACTIVO │ ←──────────────────┐
    └───┬────┘                    │
        │                         │ restablecer_bien()
        ├──────────┬──────────┐   │
        │          │          │   │
        ↓          ↓          ↓   │
   ┌────────┐  ┌──────┐  ┌──────────┐
   │INACTIVO│  │MANTEN│  │   BAJA   │
   └────────┘  │IMIENTO│  └──────────┘
               └──────┘       │
                              │ eliminar_definitivo()
                              ↓
                          [ELIMINADO]
                        (No reversible)

Transiciones permitidas:
• ACTIVO → INACTIVO
• ACTIVO → MANTENIMIENTO
• ACTIVO → BAJA
• INACTIVO → ACTIVO
• MANTENIMIENTO → ACTIVO
• BAJA → ACTIVO (restablecer)
• BAJA → [ELIMINADO] (definitivo)
```

---

## 🔄 Proceso de Carga Masiva

```
┌──────────────┐
│   Usuario    │
│ Sube Excel   │
└──────┬───────┘
       │
       ↓ POST archivo.xlsx
       │
┌──────▼────────────────────────┐
│ views.carga_masiva_bienes()   │
└──────┬────────────────────────┘
       │
       ↓ Validar formulario
       │
┌──────▼────────────────────────┐
│ Pandas read_excel()           │
│ DataFrame con datos           │
└──────┬────────────────────────┘
       │
       ↓ Normalizar columnas
       │
┌──────▼────────────────────────┐
│ for row in dataframe:         │
│   Procesar fila               │
└──────┬────────────────────────┘
       │
       ├─── Fila 1 ───┐
       ├─── Fila 2 ───┤
       ├─── Fila 3 ───┤  transaction.atomic()
       ├─── ...   ───┤  (Todo o nada)
       └─── Fila N ───┘
              │
              ↓ Para cada fila:
              │
       ┌──────▼─────────────────────┐
       │ 1. Extraer datos           │
       │ 2. Validar/convertir       │
       │ 3. Crear/actualizar bien   │
       └──────┬─────────────────────┘
              │
              ├────────────┬─────────────┐
              │            │             │
           ✅ OK        ❌ Error    ⚠️ Duplicate
              │            │             │
              ↓            ↓             ↓
         Creado       Registrado    Actualizado
              │            │             │
              └────────────┴─────────────┘
                          │
                          ↓
               ┌──────────────────────┐
               │ Resumen:             │
               │ • Creados: 50        │
               │ • Actualizados: 10   │
               │ • Errores: 2         │
               └──────────────────────┘
```

---

## 🎯 Resumen de Componentes Clave

### 1. **URLs** → Enrutador
```python
path('lista-bienes/', views.lista_bienes, name='lista_bienes')
```
- Mapea URL a función de vista
- Puede capturar parámetros: `<int:pk>`

### 2. **Views** → Controlador
```python
def lista_bienes(request):
    bienes = BienPatrimonial.objects.all()
    return render(request, 'lista.html', {'bienes': bienes})
```
- Procesa peticiones HTTP
- Interactúa con modelos
- Retorna respuestas

### 3. **Models** → Datos
```python
class BienPatrimonial(models.Model):
    nombre = models.CharField(max_length=200)
```
- Define estructura de BD
- ORM para consultas
- Validaciones

### 4. **Templates** → Presentación
```html
{% for bien in bienes %}
    <tr><td>{{ bien.nombre }}</td></tr>
{% endfor %}
```
- Renderiza HTML
- Template tags de Django
- Recibe contexto de vista

---

**📝 Nota**: Estos diagramas son simplificaciones para facilitar la comprensión. El flujo real puede incluir middlewares, caché, signals, y otros componentes de Django.
