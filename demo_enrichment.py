#!/usr/bin/env python3
"""
Demo: Enriquecimiento de Noticias

Demuestra cómo el sistema enriquece noticias con contexto adicional.
"""

import json
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.content_enricher import ContentEnricher


def main():
    """Ejecuta demo de enriquecimiento."""
    
    print("=" * 70)
    print("🔍 DEMO: Enriquecimiento de Noticias")
    print("=" * 70)
    
    # Cargar noticias
    news_file = Path("data/news.json")
    if not news_file.exists():
        print("❌ No hay noticias. Ejecuta primero: python3 src/main.py collect")
        return
    
    with open(news_file, 'r', encoding='utf-8') as f:
        all_news = json.load(f)
    
    print(f"\n📊 Noticias disponibles: {len(all_news)}")
    
    # Seleccionar noticias interesantes para enriquecer
    # Priorizar HN y Reddit que tienen comentarios
    candidates = []
    
    for news in all_news:
        collector = news.get('collector', '')
        if collector in ['hackernews', 'reddit_scraper']:
            candidates.append(news)
    
    # Si no hay HN/Reddit, usar las primeras 3
    if not candidates:
        candidates = all_news[:3]
    else:
        candidates = candidates[:3]  # Top 3
    
    print(f"🎯 Seleccionadas para enriquecer: {len(candidates)}")
    print()
    
    # Mostrar noticias seleccionadas
    for i, news in enumerate(candidates, 1):
        print(f"{i}. {news.get('title', '')[:60]}...")
        print(f"   Fuente: {news.get('source', 'N/A')}")
        print(f"   Collector: {news.get('collector', 'N/A')}")
        print()
    
    # Preguntar confirmación
    response = input("¿Enriquecer estas noticias? (s/n): ")
    if response.lower() != 's':
        print("Cancelado.")
        return
    
    # Enriquecer
    enricher = ContentEnricher()
    enriched_news = enricher.enrich_multiple(candidates, delay=2.0)
    
    # Guardar
    output_file = Path("data/demo_enriched_news.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(enriched_news, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Guardado en: {output_file}")
    
    # Mostrar comparación
    print("\n" + "=" * 70)
    print("📊 COMPARACIÓN: Antes vs Después")
    print("=" * 70)
    
    for i, (original, enriched) in enumerate(zip(candidates, enriched_news), 1):
        print(f"\n{i}. {original['title'][:60]}...")
        print(f"   Fuente: {original.get('source', 'N/A')}")
        print()
        
        # ANTES
        print("   📝 ANTES del enriquecimiento:")
        print(f"      - Summary: {len(original.get('summary', ''))} caracteres")
        print(f"      - Content: {len(original.get('content', ''))} caracteres")
        print(f"      - Keywords: {len(original.get('extracted_keywords', []))} ")
        print(f"      - Comentarios: {original.get('num_comments', 0)}")
        print()
        
        # DESPUÉS
        print("   ✨ DESPUÉS del enriquecimiento:")
        print(f"      - Full Content: {enriched.get('content_length', 0)} caracteres")
        print(f"      - Keywords Extraídos: {len(enriched.get('extracted_keywords', []))}")
        if enriched.get('extracted_keywords'):
            print(f"        {', '.join(enriched['extracted_keywords'][:5])}")
        print(f"      - Comentarios Top: {len(enriched.get('top_comments', []))}")
        if enriched.get('top_comments'):
            for j, comment in enumerate(enriched['top_comments'][:2], 1):
                print(f"        {j}. [{comment['score']} pts] {comment['text'][:60]}...")
        print(f"      - Engagement Score: {enriched.get('engagement_score', 0):.1f}")
        print(f"      - Status: {enriched.get('enrichment_status', 'unknown')}")
        print()
    
    print("=" * 70)
    print("✅ Demo completado!")
    print()
    print("📚 Siguiente paso: Entrenar modelo ML con estas noticias")
    print("   Ver: GUIA_ML_ENRIQUECIMIENTO.md")
    print("=" * 70)


if __name__ == "__main__":
    main()
