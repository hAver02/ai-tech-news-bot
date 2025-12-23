#!/bin/bash

# Script para configurar cron jobs (automatización)
# Este script ejecutará tu recolector 2 veces al día

echo "⏰ Configurando automatización (cron jobs)..."
echo ""

# Obtener la ruta absoluta del proyecto
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_BIN="$PROJECT_DIR/venv/bin/python"
SCRIPT="$PROJECT_DIR/run_automated.py"

echo "📁 Directorio del proyecto: $PROJECT_DIR"
echo "🐍 Python: $PYTHON_BIN"
echo "📜 Script: $SCRIPT"
echo ""

# Crear el comando cron
CRON_CMD_MORNING="0 9 * * * cd $PROJECT_DIR && $PYTHON_BIN $SCRIPT >> logs/cron.log 2>&1"
CRON_CMD_EVENING="0 18 * * * cd $PROJECT_DIR && $PYTHON_BIN $SCRIPT >> logs/cron.log 2>&1"

echo "📋 Comandos cron a instalar:"
echo ""
echo "   Mañana (9:00 AM):"
echo "   $CRON_CMD_MORNING"
echo ""
echo "   Tarde (6:00 PM):"
echo "   $CRON_CMD_EVENING"
echo ""

# Preguntar confirmación
read -p "¿Quieres instalar estos cron jobs? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]
then
    # Backup del crontab actual
    crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S).txt 2>/dev/null
    
    # Agregar nuevos cron jobs
    (crontab -l 2>/dev/null; echo ""; echo "# TechNews Tweet Generator - Morning run"; echo "$CRON_CMD_MORNING") | crontab -
    (crontab -l 2>/dev/null; echo "# TechNews Tweet Generator - Evening run"; echo "$CRON_CMD_EVENING") | crontab -
    
    echo "✅ Cron jobs instalados exitosamente!"
    echo ""
    echo "📅 Horarios de ejecución:"
    echo "   - 9:00 AM todos los días"
    echo "   - 6:00 PM todos los días"
    echo ""
    echo "📊 Para ver tus cron jobs:"
    echo "   crontab -l"
    echo ""
    echo "🗑️  Para eliminar los cron jobs:"
    echo "   crontab -e  (y borrar las líneas de TechNews)"
    echo ""
    echo "📝 Los logs se guardarán en: logs/cron.log"
else
    echo "❌ Instalación cancelada"
    echo ""
    echo "💡 También puedes instalar manualmente:"
    echo "   1. Ejecuta: crontab -e"
    echo "   2. Agrega estas líneas:"
    echo "      $CRON_CMD_MORNING"
    echo "      $CRON_CMD_EVENING"
fi

