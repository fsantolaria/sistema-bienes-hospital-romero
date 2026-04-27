from django.db import models


class ServicioExtra(models.Model):
    nombre = models.CharField(max_length=200, unique=True, verbose_name="Nombre del servicio")

    class Meta:
        verbose_name = "Servicio Extra"
        verbose_name_plural = "Servicios Extra"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


