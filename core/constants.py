"""Constantes compartidas del módulo `core`.

Incluye opciones y valores por defecto usados por los modelos y tests.
"""

# Origenes posibles
ORIGEN_COMPRA = 'COMPRA'
ORIGEN_COMPRA_MENOR = 'COMPRA_MENOR'
ORIGEN_DONACION = 'DONACION'
ORIGEN_TRANSFERENCIA = 'TRANSFERENCIA'
ORIGEN_OMISION = 'OMISION'

ORIGEN_CHOICES = (
    (ORIGEN_COMPRA, 'Compra'),
    (ORIGEN_COMPRA_MENOR, 'Compra Menor'),
    (ORIGEN_DONACION, 'Donación'),
    (ORIGEN_TRANSFERENCIA, 'Transferencia'),
    (ORIGEN_OMISION, 'Omisión'),
)

ORIGENES_COMPRA = {ORIGEN_COMPRA, ORIGEN_COMPRA_MENOR}

# Estados posibles
ESTADO_ACTIVO = 'ACTIVO'
ESTADO_BAJA = 'BAJA'
ESTADO_MANTENIMIENTO = 'MANTENIMIENTO'
ESTADO_INACTIVO = 'INACTIVO'

ESTADO_CHOICES = (
    (ESTADO_ACTIVO, 'Activo'),
    (ESTADO_MANTENIMIENTO, 'Mantenimiento'),
    (ESTADO_INACTIVO, 'Inactivo'),
    (ESTADO_BAJA, 'Baja'),
)

# Máximo de notificaciones por usuario (se conservan las N más recientes)
MAX_NOTIFICACIONES = 10
