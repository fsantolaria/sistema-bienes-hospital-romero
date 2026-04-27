from django.contrib import admin
from django.apps import apps
from sistema_bienes.admin import custom_admin_site  # tu admin personalizado
from .models.expediente import Expediente
from .models.bien_patrimonial import BienPatrimonial
from .models.notificacion import Notificacion
from .models.servicio_extra import ServicioExtra


# ===== Helpers seguros =====
def model_has_field(model, field_name: str) -> bool:
    return any(f.name == field_name for f in model._meta.get_fields())

def first_present(model, candidates):
    """Devuelve el primer nombre de campo que exista en el modelo."""
    for c in candidates:
        if model_has_field(model, c):
            return c
    return None


# ===== Expediente Admin =====
@admin.register(Expediente, site=custom_admin_site)
class ExpedienteAdmin(admin.ModelAdmin):
    list_display = [f for f in [
        'numero_expediente',
        'organismo_origen',
        'numero_compra',
        'proveedor',
    ] if model_has_field(Expediente, f)]
    search_fields = [f for f in [
        'numero_expediente',
        'organismo_origen',
        'numero_compra',
        'proveedor',
    ] if model_has_field(Expediente, f)]
    ordering = [f for f in ['numero_expediente'] if model_has_field(Expediente, f)]


# ===== Inline de Bienes dentro de Expediente =====
class BienInline(admin.TabularInline):
    """Inline de bienes (solo lectura) en el admin de Expediente."""
    model = BienPatrimonial
    extra = 0
    can_delete = False

    # Elegimos campos existentes y útiles
    _nombre_field = first_present(BienPatrimonial, ['nombre', 'descripcion'])
    fields = [f for f in [
        'clave_unica',
        _nombre_field,
        'estado',
        'servicios',
        'origen',
        'expediente',
    ] if f and model_has_field(BienPatrimonial, f)]

    readonly_fields = fields

# Activar inline si lo querés ver dentro de Expediente
ExpedienteAdmin.inlines = [BienInline]


# ===== Bien Patrimonial Admin =====
@admin.register(BienPatrimonial, site=custom_admin_site)
class BienPatrimonialAdmin(admin.ModelAdmin):
    # list_display dinámico según campos existentes
    list_display = [f for f in [
        'clave_unica',
        first_present(BienPatrimonial, ['nombre', 'descripcion']),
        'cantidad',
        'servicios',
        'estado',
        'expediente',
        'origen',
        'valor_adquisicion',
        'fecha_adquisicion',
        # campos de BAJA si existen
        'fecha_baja',
        'expediente_baja',
    ] if f and model_has_field(BienPatrimonial, f)]

    list_filter = [f for f in [
        'estado',
        'origen',
        'expediente',
        'fecha_adquisicion',
        'fecha_baja',           # solo si existe
    ] if model_has_field(BienPatrimonial, f)]

    search_fields = [f for f in [
        first_present(BienPatrimonial, ['nombre', 'descripcion']),
        'numero_identificacion',
        'numero_serie',
        'cuenta_codigo',
        'nomenclatura_bienes',
        'servicios',
        'expediente__numero_expediente',
        # búsqueda por campos de baja si existen
        'expediente_baja',
        'descripcion_baja',
    ] if f and (
        '__' in f or model_has_field(BienPatrimonial, f)  # permitir fk lookups
    )]

    date_hierarchy = 'fecha_adquisicion' if model_has_field(BienPatrimonial, 'fecha_adquisicion') else None
    list_per_page = 25
    ordering = tuple([f for f in ['clave_unica'] if model_has_field(BienPatrimonial, f)])
    autocomplete_fields = [f for f in ['expediente'] if model_has_field(BienPatrimonial, f)]
    readonly_fields = [f for f in ['clave_unica'] if model_has_field(BienPatrimonial, f)]

    # Campos del formulario (ordenado y seguro)
    _nombre_field = first_present(BienPatrimonial, ['nombre', 'descripcion'])
    base_fields = [
        'clave_unica',
        _nombre_field,
        'descripcion' if _nombre_field != 'descripcion' and model_has_field(BienPatrimonial, 'descripcion') else None,
        'cantidad',
        'expediente',
        'cuenta_codigo',
        'nomenclatura_bienes',
        'fecha_adquisicion',
        'origen',
        'estado',
        'numero_serie',
        'valor_adquisicion',
        'numero_identificacion',
        'servicios',
    ]
    baja_fields = [
        'fecha_baja' if model_has_field(BienPatrimonial, 'fecha_baja') else None,
        'expediente_baja' if model_has_field(BienPatrimonial, 'expediente_baja') else None,
        'descripcion_baja' if model_has_field(BienPatrimonial, 'descripcion_baja') else None,
    ]
    fields = tuple([f for f in (base_fields + baja_fields) if f])

    def save_model(self, request, obj, form, change):
        # Mantiene tu validación del modelo
        obj.full_clean()
        super().save_model(request, obj, form, change)


# ===== Servicio Extra Admin =====
@admin.register(ServicioExtra, site=custom_admin_site)
class ServicioExtraAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']
    ordering = ['nombre']



# ===== Notificacion Admin =====
admin.site.register(Notificacion)
