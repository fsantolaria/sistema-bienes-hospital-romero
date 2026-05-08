import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_bienes.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()
DEFAULT_PASSWORD = 'Operador123!'
validate_password(DEFAULT_PASSWORD)

# Crear operador si no existe
if not User.objects.filter(username='operador').exists():
    User.objects.create_user(
        username='operador',
        email='operador@hospital.com',
        password=DEFAULT_PASSWORD,
        tipo_usuario='operador'
    )
    print(f"¡Usuario operador creado exitosamente! Usuario: operador / Contraseña: {DEFAULT_PASSWORD}")
else:
    user = User.objects.get(username='operador')
    user.tipo_usuario = 'operador'
    user.set_password(DEFAULT_PASSWORD)
    user.save()
    print(f"El usuario operador ya existía. Se actualizó su tipo y contraseña a: {DEFAULT_PASSWORD}")
