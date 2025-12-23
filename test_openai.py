#!/usr/bin/env python3
"""
Script de prueba rápida para verificar que OpenAI funciona.

Uso:
    python test_openai.py
"""

import os
from dotenv import load_dotenv

# Cargar .env
load_dotenv()

print("="*60)
print("🧪 TEST DE OPENAI")
print("="*60)

# Verificar que existe la API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("\n❌ ERROR: No se encontró OPENAI_API_KEY en .env")
    print("\n📝 Pasos para configurar:")
    print("   1. Abre el archivo .env")
    print("   2. Pega tu API key después de OPENAI_API_KEY=")
    print("   3. Guarda el archivo")
    print("   4. Vuelve a ejecutar este script")
    exit(1)

if not api_key.startswith('sk-'):
    print("\n❌ ERROR: La API key no parece válida (debe empezar con 'sk-')")
    print(f"   Tu key empieza con: {api_key[:5]}...")
    exit(1)

print(f"\n✅ API Key encontrada: {api_key[:8]}...{api_key[-4:]}")

# Intentar conectar con OpenAI
print("\n🔌 Conectando con OpenAI...")

try:
    from openai import OpenAI
    
    client = OpenAI(api_key=api_key)
    
    # Test simple
    print("📤 Enviando request de prueba...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Di solo 'OK' si funciono"}
        ],
        max_tokens=10
    )
    
    answer = response.choices[0].message.content
    
    print(f"📥 Respuesta recibida: {answer}")
    print("\n" + "="*60)
    print("✅ ¡TODO FUNCIONA! OpenAI está configurado correctamente")
    print("="*60)
    print("\n🚀 Ahora puedes usar:")
    print("   python src/generators/ai_tweet_generator.py")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\n💡 Posibles causas:")
    print("   - API key incorrecta")
    print("   - No agregaste método de pago en OpenAI")
    print("   - Límite de cuota excedido")
    print("\n📖 Lee GUIA_API_KEY.md para más ayuda")
    exit(1)

