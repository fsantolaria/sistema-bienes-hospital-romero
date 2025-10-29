"""Constantes compartidas del módulo `core`.

Incluye opciones y valores por defecto usados por los modelos y tests.
"""

# Origenes posibles
ORIGEN_COMPRA = 'COMPRA'
ORIGEN_DONACION = 'DONACION'
ORIGEN_TRANSFERENCIA = 'TRANSFERENCIA'
ORIGEN_OMISION = 'OMISION'

ORIGEN_CHOICES = [
    (ORIGEN_COMPRA, 'Compra'),
    (ORIGEN_DONACION, 'Donación'),
    (ORIGEN_TRANSFERENCIA, 'Transferencia'),
    (ORIGEN_OMISION, 'Omisión'),
]

# Estados posibles
ESTADO_ACTIVO = 'ACTIVO'
ESTADO_BAJA = 'BAJA'
ESTADO_MANTENIMIENTO = 'MANTENIMIENTO'
ESTADO_INACTIVO = 'INACTIVO'

ESTADO_CHOICES = [
    (ESTADO_ACTIVO, 'Activo'),
    (ESTADO_MANTENIMIENTO, 'Mantenimiento'),
    (ESTADO_INACTIVO, 'Inactivo'),
    (ESTADO_BAJA, 'Baja'),
]
