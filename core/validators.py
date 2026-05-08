import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class ComplexPasswordValidator:
    """Valida que la contraseña tenga requisitos de seguridad mínimos."""

    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _('La contraseña debe incluir al menos una letra mayúscula.'),
                code='password_no_upper',
            )
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _('La contraseña debe incluir al menos una letra minúscula.'),
                code='password_no_lower',
            )
        if not re.search(r'\d', password):
            raise ValidationError(
                _('La contraseña debe incluir al menos un número.'),
                code='password_no_number',
            )
        if not re.search(r'[^A-Za-z0-9]', password):
            raise ValidationError(
                _('La contraseña debe incluir al menos un carácter especial.'),
                code='password_no_special',
            )

    def get_help_text(self):
        return _(
            'Tu contraseña debe tener al menos 8 caracteres e incluir una letra mayúscula, '
            'una letra minúscula, un número y un carácter especial (Ej: Lm9!abcd).'
        )
