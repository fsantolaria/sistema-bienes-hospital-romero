# 📚 Documentación del Backend

Este directorio contiene la documentación completa del backend del Sistema de Gestión de Bienes Patrimoniales.

## 📖 Documentos Disponibles

### 1. [BACKEND.md](../BACKEND.md) (Documento Principal)
**Documentación completa y detallada del backend**

Contenido:
- ✅ Arquitectura general del sistema
- ✅ Stack tecnológico completo
- ✅ Estructura del proyecto
- ✅ Modelos de datos (BienPatrimonial, Expediente, Usuario, Operador)
- ✅ Vistas y URLs
- ✅ Sistema de autenticación y permisos
- ✅ Configuración de base de datos
- ✅ Gestión de configuración por ambiente
- ✅ API endpoints disponibles
- ✅ Comandos útiles de Django
- ✅ Debugging y troubleshooting

**Ideal para**: Desarrolladores que necesitan entender el sistema completo

---

### 2. [BACKEND_API.md](BACKEND_API.md)
**Referencia de API y endpoints**

Contenido:
- ✅ Endpoints de autenticación
- ✅ Endpoints de gestión de bienes
- ✅ Endpoints de sistema de bajas
- ✅ Parámetros de filtrado y búsqueda
- ✅ Formato de carga masiva Excel
- ✅ Códigos de estado HTTP
- ✅ Ejemplos de uso con curl
- ✅ Medidas de seguridad (CSRF, sesiones)

**Ideal para**: Desarrolladores frontend, testers, integraciones

---

### 3. [BACKEND_ARCHITECTURE.md](BACKEND_ARCHITECTURE.md)
**Diagramas y arquitectura del sistema**

Contenido:
- ✅ Diagrama de arquitectura general
- ✅ Diagrama de modelos de datos (ER)
- ✅ Flujo de datos CRUD
- ✅ Flujo de autenticación
- ✅ Flujo de sistema de bajas
- ✅ Estructura de paquetes
- ✅ Componentes clave (ORM, Middleware)
- ✅ Ciclo de Request/Response
- ✅ Optimizaciones implementadas
- ✅ Patrones de diseño utilizados

**Ideal para**: Arquitectos de software, desarrolladores senior, documentación técnica

---

### 4. [BACKEND_QUICK_REFERENCE.md](BACKEND_QUICK_REFERENCE.md)
**Guía rápida de referencia**

Contenido:
- ✅ Comandos rápidos más usados
- ✅ Ejemplos de modelos
- ✅ URLs principales
- ✅ Búsquedas y filtros
- ✅ Constantes del sistema
- ✅ Roles de usuario
- ✅ Formato de Excel para carga masiva
- ✅ Workflow de bajas
- ✅ Queries comunes
- ✅ Variables de entorno

**Ideal para**: Uso diario, consultas rápidas, nuevos desarrolladores

---

## 🎯 ¿Qué documento leer según tu necesidad?

### Quiero entender el sistema completo
→ Empieza con [BACKEND.md](../BACKEND.md)

### Necesito integrarme con el backend
→ Consulta [BACKEND_API.md](BACKEND_API.md)

### Quiero ver la arquitectura y diagramas
→ Revisa [BACKEND_ARCHITECTURE.md](BACKEND_ARCHITECTURE.md)

### Necesito una consulta rápida
→ Usa [BACKEND_QUICK_REFERENCE.md](BACKEND_QUICK_REFERENCE.md)

### Soy nuevo en el proyecto
→ Lee en este orden:
1. [BACKEND_QUICK_REFERENCE.md](BACKEND_QUICK_REFERENCE.md)
2. [BACKEND_ARCHITECTURE.md](BACKEND_ARCHITECTURE.md)
3. [BACKEND.md](../BACKEND.md)
4. [BACKEND_API.md](BACKEND_API.md)

---

## 🔑 Conceptos Clave

### Modelos Principales

| Modelo | Descripción | Archivo |
|--------|-------------|---------|
| `BienPatrimonial` | Bien patrimonial del hospital | `core/models/bien_patrimonial.py` |
| `Expediente` | Expediente administrativo | `core/models/expediente.py` |
| `Usuario` | Usuario del sistema (auth custom) | `core/models/usuario.py` |
| `Operador` | Perfil de operador | `core/models/operador.py` |

### Vistas Principales

| Vista | URL | Descripción |
|-------|-----|-------------|
| `lista_bienes` | `/lista-bienes/` | Lista de bienes con filtros |
| `editar_bien` | `/bienes/<pk>/editar/` | Editar bien |
| `carga_masiva_bienes` | `/carga-masiva/` | Carga desde Excel |
| `dar_baja_bien` | `/bienes/<pk>/dar-baja/` | Dar de baja |
| `lista_baja_bienes` | `/bienes/bajas/` | Lista de bajas |

### Estados de Bienes

- **ACTIVO**: En uso normal
- **MANTENIMIENTO**: En reparación
- **INACTIVO**: Fuera de servicio temporalmente
- **BAJA**: Dado de baja (reversible hasta eliminar definitivamente)

### Orígenes de Bienes

- **COMPRA**: Adquirido mediante compra (requiere precio)
- **DONACION**: Recibido como donación
- **TRANSFERENCIA**: Transferido desde otra área
- **OMISION**: Registro de omisión anterior

---

## 🚀 Inicio Rápido

```bash
# 1. Clonar repositorio
git clone https://github.com/fsantolaria/sistema-bienes-hospital-romero.git
cd sistema-bienes-hospital-romero

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
.\venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements/base.txt
pip install -r requirements/development.txt

# 4. Configurar ambiente
cp enviroment/env_development .env

# 5. Migraciones
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Ejecutar servidor
python manage.py runserver

# Acceder a:
# - Aplicación: http://localhost:8000/
# - Admin: http://localhost:8000/admin/
```

---

## 🛠️ Tecnologías Utilizadas

### Backend Framework
- **Django 4.2.7**: Framework web principal
- **Python 3.10+**: Lenguaje de programación

### Base de Datos
- **SQLite3**: Base de datos (desarrollo, testing, producción)

### Librerías Principales
- **pandas**: Procesamiento de datos Excel
- **openpyxl**: Lectura/escritura de archivos Excel
- **django-crispy-forms**: Formularios mejorados
- **django-filter**: Filtros avanzados
- **python-decouple**: Gestión de configuración
- **whitenoise**: Servir archivos estáticos

---

## 📞 Soporte y Contacto

**Equipo de Desarrollo**
- Docentes: Karina Alvarez, Alejandra, Felipe Morales, Fernando Diego Santolaria
- Estudiantes: ISFDyT 210

**Repositorio**
- GitHub: https://github.com/fsantolaria/sistema-bienes-hospital-romero

---

## 📝 Notas de Versión

### Versión Actual
- Django 4.2.7
- Python 3.10+
- SQLite3

### Funcionalidades Implementadas
- ✅ CRUD de bienes patrimoniales
- ✅ Sistema de autenticación con roles
- ✅ Carga masiva desde Excel
- ✅ Búsqueda y filtros avanzados
- ✅ Sistema de bajas reversible
- ✅ Panel de administración personalizado
- ✅ Gestión de expedientes
- ✅ Validaciones robustas
- ✅ Logging de aplicación

---

**Última actualización**: Octubre 2024
