# ⚡ Quick Reference - Backend Sistema de Bienes

## 🚀 Comandos Rápidos

### Desarrollo
```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements/base.txt
pip install -r requirements/development.txt

# Configurar ambiente
cp enviroment/env_development .env

# Migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver

# Tests
python manage.py test
```

### Shell de Django
```bash
python manage.py shell

# Dentro del shell:
from core.models import BienPatrimonial, Expediente
bienes = BienPatrimonial.objects.all()
```

---

## 📊 Modelos Principales

### BienPatrimonial
```python
bien = BienPatrimonial.objects.create(
    nombre="Monitor LCD",
    descripcion="Monitor 24 pulgadas",
    cantidad=1,
    origen="COMPRA",
    estado="ACTIVO",
    valor_adquisicion=25000.00,
    servicios="Informática"
)
```

### Expediente
```python
exp = Expediente.objects.create(
    numero_expediente="EXP-2024-001",
    proveedor="Proveedor SA"
)
```

---

## 🌐 URLs Principales

| URL | Descripción |
|-----|-------------|
| `/admin/` | Panel de administración |
| `/login/` | Login de usuarios |
| `/lista-bienes/` | Lista de bienes |
| `/carga-masiva/` | Carga desde Excel |
| `/bienes/bajas/` | Bienes dados de baja |

---

## 🔍 Búsquedas y Filtros

### Búsqueda General
```
/lista-bienes/?q=computadora
```

### Filtros Combinados
```
/lista-bienes/?f_origen=COMPRA&f_estado=ACTIVO&orden=-fecha
```

### Rango de Fechas
```
/lista-bienes/?f_desde=2024-01-01&f_hasta=2024-12-31
```

---

## 📝 Constantes

### Estados
- `ACTIVO`
- `MANTENIMIENTO`
- `INACTIVO`
- `BAJA`

### Orígenes
- `COMPRA`
- `DONACION`
- `TRANSFERENCIA`
- `OMISION`

---

## 🔐 Roles de Usuario

### Administrador (admin)
- Acceso completo
- Dashboard: `/home_admin/`
- Puede crear/editar/eliminar

### Empleado (empleado)
- Acceso limitado
- Dashboard: `/operadores/`
- Operaciones según permisos

---

## 📤 Formato de Excel para Carga Masiva

### Columnas Requeridas (mínimo)
- **Descripcion**: Texto descriptivo del bien

### Columnas Opcionales
- N de ID
- Cantidad
- Origen (compra/donación/etc.)
- Estado (activo/baja/etc.)
- Precio
- Fecha de Alta
- Servicios
- N de Expediente
- N de Serie
- Observaciones

### Ejemplo de Fila
```
| N de ID | Descripcion | Cantidad | Origen | Estado | Precio | Servicios |
|---------|-------------|----------|--------|--------|--------|-----------|
| B001    | Monitor LCD | 1        | Compra | Activo | 25000  | IT        |
```

---

## 🛠️ Debugging

### Ver Logs
```bash
tail -f logs/app.log
```

### Inspeccionar BD
```bash
python manage.py dbshell
# En SQLite:
.tables
.schema core_bienpatrimonial
SELECT * FROM core_bienpatrimonial LIMIT 5;
```

### Reset de BD (solo desarrollo)
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 🔄 Workflow de Baja de Bienes

1. **Dar de baja**: `POST /bienes/<pk>/dar-baja/`
   - Estado → BAJA
   - Registra fecha y motivo

2. **Ver bajas**: `GET /bienes/bajas/`
   - Lista todos los bienes dados de baja

3. **Restablecer**: `POST /bienes/<pk>/restablecer/`
   - Estado → ACTIVO
   - Limpia datos de baja

4. **Eliminar**: `POST /bienes/<pk>/eliminar-definitivo/`
   - ⚠️ Eliminación física (no reversible)

---

## 📦 Estructura de Respuesta

### Operación Exitosa
- Redirección: `302 Found`
- Mensaje: `messages.success()`
- Destino: Lista correspondiente

### Error
- Redirección con mensaje: `messages.error()`
- O: Template con errores de formulario

---

## 🔒 Seguridad

### CSRF Token
```html
<form method="POST">
  {% csrf_token %}
  <!-- form fields -->
</form>
```

### Login Requerido
```python
@login_required
def vista_protegida(request):
    # código de la vista
```

### Validación de Permisos
```python
if request.user.tipo_usuario != 'admin':
    return redirect('operadores')
```

---

## 📊 Queries Comunes

### Buscar por múltiples campos
```python
from django.db.models import Q

bienes = BienPatrimonial.objects.filter(
    Q(descripcion__icontains='laptop') |
    Q(servicios__icontains='laptop')
)
```

### Con relación
```python
bienes = BienPatrimonial.objects.select_related('expediente').filter(
    expediente__numero_expediente='EXP-2024-001'
)
```

### Contar y agrupar
```python
from django.db.models import Count

# Contar por estado
stats = BienPatrimonial.objects.values('estado').annotate(
    total=Count('clave_unica')
)
```

---

## ⚙️ Variables de Entorno

```bash
DJANGO_ENV=development
DEBUG=True
SECRET_KEY=tu-clave-secreta
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 🎯 Próximos Pasos Recomendados

### Para Desarrollo
- [ ] Implementar paginación
- [ ] Agregar exportación a PDF
- [ ] API REST con DRF
- [ ] Tests automatizados completos

### Para Producción
- [ ] Migrar a PostgreSQL
- [ ] Configurar servidor web (Nginx/Apache)
- [ ] SSL/HTTPS
- [ ] Backups automáticos
- [ ] Monitoring y logging avanzado

---

## 📞 Soporte

Para más información consultar:
- `BACKEND.md` - Documentación completa
- `docs/BACKEND_API.md` - Referencia de API
- `docs/BACKEND_ARCHITECTURE.md` - Arquitectura del sistema

---

**Última actualización**: Octubre 2024
