from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# Modelo para registrar datos básicos de un expediente (trámite/compra/origen)
class Expediente(models.Model):
    # Identificador único del expediente (texto)
    numero_expediente = models.CharField(max_length=50, unique=True)
    # Organismo desde el que proviene (opcional)
    organismo_origen = models.CharField(max_length=120, blank=True)
    # Número de compra o referencia de contratación (opcional)
    numero_compra = models.CharField(max_length=50, blank=True)
    
    proveedor = models.CharField(max_length=200, blank=True)
    
    class Meta:
        # Nombres legibles en el admin
        verbose_name = "Expediente"
        verbose_name_plural = "Expedientes"
        # Orden por número de expediente por defecto
        ordering = ['numero_expediente']

    def __str__(self):
        # Representación en texto: muestra el número del expediente
        return self.numero_expediente


# Modelo principal para representar un bien patrimonial del hospital
class BienPatrimonial(models.Model):
    # Estados posibles del bien para control de ciclo de vida
    ESTADO_CHOICES = (
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('MANTENIMIENTO', 'En mantenimiento'),
        ('BAJA', 'Dado de baja'),
    )

    # Tipos generales de bienes (clasificación contable/física)
    TIPO_CHOICES = (
        ('EQUIPO_MEDICO', 'Equipo Médico'),
        ('INFORMATICA', 'Equipo Informático'),
        ('MOBILIARIO', 'Mobiliario'),
        ('VEHICULO', 'Vehículo'),
        ('OTRO', 'Otro'),
    )

    # Origen del bien (cómo ingresó al patrimonio)
    ORIGEN_CHOICES = (
        ('DONACION', 'Donación'),
        ('OMISION', 'Omisión'),
        ('TRANSFERENCIA', 'Transferencia/Traslado'),
        ('COMPRA', 'Compra'),
    )

    # Identificador interno único del inventario (placa/etiqueta)
    numero_inventario = models.CharField(max_length=50, unique=True)
    # Nombre corto del bien
    nombre = models.CharField(max_length=200)
    # Descripción detallada
    descripcion = models.TextField()
    # Tipo/clasificación del bien (usa TIPO_CHOICES)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    # Marca y modelo (opcionales)
    marca = models.CharField(max_length=100, blank=True)
    modelo = models.CharField(max_length=100, blank=True)
    # Número de serie de fábrica (opcional)
    numero_serie = models.CharField(max_length=100, blank=True)

    # Datos de adquisición
    fecha_adquisicion = models.DateField()
    # Valor de compra/donación; no puede ser negativo
    valor_adquisicion = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    # Proveedor (si aplica)
    proveedor = models.CharField(max_length=200, blank=True)

    # Información contable y de origen
    cuenta_codigo = models.CharField(max_length=20, blank=True)
    # Origen del bien (por defecto: COMPRA)
    origen = models.CharField(max_length=15, choices=ORIGEN_CHOICES, default='COMPRA')
    # Donante (solo relevante si origen es DONACION)
    donante = models.CharField(max_length=200, blank=True)
    # Identificación adicional única (ej. código patrimonial externo)
    numero_identificacion = models.CharField(
        max_length=50,
        unique=True,
        null=True, blank=True,
        verbose_name="Número de Identificación"
    )

    # Ubicación física actual (servicio/dependencia) y responsable
    ubicacion_actual = models.CharField(max_length=200)
    responsable = models.CharField(max_length=200)
    # Estado actual del bien (usa ESTADO_CHOICES; por defecto ACTIVO)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='ACTIVO')

    # Relación opcional con un expediente; si se borra el expediente, queda en NULL
    expediente = models.ForeignKey(
        Expediente,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='bienes'  # permite expediente.bienes.all()
    )

    # Observaciones y mantenimiento preventivo/correctivo
    observaciones = models.TextField(blank=True)
    fecha_ultimo_mantenimiento = models.DateField(null=True, blank=True)
    proximo_mantenimiento = models.DateField(null=True, blank=True)

    # Metadatos de auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # se setea al crear
    fecha_actualizacion = models.DateTimeField(auto_now=True)  # se actualiza en cada save
    # Usuario que creó el registro; si se borra el usuario, queda en NULL
    usuario_creacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        # Nombres legibles y orden por número de inventario
        verbose_name = "Bien Patrimonial"
        verbose_name_plural = "Bienes Patrimoniales"
        ordering = ['numero_inventario']
        # Índices para acelerar búsquedas frecuentes
        indexes = [
            models.Index(fields=['numero_inventario']),
            models.Index(fields=['tipo']),
            models.Index(fields=['estado']),
        ]

    def clean(self):
        """
        Validaciones de negocio mínimas que se ejecutan antes de guardar (full_clean):
        - Si el origen es DONACION, el campo 'donante' es obligatorio.
        """
        if self.origen == 'DONACION' and not self.donante:
            # Se asocia el error al campo 'donante' para que el admin/form lo muestre ahí
            raise ValidationError({'donante': 'Debe especificar el donante cuando el origen es DONACIÓN.'})

    def __str__(self):
        # Representación en texto: "NroInventario - Nombre"
        return f"{self.numero_inventario} - {self.nombre}"

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
    usuario_creacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

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
