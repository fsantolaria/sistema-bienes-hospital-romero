from django.db import models
from django.conf import settings

class LogActividad(models.Model):
    ACCIONES = [
        ('LOGIN', 'Inicio de Sesión'),
        ('CARGA', 'Carga de Bien'),
        ('CARGA_MASIVA', 'Carga Masiva'),
        ('EDICION', 'Edición de Bien'),
        ('BAJA', 'Baja de Bien'),
        ('ELIMINACION', 'Eliminación Definitiva'),
        ('RESTABLECIMIENTO', 'Restablecimiento de Bien'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Usuario"
    )
    accion = models.CharField(max_length=20, choices=ACCIONES, verbose_name="Acción")
    mensaje = models.TextField(verbose_name="Mensaje/Detalle")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")

    # Bien asociado al evento (para que los reportes respeten el historial)
    bien = models.ForeignKey(
        'core.BienPatrimonial',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='logs',
    )
    bien_clave_unica = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Clave Única del Bien',
    )

    class Meta:
        verbose_name = "Log de Actividad"
        verbose_name_plural = "Logs de Actividad"
        ordering = ['-fecha']

    def __str__(self):
        user_str = self.usuario.username if self.usuario else "Sistema"
        return f"{self.fecha.strftime('%d/%m/%Y %H:%M')} - {user_str}: {self.get_accion_display()}"
