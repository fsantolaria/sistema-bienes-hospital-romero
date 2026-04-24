import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_bienes.settings.development')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Crear operador si no existe
if not User.objects.filter(username='operador').exists():
    User.objects.create_user(
        username='operador',
        email='operador@hospital.com',
        password='operador123',
        tipo_usuario='operador'
    )
    print("¡Usuario operador creado exitosamente! Usuario: operador / Contraseña: operador123")
else:
    user = User.objects.get(username='operador')
    user.tipo_usuario = 'operador'
    user.set_password('operador123')
    user.save()
    print("El usuario operador ya existía. Se actualizó su tipo y contraseña.")
