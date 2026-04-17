from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    TIPO_USUARIO = [
        ('admin', 'Administrador'),
        ('supervisor', 'Supervisor'),        
        ('empleado', 'Empleado Hospital'),
    ]
    tipo_usuario = models.CharField(
        max_length=10,
        choices=TIPO_USUARIO,
        default='empleado'
    )

    numero_doc = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        verbose_name='Número de Documento'
    )

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='grupos',
        blank=True,
        help_text='Los grupos a los que pertenece este usuario.',
        related_name='usuarios_custom',
        related_query_name='usuario_custom',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='permisos de usuario',
        blank=True,
        help_text='Permisos específicos para este usuario.',
        related_name='usuarios_custom',
        related_query_name='usuario_custom',
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self) -> str:
        tipo_display = dict(self.TIPO_USUARIO).get(self.tipo_usuario, self.tipo_usuario)
        return f"{self.username} ({tipo_display})"

    # ── helpers de rol ──────────────────────────────────────────
    @property
    def es_admin(self) -> bool:
        return self.is_superuser or self.tipo_usuario == 'admin'

    @property
    def es_supervisor(self) -> bool:
        return self.tipo_usuario == 'supervisor'

    @property
    def es_empleado(self) -> bool:
        return self.tipo_usuario == 'empleado'