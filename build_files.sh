#!/usr/bin/env bash
set -e

echo "==> Instalando dependencias..."
pip install -r requirements.txt

echo "==> Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --settings=sistema_bienes.settings.production
