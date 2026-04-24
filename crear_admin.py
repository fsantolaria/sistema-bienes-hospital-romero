import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_bienes.settings.development')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Crear admin si no existe
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@hospital.com',
        password='admin123',
        tipo_usuario='admin'
    )
    print("¡Usuario administrador creado exitosamente! Usuario: admin / Contraseña: admin123")
else:
    user = User.objects.get(username='admin')
    user.tipo_usuario = 'admin'
    user.set_password('admin123')
    user.save()
    print("El usuario administrador ya existía. Se actualizó su tipo y contraseña.")
