# 🔌 API REST - Sistema de Gestión de Bienes Patrimoniales

## 📋 Índice
1. [Introducción](#introducción)
2. [Autenticación](#autenticación)
3. [Endpoints Principales](#endpoints-principales)
4. [Ejemplos de Uso](#ejemplos-de-uso)

---

## 🌐 Introducción

El backend del sistema expone endpoints basados en Django Views que manejan la lógica de negocio para la gestión de bienes patrimoniales.

### Base URL
```
http://localhost:8000/
```

### Formato de Respuesta
- **HTML Templates**: Las vistas retornan HTML renderizado
- **Redirects**: Después de operaciones POST exitosas
- **Messages**: Usa Django Messages Framework para feedback

---

## 🔐 Autenticación

### Login
```http
POST /login/
Content-Type: application/x-www-form-urlencoded

usuario=admin&contrasena=password123
```

### Protección de Rutas
- **Cookie de sesión válida**: `sessionid`
- **CSRF Token**: Para operaciones POST

---

## 📦 Endpoints Principales

### Bienes Patrimoniales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/lista-bienes/` | Lista de bienes con filtros |
| GET/POST | `/bienes/<pk>/editar/` | Editar bien |
| POST | `/bienes/<pk>/eliminar/` | Eliminar bien |
| POST | `/carga-masiva/` | Carga desde Excel |

### Bajas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/bienes/bajas/` | Lista de bajas |
| POST | `/bienes/<pk>/dar-baja/` | Dar de baja |
| POST | `/bienes/<pk>/restablecer/` | Restablecer |
| POST | `/bienes/<pk>/eliminar-definitivo/` | Eliminar físicamente |

### Parámetros de Filtrado

**Lista de bienes** (`/lista-bienes/`):
- `q`: Búsqueda general
- `f_origen`: Filtro por origen (COMPRA, DONACION, etc.)
- `f_estado`: Filtro por estado (ACTIVO, BAJA, etc.)
- `f_desde` / `f_hasta`: Rango de fechas (YYYY-MM-DD)
- `orden`: Ordenamiento (fecha, -fecha, precio, -precio)

---

## 💡 Ejemplos de Uso

### Login y Lista
```bash
# Login
curl -c cookies.txt -X POST http://localhost:8000/login/ \
  -d "usuario=admin" \
  -d "contrasena=admin123"

# Listar bienes
curl -b cookies.txt http://localhost:8000/lista-bienes/
```

### Búsqueda con Filtros
```bash
curl -b cookies.txt \
  "http://localhost:8000/lista-bienes/?q=monitor&f_estado=ACTIVO"
```

### Carga Masiva Excel
```bash
curl -b cookies.txt -X POST http://localhost:8000/carga-masiva/ \
  -F "archivo_excel=@bienes.xlsx" \
  -F "sector=Informática"
```

---

Para más detalles, consultar `BACKEND.md` en el directorio raíz del proyecto.

**Última actualización**: Octubre 2024
