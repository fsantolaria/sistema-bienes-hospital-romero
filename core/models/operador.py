from django.db import models
from .usuario import Usuario

class Operador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=300, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    dni = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = "Operador"
        verbose_name_plural = "Operadores"
        ordering = ['nombre_completo']

    def __str__(self) -> str:
        return str(self.nombre_completo)

    @property
    def email(self) -> str:
        if self.usuario and hasattr(self.usuario, 'email'):
            return self.usuario.email
        return ""

    @property
    def username(self) -> str:
        if self.usuario and hasattr(self.usuario, 'username'):
            return self.usuario.username
        return ""