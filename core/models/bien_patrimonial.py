# core/models/bien_patrimonial.py
from datetime import date
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from ..constants import (
    ESTADO_CHOICES,
    ORIGEN_CHOICES,
    ORIGEN_COMPRA,
    ESTADO_ACTIVO,
)


class BienPatrimonial(models.Model):
    """
    Modelo de Bien Patrimonial.
    Incluye campos de baja (fecha_baja, expediente_baja, descripcion_baja) y observaciones.
    Deja fecha_adquisicion como nullable para destrabar migración; luego podés volverla obligatoria.
    """

    # Identificador lógico de la app (clave visible para el usuario)
    clave_unica = models.BigAutoField(primary_key=True, verbose_name="Clave Única")

    # Datos principales
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción")
    cantidad = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Cantidad",
    )

    # Relación con Expediente
    expediente = models.ForeignKey(
        "Expediente",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bienes",
        verbose_name="N° de Expediente",
    )

    cuenta_codigo = models.CharField(
        max_length=20, blank=True, verbose_name="Cuenta Código"
    )
    nomenclatura_bienes = models.CharField(
        max_length=200, blank=True, verbose_name="Nomenclatura de Bienes"
    )

    # Fecha de alta (por ahora nullable para destrabar migraciones)
    fecha_adquisicion = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de Alta",
    )

    # Origen/Estado
    origen = models.CharField(
        max_length=15,
        choices=ORIGEN_CHOICES,
        default=ORIGEN_COMPRA,
        verbose_name="Origen",
    )
    estado = models.CharField(
        max_length=50,
        choices=ESTADO_CHOICES,
        default=ESTADO_ACTIVO,
        verbose_name="Estado",
    )

    # Identificaciones
    numero_serie = models.CharField(max_length=100, blank=True, verbose_name="N° de serie")
    numero_identificacion = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Número de ID",
    )
    numero_compra = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="N° de Compra",
    )

    # Monto (solo si origen = COMPRA, lo validamos en clean)
    valor_adquisicion = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        verbose_name="Precio",
    )

    # Datos complementarios
    servicios = models.CharField(max_length=200, blank=True, verbose_name="Servicios")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    # Fecha SIEM (campo nuevo para almacenar fechas SIEM)
    siem = models.DateField(null=True, blank=True, verbose_name="SIEM")

    # --- Campos de BAJA ---
    fecha_baja = models.DateField(
        null=True, blank=True, verbose_name="Fecha de Baja"
    )
    expediente_baja = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Expediente Baja"
    )
    descripcion_baja = models.TextField(
        blank=True, verbose_name="Descripción de baja"
    )

    class Meta:
        verbose_name = "Bien Patrimonial"
        verbose_name_plural = "Bienes Patrimoniales"
        ordering = ["clave_unica"]
        indexes = [
            models.Index(fields=["clave_unica"]),
            models.Index(fields=["estado"]),
        ]

    # -----------------------
    # Validaciones de modelo
    # -----------------------
    def clean(self):
        super().clean()

        # Precio no negativo
        if self.valor_adquisicion is not None and self.valor_adquisicion < 0:
            raise ValidationError(
                {"valor_adquisicion": "El precio no puede ser negativo"}
            )

        # Fecha de alta no futura (si está informada)
        if self.fecha_adquisicion and self.fecha_adquisicion > date.today():
            raise ValidationError(
                {"fecha_adquisicion": "La fecha no puede ser futura"}
            )

        # Si el origen no es COMPRA, no guardamos precio
        if self.origen != ORIGEN_COMPRA:
            self.valor_adquisicion = None

        # Si tiene fecha_baja, el estado debería ser BAJA (no obligatorio, pero consistente)
        # Podés dejar esto como warning en vez de forzar:
        # if self.fecha_baja and self.estado != "BAJA":
        #     raise ValidationError({"estado": "El estado debe ser BAJA si hay fecha de baja."})

    def __str__(self):
        return f"{self.clave_unica} — {self.nombre}"
