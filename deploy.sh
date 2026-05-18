#!/bin/bash

# Script de despliegue para CRM Django en producción
# Uso: ./deploy.sh

set -e  # Detener si hay errores

echo "================================"
echo "CRM Django - Script de Despliegue"
echo "================================"

# Variables
PROJECT_PATH="/home/usuario/crm1"
VENV_PATH="$PROJECT_PATH/venv"
USER="www-data"
GROUP="www-data"

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}1. Actualizar código del repositorio${NC}"
cd $PROJECT_PATH
git pull origin main

echo -e "${YELLOW}2. Activar entorno virtual${NC}"
source $VENV_PATH/bin/activate

echo -e "${YELLOW}3. Instalar dependencias${NC}"
pip install -q -r requirements.txt

echo -e "${YELLOW}4. Ejecutar migraciones${NC}"
python manage.py migrate

echo -e "${YELLOW}5. Recolectar archivos estáticos${NC}"
python manage.py collectstatic --noinput

echo -e "${YELLOW}6. Ejecutar tests${NC}"
python manage.py test

echo -e "${YELLOW}7. Reiniciar servicios${NC}"
systemctl restart crm.service
systemctl restart crm-celery.service
systemctl restart crm-celery-beat.service
systemctl restart nginx

echo -e "${GREEN}✓ Despliegue completado exitosamente${NC}"
echo ""
echo "Pasos siguientes:"
echo "1. Verifica que la aplicación está corriendo: systemctl status crm"
echo "2. Verifica los logs: journalctl -u crm -f"
echo "3. Accede a: https://yourdomain.com"
