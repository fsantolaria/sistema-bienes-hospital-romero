validators.py

import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ComplexPasswordValidator:
    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos 1 letra mayúscula."),
                code='password_no_upper',
            )
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos 1 letra minúscula."),
                code='password_no_lower',
            )
        if not re.search(r'[0-9]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos 1 número."),
                code='password_no_number',
            )
        if not re.search(r'[!@#$%^&*(),.?":{}|<>+=\-_]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos 1 carácter especial."),
                code='password_no_special',
            )

    def get_help_text(self):
        return _(
            "Tu contraseña debe contener al menos 1 mayúscula, 1 minúscula, 1 número y 1 carácter especial."
        )