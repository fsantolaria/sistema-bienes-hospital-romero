# 🏥 Sistema de Gestión de Bienes Patrimoniales - Hospital Melchor Romero

## 📋 Descripción
Sistema web desarrollado en Django para la gestión y control de bienes patrimoniales del Hospital Melchor Romero.

## 🚀 Características
- Registro y catalogación de bienes patrimoniales
- Control de inventario en tiempo real
- Gestión de mantenimientos y estados
- Informes y reportes personalizados
- Múltiples ambientes (Desarrollo, Producción)

## 👥 Equipo de Desarrollo
- **Docentes**: Karina Alvarez, Alejandra , Felipe Morales, Fernando Diego Santolaria
- **Estudiantes**: ISFDyT 210

## 🛠️ Tecnologías
- Django 4.2.7
- SQLite (Desarrollo, Testing, Produccion)
- Bootstrap 5
- JavaScript ES6+

## 📦 Instalación

### 1. Clonar repositorio
```bash
git clone https://github.com/fsantolaria/sistema-bienes-hospital-romero.git
cd sistema-bienes-hospital-romero

# 🖥️ INSTRUCTIVOS COMPLETOS - Sistema de Gestión de Bienes Patrimoniales

## 📋 INSTRUCTIVO 1: CONFIGURACIÓN INICIAL PARA WINDOWS 10

### Para todos los equipos (BACK, FRONT, TESTING)

#### 🚀 Paso 1: Prerrequisitos
```powershell
# 1. Instalar Python 3.10+ desde python.org
# 2. Instalar Git desde git-scm.com
# 3. Verificar instalaciones:
python --version
git --version
```

#### 🚀 Paso 2: Clonar y configurar proyecto
```powershell
# 1. Abrir PowerShell como administrador
# 2. Navegar al directorio deseado
cd C:\Users\TuUsuario\Documents

# 3. Clonar repositorio
git clone https://github.com/fsantolaria/sistema-bienes-hospital-romero.git
cd sistema-bienes-hospital-romero

# 4. Configurar rama según rol
# Para BACK y FRONT:
git checkout development
# Para TESTING:
git checkout testing

# 5. Actualizar repo
git pull origin development  # o testing según corresponda
```

#### 🚀 Paso 3: Entorno virtual y dependencias
```powershell
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno
.\venv\Scripts\activate

# 3. Instalar dependencias según rol
# Para BACK:
pip install -r requirements\base.txt
pip install -r requirements\development.txt

# Para FRONT:
pip install -r requirements\base.txt
pip install -r requirements\development.txt

# Para TESTING:
pip install -r requirements\base.txt
pip install -r requirements\development.txt
```

#### 🚀 Paso 4: Configurar variables de entorno
```powershell
# 1. Copiar archivo de entorno según rol
# Para BACK y FRONT:
copy enviroment\env_development .env
# Para TESTING:
copy enviroment\env_testing .env

# 2. Verificar que el archivo .env existe
dir .env
```

#### 🚀 Paso 5: Base de datos y migraciones
```powershell
#  Antes de aplicar migraciones
python manage.py makemigrations core

#  Aplicar migraciones
python manage.py migrate

#  Crear superusuario
python manage.py createsuperuser
# Seguir prompts: usuario, email, password

#  Verificar que la BD se creó
dir *.sqlite3
```

#### 🚀 Paso 6: Ejecutar servidor
```powershell
# 1. Ejecutar servidor de desarrollo
python manage.py runserver

# 2. Abrir navegador en: http://127.0.0.1:8000/
# 3. Admin: http://127.0.0.1:8000/admin/
```

---

## 🐧 INSTRUCTIVO 2: CONFIGURACIÓN PARA LINUX (Ubuntu/Debian)

### Para todos los equipos

#### 🚀 Paso 1: Prerrequisitos
```bash
# 1. Actualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar Python y herramientas
sudo apt install python3 python3-pip python3-venv git -y

# 3. Verificar instalaciones
python3 --version
pip3 --version
git --version
```

#### 🚀 Paso 2: Clonar y configurar proyecto
```bash
# 1. Navegar al directorio deseado
cd ~/Documents

# 2. Clonar repositorio
git clone https://github.com/fsantolaria/sistema-bienes-hospital-romero.git
cd sistema-bienes-hospital-romero

# 3. Configurar rama según rol
# Para BACK y FRONT:
git checkout development
# Para TESTING:
git checkout testing

# 4. Actualizar repo
git pull origin development  # o testing según corresponda
```

#### 🚀 Paso 3: Entorno virtual y dependencias
```bash
# 1. Crear entorno virtual
python3 -m venv venv

# 2. Activar entorno
source venv/bin/activate

# 3. Instalar dependencias según rol
# Para BACK y FRONT:
pip install -r requirements/base.txt
pip install -r requirements/development.txt

# Para TESTING:
pip install -r requirements/base.txt
pip install -r requirements/development.txt
```

#### 🚀 Paso 4: Configurar variables de entorno
```bash
# 1. Copiar archivo de entorno según rol
# Para BACK y FRONT:
cp enviroment/env_development .env
# Para TESTING:
cp enviroment/env_testing .env
# 2. Verificar que el archivo .env existe
ls -la .env
```

#### 🚀 Paso 5: Base de datos y migraciones
```bash
# 1. Aplicar migraciones
python manage.py migrate

# 2. Crear superusuario
python manage.py createsuperuser
# Seguir prompts: usuario, email, password

# 3. Verificar que la BD se creó
ls -la *.sqlite3
```

#### 🚀 Paso 6: Ejecutar servidor
```bash
# 1. Ejecutar servidor de desarrollo
python manage.py runserver

# 2. Abrir navegador en: http://127.0.0.1:8000/
# 3. Admin: http://127.0.0.1:8000/admin/
```

---

## 🍎 INSTRUCTIVO 3: CONFIGURACIÓN PARA macOS

### Para todos los equipos

#### 🚀 Paso 1: Prerrequisitos
```bash
# 1. Instalar Homebrew (si no está instalado)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Instalar Python y Git
brew install python git

# 3. Verificar instalaciones
python3 --version
pip3 --version
git --version
```

#### 🚀 Paso 2: Clonar y configurar proyecto
```bash
# 1. Navegar al directorio deseado
cd ~/Documents

# 2. Clonar repositorio
git clone https://github.com/fsantolaria/sistema-bienes-hospital-romero.git
cd sistema-bienes-hospital-romero

# 3. Configurar rama según rol
# Para BACK y FRONT:
git checkout development
# Para TESTING:
git checkout testing

# 4. Actualizar repo
git pull origin development  # o testing según corresponda
```

#### 🚀 Paso 3: Entorno virtual y dependencias
```bash
# 1. Crear entorno virtual
python3 -m venv venv

# 2. Activar entorno
source venv/bin/activate

# 3. Instalar dependencias según rol
# Para BACK y FRONT:
pip install -r requirements/base.txt
pip install -r requirements/development.txt

# Para TESTING:
pip install -r requirements/base.txt
pip install -r requirements/development.txt
```

#### 🚀 Paso 4: Configurar variables de entorno
```bash
# 1. Copiar archivo de entorno según rol
# Para BACK y FRONT:
cp enviroment\env_development .env
# Para TESTING:
cp enviroment\env_testing .env

# 2. Verificar que el archivo .env existe
ls -la .env
```

#### 🚀 Paso 5: Base de datos y migraciones
```bash
# 1. Aplicar migraciones
python manage.py migrate

# 2. Crear superusuario
python manage.py createsuperuser
# Seguir prompts: usuario, email, password

# 3. Verificar que la BD se creó
ls -la *.sqlite3
```

#### 🚀 Paso 6: Ejecutar servidor
```bash
# 1. Ejecutar servidor de desarrollo
python manage.py runserver

# 2. Abrir navegador en: http://127.0.0.1:8000/
# 3. Admin: http://127.0.0.1:8000/admin/
```

---

## 🎯 INSTRUCTIVO ESPECÍFICO POR ROL

### 👨‍💻 Para el equipo BACKEND (Windows 10)
```powershell
# 1. Seguir instructivo general Windows
# 2. Crear rama para feature backend
git checkout -b backend/nueva-feature

# 3. Trabajar en modelos/APIs
python manage.py startapp inventario  # si se necesita nueva app

# 4. Crear migraciones
python manage.py makemigrations

# 5. Probar migraciones
python manage.py migrate --fake-initial

# 6. Ejecutar tests específicos
python manage.py test inventario.tests

# 7. Cuando terminen, hacer commit y push
git add .
git commit -m "feat(backend): agregar modelo de categorías"
git push origin backend/nueva-feature
```

### 🎨 Para el equipo FRONTEND (Windows 10)
```powershell
# 1. Seguir instructivo general Windows
# 2. Crear rama para feature frontend
git checkout -b frontend/nuevo-diseno

# 3. Trabajar en templates y estáticos
# Editar archivos en core/templates/ y core/static/

# 4. Verificar cambios en navegador
python manage.py runserver

# 5. Colectar estáticos (si es necesario)
python manage.py collectstatic --noinput

# 6. Cuando terminen, hacer commit y push
git add .
git commit -m "feat(frontend): diseñar interfaz de inventario"
git push origin frontend/nuevo-diseno
```

### 🧪 Para el equipo TESTING (Windows 10)
```powershell
# 1. Seguir instructivo general Windows (usando rama testing)
git checkout testing
git pull origin testing

# 2. Configurar entorno testing
copy .env.testing .env

# 3. Ejecutar todos los tests
python manage.py test --settings=sistema_bienes.settings.testing

# 4. Ejecutar tests específicos
python manage.py test core.tests --settings=sistema_bienes.settings.testing

# 5. Probar manualmente
python manage.py runserver 8001 --settings=sistema_bienes.settings.testing

# 6. Crear informe de bugs
# Usar GitHub Issues para reportar problemas
```

---

## 🔄 INSTRUCTIVO INTEGRACIÓN Y PASO A PRODUCCIÓN (Windows 10)

### 🚀 Paso 1: Integración de características
```powershell
# 1. Posicionarse en development
git checkout development
git pull origin development

# 2. Mergear features probadas
git merge frontend/nuevo-diseno
git merge backend/nueva-feature

# 3. Resolver conflictos si los hay
# 4. Ejecutar tests de integración
python manage.py test --settings=sistema_bienes.settings.testing

# 5. Hacer push a development
git push origin development
```

### 🚀 Paso 2: Testing integral
```powershell
# 1. Los testers prueban en rama testing
git checkout testing
git merge development
git push origin testing

# 2. Ejecutar tests automatizados
python manage.py test --settings=sistema_bienes.settings.testing

# 3. Pruebas manuales exhaustivas
```

### 🚀 Paso 3: Preparación para producción
```powershell
# 1. Desde testing, mergear a main
git checkout main
git pull origin main
git merge testing

# 2. Configurar entorno producción
copy .env.production .env

# 3. Actualizar SECRET_KEY en .env
# Generar nueva clave: python -c "import secrets; print(secrets.token_urlsafe(50))"

# 4. Configurar ALLOWED_HOSTS con dominio real
```

### 🚀 Paso 4: Despliegue en producción (Windows 10)
```powershell
# 1. Instalar dependencias de producción
pip install -r requirements/production.txt

# 2. Aplicar migraciones
python manage.py migrate --settings=sistema_bienes.settings.production

# 3. Colectar archivos estáticos
python manage.py collectstatic --noinput --settings=sistema_bienes.settings.production

# 4. Crear superusuario de producción
python manage.py createsuperuser --settings=sistema_bienes.settings.production

# 5. Configurar servidor web (usando waitress para Windows)
pip install waitress
```

### 🚀 Paso 5: Ejecutar en producción
```powershell
# 1. Ejecutar con waitress (HTTP)
waitress-serve --port=8000 sistema_bienes.wsgi:application

# 2. O para producción real (con reverse proxy)
# Configurar IIS o Nginx con Windows

# 3. Verificar que funciona
# Abrir: http://localhost:8000/
```

### 🚀 Paso 6: Monitoreo y mantenimiento
```powershell
# 1. Verificar logs
Get-Content logfile.log -Wait  # PowerShell

# 2. Backup de base de datos SQLite
$fecha = Get-Date -Format "yyyyMMdd"
Copy-Item db.sqlite3 "backup/db_$fecha.sqlite3"

# 3. Verificar estado
python manage.py check --deploy --settings=sistema_bienes.settings.production
```

---

## 📊 GESTIÓN DE BASE DE DATOS SQLITE

### 🔧 Comandos útiles para todos los equipos
```powershell
# 1. Ver estado de la BD
python manage.py dbshell
# En SQLite shell: .tables .schema .quit

# 2. Backup manual
python manage.py dumpdata > backup_$(Get-Date -Format "yyyyMMdd").json

# 3. Restaurar backup
python manage.py loaddata backup_20231201.json

# 4. Ver tamaño de BD
Get-ChildItem *.sqlite3 | Select-Object Name, Length

# 5. Optimizar BD SQLite
python manage.py dbshell
# Ejecutar: VACUUM;
```

### 🚨 Solución de problemas comunes
```powershell
# 1. Si hay error de migraciones
python manage.py migrate --fake-initial

# 2. Si la BD se corrompe
python manage.py flush  # CUIDADO: borra datos
# Mejor: restaurar desde backup

# 3. Si hay conflictos de migraciones
python manage.py makemigrations --merge

# 4. Reset completo (solo desarrollo)
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## ✅ CHECKLIST FINAL POR ROL

### Para BACKEND:
- [ ] Entorno virtual configurado
- [ ] Dependencias instaladas
- [ ] BD SQLite funcionando
- [ ] Migraciones aplicadas
- [ ] Superusuario creado
- [ ] Servidor ejecutándose
- [ ] Rama feature creada

### Para FRONTEND:
- [ ] Entorno virtual configurado
- [ ] Dependencias instaladas
- [ ] Servidor ejecutándose
- [ ] Templates accesibles
- [ ] Archivos estáticos cargando
- [ ] Rama feature creada

### Para TESTING:
- [ ] Entorno testing configurado
- [ ] Tests ejecutándose
- [ ] Issues reportados en GitHub
- [ ] Checklist de pruebas completado

### Para INTEGRACIÓN:
- [ ] Features mergeadas en development
- [ ] Tests de integración pasando
- [ ] Testing completo realizado
- [ ] Preparación producción completada

---

¡Todos los instructivos están listos para que los equipos comiencen a trabajar! 🚀🎯
