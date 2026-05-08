import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_bienes.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()
DEFAULT_PASSWORD = 'Admin123!'
validate_password(DEFAULT_PASSWORD)

# Crear admin si no existe
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@hospital.com',
        password=DEFAULT_PASSWORD,
        tipo_usuario='admin'
    )
    print(f"¡Usuario administrador creado exitosamente! Usuario: admin / Contraseña: {DEFAULT_PASSWORD}")
else:
    user = User.objects.get(username='admin')
    user.tipo_usuario = 'admin'
    user.set_password(DEFAULT_PASSWORD)
    user.save()
    print(f"El usuario administrador ya existía. Se actualizó su tipo y contraseña a: {DEFAULT_PASSWORD}")
