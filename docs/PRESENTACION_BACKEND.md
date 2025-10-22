# 🎤 GUÍA DE PRESENTACIÓN DEL BACKEND

## 📌 Cómo Presentar el Sistema de Bienes Hospital Romero a tus Compañeros

Esta guía te ayudará a explicar el backend del sistema de manera clara y estructurada.

---

## 📋 AGENDA DE PRESENTACIÓN (45-60 minutos)

### 1. INTRODUCCIÓN (5 min)
### 2. ARQUITECTURA GENERAL (10 min)
### 3. MODELOS Y BASE DE DATOS (15 min)
### 4. VISTAS Y LÓGICA (10 min)
### 5. DEMO EN VIVO (10 min)
### 6. PREGUNTAS Y RESPUESTAS (10 min)

---

## 1️⃣ INTRODUCCIÓN (5 minutos)

### ¿Qué presentar?

**Contexto del Proyecto:**
> "El Sistema de Gestión de Bienes Patrimoniales del Hospital Melchor Romero es una aplicación web que permite gestionar todo el inventario del hospital: desde computadoras hasta equipamiento médico."

**Tecnologías:**
- Framework: **Django 4.2.7**
- Base de datos: **SQLite**
- Lenguaje: **Python 3.10+**
- Frontend: **Bootstrap 5**

**¿Por qué Django?**
- Framework maduro y robusto
- Incluye ORM para manejar la base de datos
- Sistema de autenticación integrado
- Admin panel automático
- Documentación excelente

### Demostración Visual

```
Mostrar la estructura del proyecto:
sistema-bienes-hospital-romero/
├── core/           ← Nuestra app principal
├── sistema_bienes/ ← Configuración
├── templates/      ← HTML
├── static/         ← CSS, JS
└── manage.py       ← Comando principal
```

---

## 2️⃣ ARQUITECTURA GENERAL (10 minutos)

### Patrón MTV (Model-Template-View)

**Explicación:**
> "Django usa MTV, que es similar a MVC pero con nombres diferentes:"

```
Cliente hace request
    ↓
URL mapea a una View
    ↓
View consulta Models (BD)
    ↓
View renderiza Template
    ↓
Respuesta HTML al cliente
```

### Flujo de una Petición

**Ejemplo práctico: Ver lista de bienes**

1. **Usuario**: Abre navegador → http://localhost:8000/lista-bienes/
2. **urls.py**: Busca la ruta `path('lista-bienes/', views.lista_bienes)`
3. **views.py**: Ejecuta función `lista_bienes(request)`
4. **models.py**: `BienPatrimonial.objects.all()` consulta la BD
5. **template**: `lista_bienes.html` muestra los datos
6. **Usuario**: Ve la tabla con todos los bienes

### Demo en Código

**Mostrar archivo `core/urls.py`:**
```python
urlpatterns = [
    path("lista-bienes/", views.lista_bienes, name="lista_bienes"),
]
```

**Explicar:**
- `"lista-bienes/"` → URL que el usuario visita
- `views.lista_bienes` → Función que se ejecuta
- `name="lista_bienes"` → Nombre para referenciar en templates

---

## 3️⃣ MODELOS Y BASE DE DATOS (15 minutos)

### ¿Qué son los Modelos?

> "Los modelos son clases Python que representan tablas en la base de datos. Django automáticamente crea las tablas y maneja las consultas."

### Modelos del Sistema

#### 1. **Usuario** (Autenticación)

**Mostrar código:**
```python
class Usuario(AbstractUser):
    tipo_usuario = models.CharField(
        choices=[('admin', 'Administrador'), ('empleado', 'Empleado')]
    )
```

**Explicar:**
- Extiende el usuario de Django
- Agrega el campo `tipo_usuario` para roles
- Ya incluye `username`, `password`, `email`, etc.

#### 2. **Expediente** (Documentación de compras)

**Mostrar código:**
```python
class Expediente(models.Model):
    numero_expediente = models.CharField(max_length=50, unique=True)
    proveedor = models.CharField(max_length=200, blank=True)
```

**Explicar:**
- Cada compra tiene un expediente
- `unique=True` garantiza que no haya duplicados
- `blank=True` permite que sea opcional

#### 3. **BienPatrimonial** ⭐ (El modelo principal)

**Mostrar campos principales:**
```python
class BienPatrimonial(models.Model):
    clave_unica = models.BigAutoField(primary_key=True)  # ID auto
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    cantidad = models.PositiveIntegerField(default=1)
    
    # Relación con expediente
    expediente = models.ForeignKey("Expediente", ...)
    
    # Estados
    estado = models.CharField(choices=ESTADO_CHOICES)
    origen = models.CharField(choices=ORIGEN_CHOICES)
    
    # Económico
    valor_adquisicion = models.DecimalField(max_digits=12, decimal_places=2)
```

**Conceptos clave a explicar:**

1. **Primary Key (clave_unica)**
   - Identificador único de cada bien
   - Se genera automáticamente (1, 2, 3...)

2. **ForeignKey (expediente)**
   - Relación: Muchos bienes → Un expediente
   - `on_delete=models.SET_NULL` → Si se borra el expediente, el bien queda sin expediente

3. **Choices (estado, origen)**
   - Valores predefinidos (ej: ACTIVO, INACTIVO, BAJA)
   - Evita datos inconsistentes

4. **Validaciones**
   - `clean()` valida lógica de negocio
   - Ejemplo: precio no puede ser negativo

### Demo en Django Shell

**Ejecutar en vivo:**
```python
# Abrir shell
python manage.py shell

# Crear un bien
from core.models import BienPatrimonial
bien = BienPatrimonial.objects.create(
    nombre="Computadora HP",
    descripcion="Equipo de oficina",
    cantidad=1
)

# Consultar
bienes = BienPatrimonial.objects.all()
print(bienes)

# Filtrar
activos = BienPatrimonial.objects.filter(estado="ACTIVO")
print(activos.count())

# Buscar uno
bien = BienPatrimonial.objects.get(pk=1)
print(bien.nombre)
```

### Diagrama de Relaciones

**Dibujar en pizarra o mostrar:**
```
┌─────────────┐
│  Expediente │
│ (1)         │
└──────┬──────┘
       │
       │ tiene
       │
       ↓ (N)
┌─────────────────┐
│ BienPatrimonial │
└─────────────────┘
```

---

## 4️⃣ VISTAS Y LÓGICA (10 minutos)

### ¿Qué son las Vistas?

> "Las vistas son funciones Python que reciben una petición HTTP y devuelven una respuesta. Aquí va toda la lógica del backend."

### Estructura de una Vista

**Mostrar código:**
```python
@login_required  # Requiere login
def lista_bienes(request):
    # 1. Obtener parámetros
    busqueda = request.GET.get('q', '')
    
    # 2. Consultar BD
    bienes = BienPatrimonial.objects.all()
    if busqueda:
        bienes = bienes.filter(nombre__icontains=busqueda)
    
    # 3. Preparar contexto
    context = {'bienes': bienes}
    
    # 4. Renderizar template
    return render(request, 'lista_bienes.html', context)
```

**Explicar paso a paso:**
1. **`@login_required`**: Solo usuarios autenticados pueden acceder
2. **`request.GET.get()`**: Obtiene parámetros de la URL (ej: ?q=computadora)
3. **QuerySet**: `objects.all()` obtiene todos los registros
4. **Filter**: `filter(nombre__icontains=busqueda)` busca en el nombre
5. **Render**: Combina template con datos y devuelve HTML

### Vistas CRUD

#### CREATE (Crear)
```python
def crear_bien(request):
    if request.method == 'POST':
        form = BienForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_bienes')
    else:
        form = BienForm()
    return render(request, 'crear_bien.html', {'form': form})
```

#### READ (Leer)
```python
def ver_bien(request, pk):
    bien = get_object_or_404(BienPatrimonial, pk=pk)
    return render(request, 'ver_bien.html', {'bien': bien})
```

#### UPDATE (Actualizar)
```python
def editar_bien(request, pk):
    bien = get_object_or_404(BienPatrimonial, pk=pk)
    if request.method == 'POST':
        form = BienForm(request.POST, instance=bien)
        if form.is_valid():
            form.save()
            return redirect('lista_bienes')
    else:
        form = BienForm(instance=bien)
    return render(request, 'editar_bien.html', {'form': form})
```

#### DELETE (Eliminar)
```python
def eliminar_bien(request, pk):
    bien = get_object_or_404(BienPatrimonial, pk=pk)
    bien.delete()
    return redirect('lista_bienes')
```

### Funcionalidades Avanzadas

#### 1. **Búsqueda y Filtros**
```python
# Búsqueda en múltiples campos
bienes = bienes.filter(
    Q(nombre__icontains=q) |
    Q(descripcion__icontains=q) |
    Q(numero_identificacion__icontains=q)
)

# Filtro por estado
if estado:
    bienes = bienes.filter(estado=estado)

# Filtro por rango de fechas
if fecha_desde:
    bienes = bienes.filter(fecha_adquisicion__gte=fecha_desde)
```

**Explicar Q objects:**
- `Q()` permite hacer consultas OR
- `__icontains` busca texto sin importar mayúsculas

#### 2. **Sistema de Bajas**
```python
def dar_baja_bien(request, pk):
    bien = get_object_or_404(BienPatrimonial, pk=pk)
    bien.estado = "BAJA"
    bien.fecha_baja = date.today()
    bien.save()
    return redirect('lista_baja_bienes')
```

**Explicar:**
- No se elimina físicamente
- Solo cambia el estado a "BAJA"
- Se puede restaurar después

#### 3. **Carga Masiva desde Excel**
```python
def carga_masiva_bienes(request):
    archivo = request.FILES['archivo_excel']
    df = pd.read_excel(archivo)  # Pandas lee Excel
    
    with transaction.atomic():  # Todo o nada
        for i, row in df.iterrows():
            BienPatrimonial.objects.create(
                nombre=row['descripcion'],
                cantidad=row['cantidad'],
                # ...
            )
```

**Explicar:**
- Usa Pandas para leer Excel
- `transaction.atomic()` asegura consistencia
- Si una fila falla, se deshacen todos los cambios

---

## 5️⃣ DEMO EN VIVO (10 minutos)

### Preparación

**Antes de la presentación:**
1. Tener el servidor corriendo: `python manage.py runserver`
2. Tener datos de prueba en la BD
3. Abrir navegador en http://127.0.0.1:8000/

### Flujo de Demo

#### 1. Login
- Mostrar pantalla de login
- Ingresar credenciales
- Explicar que Django maneja sesiones

#### 2. Dashboard
- Mostrar dashboard según rol (admin/operador)
- Explicar control de acceso por roles

#### 3. Lista de Bienes
- Ver tabla completa de bienes
- Probar búsqueda: buscar "computadora"
- Probar filtros: estado=ACTIVO
- Mostrar ordenamiento

#### 4. Crear Bien
- Ir a formulario de crear bien
- Llenar campos
- Guardar
- Ver mensaje de éxito
- Verificar que aparece en la lista

#### 5. Editar Bien
- Hacer clic en "Editar" de un bien
- Cambiar algún campo
- Guardar
- Verificar cambios

#### 6. Sistema de Bajas
- Dar de baja un bien
- Ver lista de bienes dados de baja
- Restablecer un bien

#### 7. Carga Masiva
- Mostrar archivo Excel de ejemplo
- Subir archivo
- Ver mensaje de bienes creados
- Verificar en lista

#### 8. Admin de Django
- Ir a http://127.0.0.1:8000/admin/
- Mostrar panel de administración
- Ver que Django genera CRUD automático

### Mostrar el Código Detrás

**Después de cada demo, mostrar el código:**
```python
# Por ejemplo, después de crear un bien:
"Esto es lo que pasó en el backend:"

def crear_bien(request):
    if request.method == 'POST':
        form = BienForm(request.POST)
        if form.is_valid():
            form.save()  # ← Aquí se guardó en la BD
            messages.success(request, "Bien creado")
            return redirect('lista_bienes')
```

---

## 6️⃣ CONCEPTOS CLAVE PARA EXPLICAR

### 1. ORM (Object-Relational Mapping)

**Analogía:**
> "El ORM es como un traductor. Tú hablas Python, la base de datos habla SQL. El ORM traduce entre ambos."

**Sin ORM (SQL directo):**
```sql
SELECT * FROM core_bienpatrimonial WHERE estado = 'ACTIVO';
```

**Con ORM Django:**
```python
BienPatrimonial.objects.filter(estado='ACTIVO')
```

### 2. QuerySets (Consultas Perezosas)

**Explicar:**
> "Los QuerySets son 'lazy' (perezosos). No van a la base de datos hasta que realmente necesitas los datos."

```python
# Esto NO ejecuta query
bienes = BienPatrimonial.objects.filter(estado='ACTIVO')

# Esto SÍ ejecuta query
for bien in bienes:  # ← Aquí va a la BD
    print(bien.nombre)
```

### 3. Migraciones

**Explicar:**
> "Las migraciones son como un historial de cambios de la base de datos. Django las crea automáticamente."

```bash
# 1. Modificas un modelo
# 2. Creas migración
python manage.py makemigrations

# 3. Aplicas migración (actualiza BD)
python manage.py migrate
```

### 4. Decoradores

**Explicar:**
> "Los decoradores son funciones que modifican otras funciones. Se usan mucho en Django."

```python
@login_required  # ← Decorador
def mi_vista(request):
    pass

# Es equivalente a:
def mi_vista(request):
    pass
mi_vista = login_required(mi_vista)
```

**Decoradores comunes:**
- `@login_required`: Requiere autenticación
- `@require_POST`: Solo acepta POST
- `@transaction.atomic`: Transacción atómica

### 5. Context y Template

**Explicar:**
> "El context es un diccionario que pasas del backend al template para mostrar datos."

**Backend (views.py):**
```python
def lista_bienes(request):
    bienes = BienPatrimonial.objects.all()
    context = {
        'bienes': bienes,
        'total': bienes.count()
    }
    return render(request, 'lista_bienes.html', context)
```

**Frontend (template):**
```html
<h1>Total de bienes: {{ total }}</h1>
{% for bien in bienes %}
    <tr>
        <td>{{ bien.nombre }}</td>
        <td>{{ bien.estado }}</td>
    </tr>
{% endfor %}
```

---

## 7️⃣ PREGUNTAS FRECUENTES

### Q: ¿Cómo agrego un nuevo campo al modelo?

**A:**
```python
# 1. Agregar campo al modelo
class BienPatrimonial(models.Model):
    # ... campos existentes
    marca = models.CharField(max_length=100, blank=True)  # ← Nuevo

# 2. Crear migración
python manage.py makemigrations

# 3. Aplicar migración
python manage.py migrate
```

### Q: ¿Cómo hago una consulta compleja?

**A:**
```python
from django.db.models import Q

# OR
bienes = BienPatrimonial.objects.filter(
    Q(estado='ACTIVO') | Q(estado='MANTENIMIENTO')
)

# AND
bienes = BienPatrimonial.objects.filter(
    estado='ACTIVO',
    origen='COMPRA'
)

# NOT
from django.db.models import Q
bienes = BienPatrimonial.objects.exclude(estado='BAJA')
```

### Q: ¿Cómo manejo errores?

**A:**
```python
from django.shortcuts import get_object_or_404

def ver_bien(request, pk):
    # Si no existe, retorna 404 automáticamente
    bien = get_object_or_404(BienPatrimonial, pk=pk)
    return render(request, 'ver_bien.html', {'bien': bien})
```

### Q: ¿Cómo valido datos?

**A:**
```python
# En el modelo
def clean(self):
    if self.valor_adquisicion < 0:
        raise ValidationError("El precio no puede ser negativo")

# O en formularios
class BienForm(forms.ModelForm):
    def clean_valor_adquisicion(self):
        valor = self.cleaned_data['valor_adquisicion']
        if valor < 0:
            raise ValidationError("El precio no puede ser negativo")
        return valor
```

---

## 8️⃣ EJERCICIOS PRÁCTICOS PARA TUS COMPAÑEROS

### Ejercicio 1: Crear un bien desde el shell
```python
python manage.py shell

from core.models import BienPatrimonial
bien = BienPatrimonial.objects.create(
    nombre="Mi Primer Bien",
    descripcion="Creado desde el shell"
)
print(f"Bien creado con ID: {bien.clave_unica}")
```

### Ejercicio 2: Consultar bienes activos
```python
activos = BienPatrimonial.objects.filter(estado='ACTIVO')
print(f"Total de bienes activos: {activos.count()}")
for bien in activos[:5]:
    print(f"- {bien.nombre}")
```

### Ejercicio 3: Actualizar un bien
```python
bien = BienPatrimonial.objects.get(pk=1)
bien.nombre = "Nombre Actualizado"
bien.save()
print("Bien actualizado!")
```

### Ejercicio 4: Agregar una nueva vista
```python
# En views.py
@login_required
def bienes_por_origen(request, origen):
    bienes = BienPatrimonial.objects.filter(origen=origen)
    context = {'bienes': bienes, 'origen': origen}
    return render(request, 'bienes_por_origen.html', context)

# En urls.py
path('bienes/origen/<str:origen>/', views.bienes_por_origen, name='bienes_origen')
```

---

## 9️⃣ TIPS PARA UNA BUENA PRESENTACIÓN

### Antes de Presentar:
1. ✅ Practica el flujo completo
2. ✅ Prepara datos de prueba
3. ✅ Verifica que el servidor funcione
4. ✅ Ten el código abierto en tu editor
5. ✅ Prepara ejemplos claros

### Durante la Presentación:
1. 🗣️ Habla despacio y claro
2. 📊 Usa diagramas visuales
3. 💻 Muestra código Y resultado
4. ❓ Haz pausas para preguntas
5. 🎯 Enfócate en conceptos clave

### Después de Presentar:
1. 📝 Comparte esta documentación
2. 🔗 Comparte recursos adicionales
3. 💬 Crea un canal de consultas
4. 🤝 Ofrece ayuda para ejercicios

---

## 🎓 RECURSOS PARA COMPARTIR

### Documentación Oficial:
- Django Docs: https://docs.djangoproject.com/
- Django Tutorial: https://docs.djangoproject.com/en/4.2/intro/tutorial01/

### Tutoriales en Español:
- Django Girls: https://tutorial.djangogirls.org/es/
- Django en Español: https://docs.djangoproject.com/es/4.2/

### Videos Recomendados:
- "Django para principiantes" en YouTube
- Cursos de Django en Platzi/Udemy

### Práctica:
- Django by Example (libro)
- Ejercicios en nuestro repo

---

## 🎯 CHECKLIST DE PRESENTACIÓN

Antes de presentar, verifica:

- [ ] Servidor corriendo sin errores
- [ ] Base de datos con datos de prueba
- [ ] Navegador abierto en la página principal
- [ ] Editor de código con archivos relevantes
- [ ] Terminal con shell de Django lista
- [ ] Diapositivas o pizarra preparada
- [ ] Archivo Excel de ejemplo para carga masiva
- [ ] Documentación impresa o compartida
- [ ] Ejemplos de código preparados
- [ ] Preguntas frecuentes revisadas

---

## 📞 CONTACTO Y SOPORTE

**Después de la presentación:**
- 💬 Canal de Slack/Discord del equipo
- 📧 Email del líder técnico
- 📝 Issues en GitHub para dudas
- 🤝 Sesiones de pair programming

---

**¡Éxito en tu presentación! 🚀**

Recuerda: El objetivo no es que entiendan TODO, sino que comprendan:
1. ✅ La arquitectura general (MTV)
2. ✅ Cómo funcionan los modelos
3. ✅ Cómo crear vistas básicas
4. ✅ Dónde buscar más información

**¡Con esta guía estás listo para explicar el backend del sistema! 💪**
