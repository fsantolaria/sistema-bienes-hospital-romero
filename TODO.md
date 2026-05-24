# TODO

- [ ] Crear campo `ultima_actualizacion_estado` en `BienPatrimonial` (DateTimeField, null=True).
- [ ] Migración para agregar campo.
- [ ] Actualizar vistas que cambian estado (`dar_baja_bien`, `dar_baja_bienes_seleccionados`, `restablecer_bien`, `restablecer_bienes_seleccionados`, `editar_bien` si aplica) para setear `ultima_actualizacion_estado=timezone.now()`.
- [ ] Actualizar `reportes_view` y `reportes_pdf` para que el filtro `scope=24h/12h/6h` use `ultima_actualizacion_estado` (OR con el comportamiento actual si querés compatibilidad).
- [ ] Verificar templates `reportes.html` y `reportes_pdf.html` no requieren cambios (ya muestran `estado`).
- [ ] Ejecutar migraciones y probar manualmente: cambiar estado y confirmar que aparece en scope correspondiente.

