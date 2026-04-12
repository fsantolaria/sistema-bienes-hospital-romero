#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

echo "===================================="
echo "  SISTEMA DE BIENES - HOSPITAL"
echo "  DEPLOY COMPLETO v2.0 (macOS)"
echo "===================================="
echo

# --- Configuración base (usa SIEMPRE la carpeta donde está el script) ---
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKUP_DIR="$PROJECT_DIR/backups"
LOG_DIR="$PROJECT_DIR/logs"
STATIC_DIR="$PROJECT_DIR/static"
MEDIA_DIR="$PROJECT_DIR/media"
DB_DIR="$PROJECT_DIR/db"
BRANCH="${BRANCH:-development}"            # podés export BRANCH=otra_rama si querés
VENV_DIR="$PROJECT_DIR/venv"
TIMESTAMP="$(date +"%Y-%m-%d_%H-%M")"

# Usar SIEMPRE el mismo settings que tu manage.py por defecto
SETTINGS_MODULE="sistema_bienes.settings.development"

# Detectar archivo de BD preferido (ajustá si tenés otra ruta/nombre)
if [ -f "$PROJECT_DIR/db_development.sqlite3" ]; then
  DB_FILE="$PROJECT_DIR/db_development.sqlite3"
elif [ -f "$DB_DIR/produccion.sqlite3" ]; then
  DB_FILE="$DB_DIR/produccion.sqlite3"
else
  DB_FILE=""  # no corta el deploy; solo no hace backup
fi

# --- Crear directorios necesarios ---
for d in "$BACKUP_DIR" "$LOG_DIR" "$STATIC_DIR" "$MEDIA_DIR" "$DB_DIR"; do
  [ -d "$d" ] || mkdir -p "$d"
done

# --- Detección de Internet ---
echo "Verificando conectividad..."
if ping -c 1 github.com &>/dev/null; then
  INTERNET_MODE="ONLINE"
  echo "✅ Modo: CON INTERNET"
else
  INTERNET_MODE="OFFLINE"
  echo "⚠️ Modo: SIN INTERNET"
fi

cd "$PROJECT_DIR"

# --- Backup crítico ---
echo "Realizando backup de seguridad..."
if [ -n "${DB_FILE}" ] && [ -f "$DB_FILE" ]; then
  cp "$DB_FILE" "$BACKUP_DIR/backup_${TIMESTAMP}.sqlite3"
  echo "✅ Backup BD: backup_${TIMESTAMP}.sqlite3"
else
  echo "ℹ️  No se encontró archivo de BD para respaldar (continúo igual)."
fi

# --- Deploy según modo ---
if [ "$INTERNET_MODE" = "ONLINE" ]; then
  echo "🌐 Realizando deploy ONLINE desde Git..."

  if [ -d ".git" ]; then
    echo "Repositorio ya existe → actualizando..."
    git fetch origin || true
    git stash || true
    git checkout "$BRANCH" || git checkout -b "$BRANCH"
    git pull origin "$BRANCH" || true
    git stash pop || true
  else
    echo "Repositorio no inicializado → configurando origen..."
    git init
    if git remote get-url origin &>/dev/null; then
      git remote set-url origin "https://github.com/fsantolaria/sistema-bienes-hospital-romero.git"
    else
      git remote add origin "https://github.com/fsantolaria/sistema-bienes-hospital-romero.git"
    fi
    git fetch origin
    git checkout -b "$BRANCH" "origin/$BRANCH" || git checkout -b "$BRANCH"
  fi

else
  echo "📦 Modo OFFLINE – usando archivos locales"
  if [ ! -f "manage.py" ]; then
    echo "❌ ERROR: No hay manage.py en $PROJECT_DIR"
    exit 1
  fi
  echo "✅ Archivos del proyecto encontrados"
fi

# --- Post deploy ---
echo "Configurando entorno..."

# Entorno virtual
if [ ! -d "$VENV_DIR" ]; then
  echo "Creando entorno virtual..."
  python3 -m venv "$VENV_DIR"
fi

# Activar entorno
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

# Instalar dependencias
if   [ -f "requirements.txt" ]; then REQ_FILE="requirements.txt"
elif [ -f "requirements/base.txt" ]; then REQ_FILE="requirements/base.txt"
else REQ_FILE=""; fi

if [ -n "$REQ_FILE" ]; then
  echo "Instalando dependencias desde $REQ_FILE ..."
  pip install --upgrade pip
  pip install -r "$REQ_FILE"
else
  echo "ℹ️  No se encontró requirements.txt ni requirements/base.txt; salto instalación."
fi

# Mostrar DB efectiva
echo "DB en uso (según $SETTINGS_MODULE):"
python manage.py shell --settings="$SETTINGS_MODULE" -c "from django.conf import settings; print(settings.DATABASES['default']['NAME'])" || true

# Migraciones y estáticos (SIEMPRE con --settings)
echo "Aplicando migraciones..."
python manage.py makemigrations --noinput --settings="$SETTINGS_MODULE" || true
python manage.py migrate --noinput --settings="$SETTINGS_MODULE"

echo "Colectando archivos estáticos..."
python manage.py collectstatic --noinput --clear --settings="$SETTINGS_MODULE" || true

# Superusuario automático (si no existe)
echo "Configurando usuario administrador..."
python manage.py shell --settings="$SETTINGS_MODULE" <<'PYCODE'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@hospital.com', 'Admin123!!')
    print("✅ Superusuario creado")
else:
    print("✅ Superusuario ya existe")
PYCODE

# Lanzar servidor (modo desarrollo) -> escribir en logs/app.log
LOG_FILE="$LOG_DIR/app.log"
# Rotar log anterior (opcional)
if [ -f "$LOG_FILE" ]; then mv "$LOG_FILE" "$LOG_DIR/app_$TIMESTAMP.log"; fi

echo "Iniciando servidor en segundo plano..."
nohup python manage.py runserver 0.0.0.0:8000 --settings="$SETTINGS_MODULE" > "$LOG_FILE" 2>&1 &

echo
echo "===================================="
echo " 🎉 DEPLOY COMPLETADO EXITOSO"
echo "===================================="
echo "Modo: $INTERNET_MODE"
echo "URL: http://localhost:8000"
echo "Usuario: admin / Contraseña: Admin123!!"
[ -n "${DB_FILE}" ] && echo "Backup creado: backup_${TIMESTAMP}.sqlite3"
echo "Logs: $LOG_FILE"
