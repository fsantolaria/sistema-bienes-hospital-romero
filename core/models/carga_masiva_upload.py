# core/models/carga_masiva_upload.py
from django.conf import settings
from django.db import models


class CargaMasivaUpload(models.Model):
    """
    Registro de auditoría para cada carga masiva de relevamientos.
    No guarda el archivo binario (filesystem de Vercel es efímero).
    """
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="cargas_masivas",
    )
    archivo_nombre = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)
    total_filas_leidas = models.IntegerField(default=0)
    total_filas_cargadas = models.IntegerField(default=0)
    total_filas_omitidas = models.IntegerField(default=0)
    columnas_no_reconocidas = models.JSONField(default=list)
    warnings = models.JSONField(default=list)
    resumen = models.JSONField(default=dict)

    class Meta:
        verbose_name = "Carga masiva (upload)"
        verbose_name_plural = "Cargas masivas (uploads)"
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.archivo_nombre} ({self.fecha:%Y-%m-%d %H:%M}) — {self.total_filas_cargadas} cargados"

    @property
    def tiene_columnas_no_reconocidas(self):
        return bool(self.columnas_no_reconocidas)
