# Plan: Revertir 8 commits de lucaskiernicki

## Commits a revertir (del más reciente al más antiguo)

| # | Hash | Autor | Descripción |
|---|------|-------|-------------|
| 1 | `5bfb162` | lucaskiernicki | 0005: set missing fecha_adquisicion before altering to avoid NOT NULL errors |
| 2 | `328600b` | lucaskiernicki | Add core migrations 0002 and 0004 (track migrations) |
| 3 | `842ea3e` | lucaskiernicki | Stop ignoring migration .py files: ensure migrations are tracked |
| 4 | `46c403d` | lucaskiernicki | 0001_initial: add Notificacion model creation |
| 5 | `c4d163d` | lucaskiernicki | Whitelist and add restored 0001_initial migration |
| 6 | `d1e2622` | lucaskiernicki | Restore migration 0003_add_numero_compra_bien and whitelist in .gitignore |
| 7 | `e842d2d` | lucaskiernicki | Reportes: ajustar .alta-header para coincidir con alta_operadores |
| 8 | `a23fc19` | lucaskiernicki | Reportes: UI: cuadro título, buscador y filtros; backend: q and f_estado filters; add reportes.css |

## Problemas críticos detectados

1. **`core/migrations/0001_initial.py` tiene ERROR DE SINTAXIS GRAVE**: el modelo `Notificacion` está insertado en medio del diccionario `options` de `BienPatrimonial`. Esto rompe cualquier comando Django.
2. **Migraciones duplicadas en el filesystem** (mismo número, diferentes nombres).
3. En el commit anterior (`893805a`), `core/migrations/` solo tenía `__init__.py`.

## Estrategia: `git revert` (orden del más antiguo al más reciente)

`git revert` preserva la historia del repo y es seguro para branches compartidos.

## Pasos detallados

### Paso 1: Revertir `a23fc19` (Reportes UI + filtros)
- Eliminar filtros `q` y `f_estado` de `reportes_view()` en `core/views.py`
- Eliminar archivo nuevo `static/css/reportes.css`
- Revertir `templates/reportes.html`

### Paso 2: Revertir `e842d2d` (Reportes alta-header)
- Revertir ajustes CSS (el archivo ya no existirá tras paso 1)

### Paso 3: Revertir `d1e2622` (Restore migration 0003)
- Eliminar `core/migrations/0003_add_numero_compra_bien.py`
- Revertir `.gitignore`

### Paso 4: Revertir `c4d163d` (Whitelist 0001_initial)
- Eliminar `core/migrations/0001_initial.py`
- Revertir `.gitignore`

### Paso 5: Revertir `46c403d` (0001_initial Notificacion)
- Revertir modificaciones en `core/migrations/0001_initial.py` (ya eliminado en paso 4)

### Paso 6: Revertir `842ea3e` (Stop ignoring migrations)
- Revertir `.gitignore` para que vuelva a ignorar `*/migrations/*.py`

### Paso 7: Revertir `328600b` (Add migrations 0002 y 0004)
- Eliminar `core/migrations/0002_notificacion_eliminada_operador_dni_and_more.py`
- Eliminar `core/migrations/0004_bienpatrimonial_siem.py`

### Paso 8: Revertir `5bfb162` (0005 fecha_adquisicion)
- Eliminar `core/migrations/0005_remove_operador_email_and_more.py`

### Paso 9: Limpieza de migraciones huérfanas/duplicadas
Eliminar estos archivos que NO fueron creados por los 8 commits pero causan conflictos:
- `core/migrations/0002_usuario_numero_doc_alter_bienpatrimonial_estado_and_more.py`
- `core/migrations/0003_alter_usuario_tipo_usuario.py`
- `core/migrations/0004_alter_usuario_tipo_usuario.py`
- `core/migrations/0005_notificacion_eliminada_operador_dni_and_more.py`

### Paso 10: Verificación
- `python manage.py check`
- Asegurar que no queden archivos de migración rotos

## Archivos a modificar/eliminar

- `.gitignore`
- `core/views.py`
- `static/css/reportes.css` → ELIMINAR
- `templates/reportes.html`
- `core/migrations/0001_initial.py` → ELIMINAR
- `core/migrations/0002_notificacion_eliminada_operador_dni_and_more.py` → ELIMINAR
- `core/migrations/0003_add_numero_compra_bien.py` → ELIMINAR
- `core/migrations/0004_bienpatrimonial_siem.py` → ELIMINAR
- `core/migrations/0005_remove_operador_email_and_more.py` → ELIMINAR
- `core/migrations/0002_usuario_numero_doc_alter_bienpatrimonial_estado_and_more.py` → ELIMINAR
- `core/migrations/0003_alter_usuario_tipo_usuario.py` → ELIMINAR
- `core/migrations/0004_alter_usuario_tipo_usuario.py` → ELIMINAR
- `core/migrations/0005_notificacion_eliminada_operador_dni_and_more.py` → ELIMINAR

