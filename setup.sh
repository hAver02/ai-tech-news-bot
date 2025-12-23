#!/bin/bash

# Script de configuración inicial del proyecto
# Este script automatiza todos los pasos de instalación

echo "🚀 Configurando TechNews Tweet Generator..."
echo ""

# Verificar Python
echo "1️⃣  Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado. Por favor instálalo desde python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "   ✅ $PYTHON_VERSION encontrado"
echo ""

# Crear entorno virtual
echo "2️⃣  Creando entorno virtual..."
if [ -d "venv" ]; then
    echo "   ⚠️  El entorno virtual ya existe, saltando..."
else
    python3 -m venv venv
    echo "   ✅ Entorno virtual creado"
fi
echo ""

# Activar entorno virtual
echo "3️⃣  Activando entorno virtual..."
source venv/bin/activate
echo "   ✅ Entorno virtual activado"
echo ""

# Instalar dependencias
echo "4️⃣  Instalando dependencias..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "   ✅ Dependencias instaladas"
echo ""

# Crear directorios
echo "5️⃣  Creando directorios..."
mkdir -p data
mkdir -p logs
echo "   ✅ Directorios creados"
echo ""

# Copiar archivo de ejemplo de .env
echo "6️⃣  Configurando archivo .env..."
if [ ! -f ".env" ]; then
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "   ✅ Archivo .env creado (edítalo para agregar tus API keys)"
    fi
else
    echo "   ⚠️  El archivo .env ya existe, saltando..."
fi
echo ""

# Probar instalación
echo "7️⃣  Probando instalación..."
python3 -c "import feedparser, requests, yaml; print('   ✅ Todas las librerías importadas correctamente')"
echo ""

echo "✨ ¡Configuración completada!"
echo ""
echo "📝 Próximos pasos:"
echo ""
echo "   1. Activa el entorno virtual:"
echo "      source venv/bin/activate"
echo ""
echo "   2. Prueba el recolector RSS:"
echo "      python src/collectors/rss_collector.py"
echo ""
echo "   3. Genera tweets:"
echo "      python src/generators/tweet_generator.py"
echo ""
echo "   4. Lee el TUTORIAL.md para más información"
echo ""
echo "¡Feliz aprendizaje! 🎉"

