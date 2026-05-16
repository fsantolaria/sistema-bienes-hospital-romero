# core/forms.py
import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from core.models import BienPatrimonial
from core.models.expediente import Expediente
from datetime import date


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'class': 'form-control', 'accept': '.xlsx,.xls,.xlsm,.xlsb,.ods'}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return single_file_clean(data, initial)


# ========== FORMULARIO DE CARGA MASIVA ==========
class CargaMasivaForm(forms.Form):
    archivo_excel = MultipleFileField(
        label='Seleccionar archivo(s) Excel',
        help_text='Formatos soportados: .xlsx, .xls, .xlsm, .xlsb, .ods'
    )
    servicio = forms.CharField(
        max_length=100,
        required=False,
        label='Servicio por defecto (opcional)',
        help_text='Si se deja vacío, se tomará el servicio de cada fila del archivo.',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


# ========== FORMULARIO DE BIENES PATRIMONIALES ==========
class BienPatrimonialForm(forms.ModelForm):
    numero_expediente = forms.CharField(label="N° de Expediente", max_length=50, required=False)
    numero_compra     = forms.CharField(label="N° de Compra",     max_length=50, required=False)

    class Meta:
        model = BienPatrimonial
        fields = [
            'descripcion', 'cantidad', 'expediente', 'cuenta_codigo', 'nomenclatura_bienes',
            'numero_serie', 'numero_identificacion', 'origen', 'estado', 'servicios',
            'observaciones', 'valor_adquisicion', 'fecha_adquisicion', 'fecha_baja', 'siem',
        ]
        error_messages = {
            'descripcion': {'required': 'Este campo es obligatorio.'},
            'cantidad':    {'required': 'Este campo es obligatorio.'},
            'origen':      {'required': 'Este campo es obligatorio.'},
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'expediente': forms.Select(attrs={'class': 'form-select'}),
            'cuenta_codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nomenclatura_bienes': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_identificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'origen': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'servicios': forms.Select(attrs={'class': 'form-select flex-grow-1'}),
            'observaciones': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'valor_adquisicion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0}),
            'fecha_adquisicion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_baja': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'siem': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["numero_expediente"].widget.attrs.setdefault("class", "form-control")
        self.fields["numero_compra"].widget.attrs.setdefault("class", "form-control")
        self.fields["numero_expediente"].widget.attrs.setdefault("placeholder", "Ej: EX-123/2025")
        self.fields["numero_compra"].widget.attrs.setdefault("placeholder", "Ej: OC-45/2025")

        exp = getattr(self.instance, "expediente", None)
        if exp:
            self.fields["numero_expediente"].initial = exp.numero_expediente
            self.fields["numero_compra"].initial = exp.numero_compra

        # ===== SERVICIOS: fijos + extras, ordenados alfabéticamente =====
        from core.models.servicio_extra import ServicioExtra

        SERVICIOS_FIJOS = [
            'Apoyo A La Comunidad',
            'Area Guardia',
            'Area Limpieza Hospitalaria',
            'Area Parque Cultural',
            'Arquitectura',
            'CAPER',
            'Camilleros',
            'Cardiologia',
            'Charcot',
            'Cirugia',
            'Clinica',
            'Cocina',
            'Compras',
            'Conmutador',
            'Consejeria',
            'Consultorio De Gastroenterologia',
            'Consultorio Externo Salud Mental',
            'Consultorios Externos Pab V',
            'Contable',
            'Costurero',
            'Cud Y Servicios De Consumos Problematicos',
            'Departamento De Enfermerias Supervision',
            'Departamento Sistema De Informacion - Samo Turnos Y Estadistica',
            'Deposito Descartable',
            'Deposito General',
            'Dermatologia',
            'Diagnostico Por Imagenes',
            'Dira',
            'Direccion Administrativa',
            'Direccion Asociada Area Tecnica',
            'Direccion Asociada Medico Quirurgica',
            'Direccion Ejecutiva',
            'Direccion Salud Mental',
            'Dispositivo Artistico Cultural',
            'Docencia E Investigacion',
            'Donacion Fundacion Florencio Perez',
            'Emergencia',
            'En Guarda Patrimoniales',
            'Enfermeria',
            'Epidemiologia',
            'Estadistica',
            'Estadistica Central',
            'Estadistica Pabellon V',
            'Esterilizacion',
            'Farmacia',
            'Gastroenterologia',
            'Gerenciamiento De Camas',
            'Hemoterapia',
            'Infancias Y Juventudes',
            'Infectologia',
            'Informatica',
            'Infraestructura Y Mantenimiento',
            'Intendencia',
            'Jardin Maternal',
            'Laboratorio',
            'Lasegue',
            'Legales',
            'Limpieza',
            'Mesa De Entrada',
            'Neumonologia Y Oftalmologia',
            'Neurocirugia',
            'Neuropsicologia',
            'Odontologia',
            'Oncologia',
            'Patologia',
            'Patrimoniales',
            'Pediatria Y Neonatologia',
            'Penfield',
            'Percial',
            'Podologia Y Peluqueria',
            'Polo Educativo',
            'Pre Alta',
            'Quirofano',
            'RRHH',
            'Recuperacion Clinica',
            'Registro Civil',
            'Rehabilitacion Fisica Y Kinesiologia',
            'Rehabilitacion Salud Mental Direccion',
            'Reumatologia Y Oftalmologia',
            'SAC',
            'SAM',
            'SAMO Contable',
            'SAMO Facturacion',
            'SAP (Servicio De Area Programatica Y Redes De Salud)',
            'SGU',
            'Sala De Endoscopia',
            'Sala F',
            'Sala G',
            'Seguridad E Higiene',
            'Servicio De Psicologia',
            'Servicio Rehabilitacion Larga Distancia',
            'Servicio Social',
            'Sumar',
            'Tocoginecologia',
            'Toxicologia',
            'Traumatologia',
            'U.T.I.',
            'UCAC',
            'Vacunacion',
            'Vigilancia',
        ]

        extras = [s.nombre for s in ServicioExtra.objects.all()]
        todos = sorted(set(SERVICIOS_FIJOS + extras))
        choices = [('', '— Seleccionar servicio —')] + [(s, s) for s in todos]
        self.fields["servicios"].widget.choices = choices

        origen_choices = [('', '— Seleccionar origen —')] + list(self.fields["origen"].choices)
        self.fields["origen"].choices = origen_choices
        self.fields["origen"].required = False  # manejado por clean_origen
        self.fields["origen"].initial = ''       # no pre-seleccionar el default del modelo

    def clean_origen(self):
        value = self.cleaned_data.get("origen")
        if not value:
            raise forms.ValidationError("Este campo es obligatorio.")
        return value

    def clean_servicios(self):
        value = self.cleaned_data.get("servicios")
        if not value:
            raise forms.ValidationError("Este campo es obligatorio.")
        return value
    
    def clean(self):
        cleaned = super().clean()

        n_exp = (cleaned.get("numero_expediente") or "").strip()
        n_cmp = (cleaned.get("numero_compra") or "").strip()

        if n_cmp and not n_exp:
            self.add_error("numero_expediente", "Si informás N° de compra, debés indicar el N° de Expediente.")


        # Precio: si el origen no es COMPRA, ignorar precio
        if cleaned.get("origen") and cleaned["origen"] != "COMPRA":
            cleaned["valor_adquisicion"] = None

        estado = cleaned.get("estado")
        fecha_baja = cleaned.get("fecha_baja")

        if estado == "BAJA":
            if not fecha_baja:
                cleaned["fecha_baja"] = date.today()
        else:
            cleaned["fecha_baja"] = None

        return cleaned

    def save(self, commit=True):
        bien = super().save(commit=False)

        n_exp = (self.cleaned_data.get("numero_expediente") or "").strip()
        n_cmp = (self.cleaned_data.get("numero_compra") or "").strip()

        expediente = None
        if n_exp:
            expediente, _ = Expediente.objects.get_or_create(numero_expediente=n_exp)
            if n_cmp and expediente.numero_compra != n_cmp:
                expediente.numero_compra = n_cmp
                expediente.save()
        else:
            expediente = self.cleaned_data.get("expediente")

        bien.expediente = expediente

        if commit:
            bien.save()
            self.save_m2m()
        return bien


# ========== FORMULARIO OPERADOR ==========
class OperadorForm(forms.Form):
    nombre = forms.CharField(max_length=200, required=True, label='Nombre')
    apellido = forms.CharField(max_length=200, required=True, label='Apellido')
    pais = forms.CharField(max_length=100, required=False, label='País')
    dni = forms.CharField(
        max_length=8,
        required=True,
        label='DNI',
        validators=[
            RegexValidator(r'^\d{1,8}$', 'El DNI debe tener sólo números y hasta 8 dígitos.')
        ]
    )
    email = forms.EmailField(required=False, label='Email')
    tipo_usuario = forms.ChoiceField(
        choices=[('operador', 'Operador'), ('supervisor', 'Supervisor')],
        initial='operador',
        label='Tipo de Usuario'
    )
    estado = forms.ChoiceField(
        choices=[('habilitado', 'Habilitado'), ('no-habilitado', 'No Habilitado')],
        initial='habilitado',
        label='Estado'
    )
    password = forms.CharField(required=False, widget=forms.PasswordInput, label='Contraseña')

    def __init__(self, *args, operador_pk=None, **kwargs):
        self.operador_pk = operador_pk
        super().__init__(*args, **kwargs)
        if self.operador_pk:
            self.fields['dni'].required = False

    def clean_dni(self):
        dni = (self.cleaned_data.get('dni') or '').strip()
        if not dni:
            return dni

        if not dni.isdigit() or not (1 <= len(dni) <= 8):
            raise ValidationError('El DNI debe tener hasta 8 números.')

        Operador = get_user_model()
        operadores = Operador.objects.filter(numero_doc__iexact=dni)
        if self.operador_pk:
            operadores = operadores.exclude(pk=self.operador_pk)
        if operadores.exists():
            raise ValidationError('Ya existe un operador con ese DNI')
        return dni

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip()
        if not email:
            return email
        Operador = get_user_model()
        operadores = Operador.objects.filter(email__iexact=email)
        if self.operador_pk:
            operadores = operadores.exclude(pk=self.operador_pk)
        if operadores.exists():
            raise ValidationError('Ya existe un operador con ese email')
        return email

    def clean_password(self):
        password = (self.cleaned_data.get('password') or '').strip()
        if not password:
            return password

        if len(password) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
        if not re.search(r'[A-Z]', password):
            raise ValidationError('La contraseña debe incluir al menos una letra mayúscula.')
        if not re.search(r'[a-z]', password):
            raise ValidationError('La contraseña debe incluir al menos una letra minúscula.')
        if not re.search(r'\d', password):
            raise ValidationError('La contraseña debe incluir al menos un número.')
        if not re.search(r'[^A-Za-z0-9]', password):
            raise ValidationError('La contraseña debe incluir al menos un carácter especial.')

        from django.contrib.auth.password_validation import validate_password
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError(e.messages)

        return password
