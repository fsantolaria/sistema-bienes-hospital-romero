# Tarjetas para Tablero GitHub

## Tarjeta 1: Reportes de bienes únicos con impacto por alta, baja y restablecimiento

**Tipo:** Feature  
**Estado sugerido:** Done  
**Prioridad:** Alta  
**Archivos:** `core/views.py`, `templates/reportes.html`

### Descripción
Se ajustó la lógica de reportes para que muestre bienes únicos, sin duplicarse por cada modificación. Un bien entra al reporte cuando tiene una acción relevante: alta, carga masiva, baja o restablecimiento.

### Cambios realizados
- Se centralizó el rango de reportes en `_rango_reportes`.
- Se creó `_bienes_reportes_queryset` para obtener bienes únicos impactados por acciones relevantes.
- Se usa `Max("logs__fecha")` para ordenar por última acción de reporte sin duplicar filas.
- Se mantuvieron filtros por texto y servicios sobre los datos actuales del bien.
- Se eliminó la vista basada en movimientos duplicados dentro de `reportes.html`.

### Criterios de aceptación
- Al crear un bien, aparece en reportes del rango correspondiente.
- Al dar de baja un bien, aparece con estado y fecha de baja actualizados.
- Al restablecer un bien, aparece una sola vez con datos actualizados.
- Si se edita un bien ya reportado, la información se actualiza sin generar una fila duplicada.

---

## Tarjeta 2: Registrar logs asociados al bien para reportes confiables

**Tipo:** Mejora técnica  
**Estado sugerido:** Done  
**Prioridad:** Alta  
**Archivo:** `core/views.py`

### Descripción
Se mejoró el registro de actividad para asociar cada acción relevante con el bien correspondiente, permitiendo que los reportes identifiquen correctamente qué bienes fueron impactados.

### Cambios realizados
- `registrar_log` ahora acepta el parámetro opcional `bien`.
- Se guarda `bien` y `bien_clave_unica` en `LogActividad`.
- La carga individual registra el bien creado.
- La baja individual registra el bien dado de baja.
- La baja masiva registra un log por cada bien.
- El restablecimiento individual y masivo registran cada bien restablecido.

### Criterios de aceptación
- Cada alta, baja o restablecimiento queda vinculado al bien.
- Las bajas/restablecimientos masivos impactan correctamente en reportes por cada bien seleccionado.
- Los reportes pueden filtrar y ordenar por acciones relevantes sin perder trazabilidad.

---

## Tarjeta 3: Actualizar fechas al restablecer bienes dados de baja

**Tipo:** Feature  
**Estado sugerido:** Done  
**Prioridad:** Media  
**Archivo:** `core/views.py`

### Descripción
Se ajustó el comportamiento al restablecer bienes para que la fecha de alta se actualice y la fecha de baja se limpie.

### Cambios realizados
- Al restablecer un bien individual, `fecha_adquisicion` pasa a la fecha actual.
- Al restablecer bienes masivamente, cada bien actualiza `fecha_adquisicion`.
- Al cambiar desde edición de `BAJA` a `ACTIVO`, se actualiza `fecha_adquisicion`.
- Al restablecer se limpia `fecha_baja`, `expediente_baja` y `descripcion_baja`.

### Criterios de aceptación
- Un bien dado de baja muestra fecha de baja en reportes.
- Al volver a activo, desaparece la fecha de baja.
- Al volver a activo, la fecha de alta queda actualizada al día del restablecimiento.

---

## Tarjeta 4: Mejorar visualización de estados en reportes

**Tipo:** UI  
**Estado sugerido:** Done  
**Prioridad:** Media  
**Archivo:** `templates/reportes.html`

### Descripción
Se alineó la columna Estado de reportes con el diseño usado en las listas de bienes mediante cápsulas de colores.

### Cambios realizados
- `ACTIVO`: cápsula verde.
- `INACTIVO`: cápsula gris.
- `MANTENIMIENTO`: cápsula celeste.
- `BAJA`: cápsula roja.
- Estado vacío: texto tenue.

### Criterios de aceptación
- Los estados del reporte se identifican visualmente con cápsulas.
- El diseño queda consistente con las listas de bienes.

---

## Tarjeta 5: Mejorar flujo de baja múltiple

**Tipo:** UX  
**Estado sugerido:** Done  
**Prioridad:** Alta  
**Archivo:** `templates/bienes/lista_bienes.html`

### Descripción
Se mejoró el flujo de baja múltiple para que el panel contador y el formulario final no se superpongan, y para que el usuario pueda volver a cancelar la selección si cierra el formulario de motivos.

### Cambios realizados
- Al confirmar desde el panel contador, se oculta el panel de baja múltiple.
- Se abre el formulario final con fecha, expediente, motivo y confirmación.
- Si se cierra el formulario final sin enviar, vuelve a aparecer el panel contador.
- Si se confirma la baja final, se limpia la selección guardada.

### Criterios de aceptación
- El panel contador desaparece al abrir el formulario de motivos.
- Al tocar afuera del formulario de motivos, vuelve el panel contador.
- El usuario puede cancelar la selección después de cerrar el formulario final.
- Al confirmar la baja final, no reaparece el contador.

---

## Tarjeta 6: Ajustar vista de supervisor

**Tipo:** UI  
**Estado sugerido:** Done  
**Prioridad:** Baja  
**Archivo:** `templates/bienes/lista_bienes_supervisor.html`

### Descripción
Se limpió la cabecera de la lista de bienes del supervisor quitando el botón decorativo "Solo lectura".

### Cambios realizados
- Se eliminó el botón "Solo lectura".
- Se mantuvo disponible el botón "Lista de bajas".

### Criterios de aceptación
- La lista del supervisor ya no muestra el botón "Solo lectura".
- El acceso a lista de bajas sigue visible.

---

## Tarjeta 7: Verificaciones realizadas

**Tipo:** QA  
**Estado sugerido:** Done  
**Prioridad:** Media  

### Descripción
Se validaron los cambios principales con checks de Django, carga de templates y render de vistas clave.

### Validaciones ejecutadas
- `DEBUG=True ./.venv/bin/python manage.py check`
- Render de `/reportes/`
- Render de `/reportes/pdf/`
- Carga de template `bienes/lista_bienes.html`
- Carga de template `bienes/lista_bienes_supervisor.html`
- Prueba de duplicados en reportes: `duplicates 0`

### Criterios de aceptación
- Django no reporta errores de configuración o rutas.
- Los templates modificados cargan correctamente.
- Reportes web y PDF responden correctamente.
- El reporte no duplica bienes.

---

## Tarjeta 8: Backend - visualización de reportes para supervisor

**Tipo:** Backend / Permisos  
**Estado sugerido:** Done  
**Prioridad:** Alta  
**Archivo:** `core/views.py`

### Descripción
Se habilitó a los usuarios con rol supervisor para consultar reportes sin otorgarles permisos administrativos sobre bienes.

### Cambios realizados
- Se permitió que el supervisor acceda a la vista de reportes.
- Se mantiene el contexto de permisos del usuario para renderizar reportes en modo consulta.
- Se preservan restricciones para impedir acciones administrativas desde el rol supervisor.

### Criterios de aceptación
- Un usuario supervisor autenticado puede acceder a reportes.
- El supervisor puede visualizar datos del reporte.
- El supervisor no adquiere permisos de alta, edición, baja, restablecimiento ni eliminación.

---

## Tarjeta 9: Frontend - acceso a reportes en home supervisor

**Tipo:** Frontend / UI  
**Estado sugerido:** Done  
**Prioridad:** Alta  
**Archivo:** `templates/home_supervisor.html`

### Descripción
Se agregó en el home del supervisor un acceso visible a reportes para que pueda ingresar directamente desde su panel.

### Cambios realizados
- El home del supervisor muestra el botón de reportes.
- El acceso apunta a la ruta `reportes`.
- El botón mantiene el estilo de los botones del home.

### Criterios de aceptación
- El supervisor ve un acceso a reportes desde su home.
- Al presionar el botón, navega a reportes.
- El acceso se muestra integrado con el diseño del panel del supervisor.

---

## Tarjeta 10: Backend - visualización de lista de bajas para supervisor

**Tipo:** Backend / Permisos  
**Estado sugerido:** Done  
**Prioridad:** Alta  
**Archivo:** `core/views.py`

### Descripción
Se habilitó a los usuarios con rol supervisor para consultar la lista de bienes dados de baja sin permitirles ejecutar acciones de restablecimiento o modificación.

### Cambios realizados
- El supervisor puede acceder a la vista de bienes dados de baja.
- Se conserva el contexto de permisos para distinguir supervisor de administrador.
- Las acciones de restablecimiento siguen restringidas a administradores.
- Se mantiene la seguridad del backend aunque el usuario manipule el frontend.

### Criterios de aceptación
- Un usuario supervisor autenticado puede acceder a la lista de bajas.
- La lista muestra bienes dados de baja en modo consulta.
- El supervisor no puede restablecer bienes.
- Las acciones sensibles siguen reservadas para administradores.

---

## Tarjeta 11: Frontend - acceso a lista de bajas para supervisor

**Tipo:** Frontend / UI  
**Estado sugerido:** Done  
**Prioridad:** Alta  
**Archivo:** `templates/bienes/lista_bienes_supervisor.html`

### Descripción
Se mantuvo en la lista de bienes del supervisor un acceso claro a la lista de bienes dados de baja y se limpió la cabecera quitando elementos visuales innecesarios.

### Cambios realizados
- La lista de bienes del supervisor muestra el botón "Lista de bajas".
- Se eliminó el botón decorativo "Solo lectura".
- La cabecera queda enfocada en navegación útil.
- La interfaz no muestra acciones administrativas.

### Criterios de aceptación
- El supervisor ve un acceso a lista de bajas desde su lista de bienes.
- Al presionar el botón, navega a la lista de bajas.
- La cabecera queda limpia, sin el botón "Solo lectura".
- No se muestran acciones administrativas en la vista del supervisor.
