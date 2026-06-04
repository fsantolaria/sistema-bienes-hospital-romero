import os
import sys

# Establecer settings de producción ANTES de que Django se inicialice
os.environ['DJANGO_SETTINGS_MODULE'] = 'sistema_bienes.settings.production'

# Agregar el directorio raíz al path para que Django encuentre el proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sistema_bienes.wsgi import application

app = application
