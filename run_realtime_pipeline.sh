#!/bin/bash
# Pipeline completo de noticias en tiempo real

set -e  # Exit on error

echo "🚀 INICIANDO PIPELINE DE NOTICIAS EN TIEMPO REAL"
echo "================================================"

# Activar entorno virtual
source venv/bin/activate

# 1. Recopilar noticias en tiempo real
echo ""
echo "📡 PASO 1: Recopilando noticias en tiempo real..."
python -c "
from src.agents.continuous_collector_agent import ContinuousCollectorAgent

agent = ContinuousCollectorAgent(interval_minutes=30, max_age_hours=4)
news = agent.run_once()
print(f'\n✅ {len(news)} noticias frescas recopiladas')
"

# 2. Copiar a news.json para validación
cp data/realtime_news.json data/news.json

# 3. Validar con LLM (primeras 30 noticias)
echo ""
echo "🤖 PASO 2: Validando noticias con Agente LLM..."
python -c "
from src.agents.news_validator_agent import NewsValidatorAgent
import json

with open('data/realtime_news.json', 'r', encoding='utf-8') as f:
    news = json.load(f)

agent = NewsValidatorAgent()
validated = agent.validate_batch(
    news[:30],  # Primeras 30
    min_relevance=50,
    min_quality=50,
    require_recent=False
)

if validated:
    with open('data/validated_news.json', 'w', encoding='utf-8') as f:
        json.dump(validated, f, ensure_ascii=False, indent=2)
    print(f'\n✅ {len(validated)} noticias validadas')
else:
    print('\n⚠️  Ninguna noticia pasó la validación')
    exit(1)
"

# 4. Copiar a approved_news.json para generación
cp data/validated_news.json data/approved_news.json

# 5. Generar tweets
echo ""
echo "🐦 PASO 3: Generando tweets..."
python src/main.py generate

# 6. Mostrar resumen
echo ""
echo "================================================"
echo "✅ PIPELINE COMPLETADO"
echo "================================================"

python -c "
import json

# Contar noticias
with open('data/realtime_news.json', 'r') as f:
    total_news = len(json.load(f))

with open('data/validated_news.json', 'r') as f:
    validated = len(json.load(f))

with open('data/ai_tweets.json', 'r') as f:
    tweets = json.load(f)
    en_tweets = [t for t in tweets if t.get('language') == 'en']
    es_tweets = [t for t in tweets if t.get('language') == 'es']

print(f'\n📊 RESUMEN:')
print(f'   📰 Noticias recopiladas: {total_news}')
print(f'   ✅ Noticias validadas: {validated}')
print(f'   🐦 Tweets generados: {len(tweets)}')
print(f'      🇺🇸 Inglés: {len(en_tweets)}')
print(f'      🇪🇸 Español: {len(es_tweets)}')
print(f'\n📁 Archivos generados:')
print(f'   - data/realtime_news.json')
print(f'   - data/validated_news.json')
print(f'   - data/ai_tweets.json')
print(f'\n🎉 ¡Listo para publicar!')
"

echo ""
