from django.conf import settings
from django.db import models


class ArchivoCargaMasiva(models.Model):
    nombre_archivo = models.CharField(max_length=255)
    hash_archivo = models.CharField(max_length=64, unique=True)
    hash_contenido = models.CharField(max_length=64, null=True, blank=True, db_index=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="archivos_carga_masiva",
    )
    fecha_carga = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Archivo de carga masiva"
        verbose_name_plural = "Archivos de carga masiva"
        ordering = ["-fecha_carga"]
        indexes = [
            models.Index(fields=["hash_archivo"]),
        ]

    def __str__(self):
        return f"{self.nombre_archivo} ({self.fecha_carga:%Y-%m-%d %H:%M})"
