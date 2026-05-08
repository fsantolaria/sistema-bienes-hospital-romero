from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings

# --- Modelo de dominio: EmpleadoHospital ---
# Registra personal del hospital (NO necesariamente usuarios del sistema).
# Se usa para asignar responsables a Bienes Patrimoniales y consultar por sector/cargo/estado.
# Incluye: DNI y legajo únicos, datos personales y de contacto, info laboral y auditoría.
# Validación: el DNI debe tener al menos 7 dígitos (ignorando guiones/espacios).

class EmpleadoHospital(models.Model):
    ESTADO_CHOICES = (('ACTIVO', 'Activo'), ('INACTIVO', 'Inactivo'))
    CARGO_CHOICES = (
        ('ADMIN', 'Administrativo'),
        ('MEDICO', 'Médico'),
        ('ENFERMERIA', 'Enfermería'),
        ('TECNICO', 'Técnico'),
        ('OTRO', 'Otro'),
    )

    # Identificación (únicos para evitar duplicados)
    dni = models.CharField(max_length=20, unique=True)
    legajo = models.CharField(max_length=20, unique=True)

    # Datos personales
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    # Contacto
    email = models.EmailField(unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True)

    # Laboral
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES, default='OTRO')
    sector = models.CharField(max_length=120, blank=True)
    fecha_ingreso = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVO')

    # Auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario_creacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['apellido', 'nombre']
        indexes = [
            models.Index(fields=['dni']),
            models.Index(fields=['legajo']),
            models.Index(fields=['estado']),
            models.Index(fields=['cargo']),
        ]
        verbose_name = "Empleado Hospital"
        verbose_name_plural = "Empleados Hospital"

    def __str__(self):
        return f"{self.apellido}, {self.nombre} (Legajo {self.legajo})"

    def clean(self):
        # Validación simple: DNI con al menos 7 dígitos (ignorando guiones/espacios)
        if self.dni:
            solo_digitos = ''.join(ch for ch in self.dni if ch.isdigit())
            if len(solo_digitos) < 7:
                raise ValidationError({'dni': 'El DNI debe tener al menos 7 dígitos.'})
