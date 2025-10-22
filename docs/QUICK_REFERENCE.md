# ⚡ REFERENCIA RÁPIDA - Backend Sistema de Bienes

## 🚀 Comandos Esenciales

```bash
# Iniciar servidor
python manage.py runserver

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Shell interactivo
python manage.py shell

# Crear superusuario
python manage.py createsuperuser

# Ejecutar tests
python manage.py test

# Colectar archivos estáticos
python manage.py collectstatic
```

---

## 📊 ORM - Operaciones Básicas

### Crear
```python
# Método 1
bien = BienPatrimonial.objects.create(
    nombre="Computadora",
    descripcion="HP ProBook"
)

# Método 2
bien = BienPatrimonial(nombre="Computadora")
bien.save()
```

### Leer
```python
# Todos
bienes = BienPatrimonial.objects.all()

# Uno por PK
bien = BienPatrimonial.objects.get(pk=1)

# Con filtro
activos = BienPatrimonial.objects.filter(estado='ACTIVO')

# Primer resultado
primero = BienPatrimonial.objects.first()

# Último resultado
ultimo = BienPatrimonial.objects.last()

# Contar
total = BienPatrimonial.objects.count()
```

### Actualizar
```python
# Método 1: save()
bien = BienPatrimonial.objects.get(pk=1)
bien.nombre = "Nuevo nombre"
bien.save()

# Método 2: update() (múltiples)
BienPatrimonial.objects.filter(estado='INACTIVO').update(estado='ACTIVO')
```

### Eliminar
```python
# Uno
bien = BienPatrimonial.objects.get(pk=1)
bien.delete()

# Múltiples
BienPatrimonial.objects.filter(estado='BAJA').delete()
```

---

## 🔍 Filtros y Consultas

### Filtros Básicos
```python
# Igual a
BienPatrimonial.objects.filter(estado='ACTIVO')

# Contiene (case insensitive)
BienPatrimonial.objects.filter(nombre__icontains='computadora')

# Mayor que
BienPatrimonial.objects.filter(valor_adquisicion__gt=1000)

# Menor o igual que
BienPatrimonial.objects.filter(cantidad__lte=5)

# En una lista
BienPatrimonial.objects.filter(estado__in=['ACTIVO', 'MANTENIMIENTO'])

# Es nulo
BienPatrimonial.objects.filter(fecha_baja__isnull=True)

# Rango de fechas
BienPatrimonial.objects.filter(
    fecha_adquisicion__gte='2024-01-01',
    fecha_adquisicion__lte='2024-12-31'
)
```

### Consultas OR
```python
from django.db.models import Q

bienes = BienPatrimonial.objects.filter(
    Q(estado='ACTIVO') | Q(estado='MANTENIMIENTO')
)
```

### Consultas NOT
```python
# Exclude
bienes = BienPatrimonial.objects.exclude(estado='BAJA')

# Con Q
from django.db.models import Q
bienes = BienPatrimonial.objects.filter(~Q(estado='BAJA'))
```

### Ordenar
```python
# Ascendente
BienPatrimonial.objects.order_by('nombre')

# Descendente
BienPatrimonial.objects.order_by('-fecha_adquisicion')

# Múltiples campos
BienPatrimonial.objects.order_by('estado', '-fecha_adquisicion')
```

### Optimización
```python
# Select related (ForeignKey)
bienes = BienPatrimonial.objects.select_related('expediente')

# Prefetch related (ManyToMany)
# (si tuviéramos relaciones M2M)
```

---

## 🎯 Vistas - Patrones Comunes

### Vista Básica
```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def mi_vista(request):
    datos = Model.objects.all()
    return render(request, 'template.html', {'datos': datos})
```

### Vista con GET
```python
@login_required
def lista_con_busqueda(request):
    q = request.GET.get('q', '')
    items = Model.objects.all()
    if q:
        items = items.filter(nombre__icontains=q)
    return render(request, 'lista.html', {'items': items})
```

### Vista con POST
```python
@login_required
def crear(request):
    if request.method == 'POST':
        form = MiForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Creado correctamente')
            return redirect('lista')
    else:
        form = MiForm()
    return render(request, 'crear.html', {'form': form})
```

### Vista con PK
```python
from django.shortcuts import get_object_or_404

@login_required
def detalle(request, pk):
    item = get_object_or_404(Model, pk=pk)
    return render(request, 'detalle.html', {'item': item})
```

### Vista solo POST
```python
from django.views.decorators.http import require_POST

@login_required
@require_POST
def eliminar(request, pk):
    item = get_object_or_404(Model, pk=pk)
    item.delete()
    messages.success(request, 'Eliminado')
    return redirect('lista')
```

---

## 🛣️ URLs - Patrones

### URL Básica
```python
from django.urls import path
from . import views

urlpatterns = [
    path('lista/', views.lista, name='lista'),
]
```

### URL con Parámetro
```python
path('item/<int:pk>/', views.detalle, name='detalle'),
path('item/<int:pk>/editar/', views.editar, name='editar'),
path('item/<int:pk>/eliminar/', views.eliminar, name='eliminar'),
```

### URL con String
```python
path('categoria/<str:slug>/', views.por_categoria, name='categoria'),
```

### Redirección
```python
from django.views.generic import RedirectView

path('vieja/', RedirectView.as_view(url='/nueva/')),
```

---

## 📝 Formularios

### ModelForm
```python
from django import forms
from .models import BienPatrimonial

class BienForm(forms.ModelForm):
    class Meta:
        model = BienPatrimonial
        fields = ['nombre', 'descripcion', 'cantidad']
        # o
        fields = '__all__'
        # o excluir campos
        exclude = ['fecha_creacion']
```

### Validación en Form
```python
class BienForm(forms.ModelForm):
    def clean_valor_adquisicion(self):
        valor = self.cleaned_data['valor_adquisicion']
        if valor < 0:
            raise forms.ValidationError("No puede ser negativo")
        return valor
```

### Uso en Vista
```python
# Crear
form = BienForm(request.POST)
if form.is_valid():
    form.save()

# Editar
bien = BienPatrimonial.objects.get(pk=1)
form = BienForm(request.POST, instance=bien)
if form.is_valid():
    form.save()
```

---

## 🔐 Autenticación

### Decoradores
```python
from django.contrib.auth.decorators import login_required

@login_required
def mi_vista(request):
    pass
```

### Login Manual
```python
from django.contrib.auth import authenticate, login

user = authenticate(username='user', password='pass')
if user is not None:
    login(request, user)
```

### Logout
```python
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('inicio')
```

### Usuario Actual
```python
def mi_vista(request):
    if request.user.is_authenticated:
        print(request.user.username)
        print(request.user.email)
```

---

## 💾 Transacciones

### Transaction Atomic
```python
from django.db import transaction

@transaction.atomic
def operacion_critica(request):
    # Todo o nada
    bien1.save()
    bien2.save()
    # Si algo falla, se deshace todo
```

### Context Manager
```python
from django.db import transaction

with transaction.atomic():
    bien1 = BienPatrimonial.objects.create(...)
    bien2 = BienPatrimonial.objects.create(...)
```

---

## 📋 Messages Framework

### Agregar Mensajes
```python
from django.contrib import messages

messages.success(request, 'Operación exitosa')
messages.error(request, 'Algo salió mal')
messages.warning(request, 'Advertencia')
messages.info(request, 'Información')
```

### En Template
```html
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}
```

---

## 🧪 Testing

### Test Básico
```python
from django.test import TestCase
from .models import BienPatrimonial

class BienTest(TestCase):
    def test_crear_bien(self):
        bien = BienPatrimonial.objects.create(
            nombre="Test",
            descripcion="Desc"
        )
        self.assertEqual(bien.nombre, "Test")
```

### Test de Vista
```python
class ViewTest(TestCase):
    def test_lista_bienes(self):
        response = self.client.get('/lista-bienes/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bienes')
```

### Test con Login
```python
def setUp(self):
    self.user = User.objects.create_user(
        username='test',
        password='pass123'
    )

def test_vista_protegida(self):
    self.client.login(username='test', password='pass123')
    response = self.client.get('/protegida/')
    self.assertEqual(response.status_code, 200)
```

---

## 🔧 Django Shell - Ejemplos

```python
# Abrir shell
python manage.py shell

# Importar modelos
from core.models import BienPatrimonial, Expediente

# Crear
bien = BienPatrimonial.objects.create(nombre="Test")

# Ver SQL de query
print(BienPatrimonial.objects.filter(estado='ACTIVO').query)

# Contar queries
from django.db import connection
len(connection.queries)

# Ver último query
connection.queries[-1]

# Reset BD (cuidado!)
from django.core.management import call_command
call_command('flush', interactive=False)
```

---

## 📦 Pandas para Carga Masiva

```python
import pandas as pd

# Leer Excel
df = pd.read_excel('archivo.xlsx', dtype=str)

# Ver columnas
print(df.columns)

# Iterar filas
for i, row in df.iterrows():
    nombre = row.get('Descripción', '')
    cantidad = row.get('Cantidad', 1)
    
    BienPatrimonial.objects.create(
        nombre=nombre,
        cantidad=int(cantidad)
    )
```

---

## 🔍 Debug

### Print SQL Queries
```python
# En settings.py (solo development)
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### Ver Variables
```python
import pdb; pdb.set_trace()  # Breakpoint
```

### Print en Template
```html
<pre>{{ variable|pprint }}</pre>
```

---

## ⚠️ Errores Comunes

### DoesNotExist
```python
try:
    bien = BienPatrimonial.objects.get(pk=999)
except BienPatrimonial.DoesNotExist:
    bien = None

# O mejor:
bien = get_object_or_404(BienPatrimonial, pk=999)
```

### MultipleObjectsReturned
```python
# get() debe retornar un solo objeto
# Usar filter() si pueden ser varios
bienes = BienPatrimonial.objects.filter(nombre='Test')
```

### IntegrityError
```python
from django.db import IntegrityError

try:
    bien.save()
except IntegrityError:
    # Violación de constraint (ej: unique)
    pass
```

---

## 📚 Recursos

### Documentación Oficial
- https://docs.djangoproject.com/
- https://docs.djangoproject.com/en/4.2/ref/models/querysets/

### Cheat Sheets
- Django ORM Cheatsheet
- Django QuerySet Cheatsheet

### Práctica
- Django Tutorial oficial
- Django by Example (libro)

---

**💡 Tip Final**: Guarda esta referencia y consúltala frecuentemente. Con la práctica, estos patrones se vuelven naturales.
