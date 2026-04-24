import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_bienes.settings.development')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Crear supervisor si no existe
if not User.objects.filter(username='supervisor').exists():
    User.objects.create_user(
        username='supervisor',
        email='supervisor@hospital.com',
        password='supervisor123',
        tipo_usuario='supervisor'
    )
    print("¡Usuario supervisor creado exitosamente! Usuario: supervisor / Contraseña: supervisor123")
else:
    user = User.objects.get(username='supervisor')
    user.tipo_usuario = 'supervisor'
    user.set_password('supervisor123')
    user.save()
    print("El usuario supervisor ya existía. Se actualizó su tipo y contraseña.")
