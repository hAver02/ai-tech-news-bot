#!/usr/bin/env python3
"""
Script de prueba para verificar que News API funciona.

Uso:
    python test_news_api.py
"""

import os
from dotenv import load_dotenv

# Cargar .env
load_dotenv()

print("="*60)
print("🧪 TEST DE NEWS API")
print("="*60)

# Verificar que existe la API key
api_key = os.getenv("NEWS_API_KEY")

if not api_key:
    print("\n⚠️  NEWS_API_KEY no está configurado (opcional)")
    print("\n💡 Si quieres usar News API:")
    print("   1. Obtén tu API key gratis en: https://newsapi.org/register")
    print("   2. Agrégala al archivo .env:")
    print("      NEWS_API_KEY=tu_clave_aqui")
    print("   3. Vuelve a ejecutar este script")
    print("\n✅ Puedes seguir usando solo RSS Feeds sin problema.")
    exit(0)

print(f"\n✅ API Key encontrada: {api_key[:8]}...{api_key[-4:]}")

# Intentar conectar con News API
print("\n🔌 Conectando con News API...")

try:
    import requests
    
    # Test simple
    print("📤 Haciendo request de prueba...")
    
    params = {
        'q': 'technology',
        'language': 'en',
        'pageSize': 3,
        'apiKey': api_key
    }
    
    response = requests.get(
        'https://newsapi.org/v2/everything',
        params=params,
        timeout=10
    )
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    if data.get('status') != 'ok':
        raise Exception(data.get('message', 'Unknown error'))
    
    articles = data.get('articles', [])
    total = data.get('totalResults', 0)
    
    print(f"📥 Respuesta recibida: {len(articles)} artículos")
    print(f"📊 Total disponible: {total:,} artículos")
    
    if articles:
        print("\n📰 Ejemplo de noticia:")
        article = articles[0]
        print(f"   Título: {article['title'][:60]}...")
        print(f"   Fuente: {article['source']['name']}")
        print(f"   Fecha: {article['publishedAt']}")
    
    print("\n" + "="*60)
    print("✅ ¡NEWS API FUNCIONA! Está configurado correctamente")
    print("="*60)
    print("\n🚀 Ahora puedes usar:")
    print("   python src/main.py collect")
    print("\n   Recopilará noticias de:")
    print("   - RSS Feeds (TechCrunch, Hacker News, etc.)")
    print("   - News API (80,000+ fuentes)")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\n💡 Posibles causas:")
    print("   - API key incorrecta")
    print("   - Sin conexión a internet")
    print("   - Límite de requests excedido (100/día)")
    print("\n📖 Lee GUIA_NEWS_API.md para más ayuda")
    exit(1)

