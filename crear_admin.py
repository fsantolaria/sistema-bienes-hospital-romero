import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_bienes.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Crear superusuario si no existe
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@hospital.com', 'admin123')
    print("¡Usuario administrador creado exitosamente! Usuario: admin / Contraseña: admin123")
else:
    print("El usuario administrador ya existe.")
