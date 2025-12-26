"""
Test del sistema mejorado de noticias
"""

print("🚀 PROBANDO SISTEMA MEJORADO DE NOTICIAS")
print("="*70)

# 1. Probar GitHub Releases
print("\n📦 TEST 1: GitHub Releases Collector")
print("-"*70)

from src.collectors.github_releases_collector import GitHubReleasesCollector

gh_releases = GitHubReleasesCollector()
releases = gh_releases.collect_all(
    max_releases_per_repo=1,  # Solo 1 por repo para test rápido
    max_age_days=30
)

print(f"\n✅ {len(releases)} releases recopilados")
if releases:
    print("\n📰 Ejemplos de releases:")
    for r in releases[:5]:
        breaking = "⚠️ BREAKING" if r.get('has_breaking_changes') else ""
        print(f"   - {r['title']} {breaking}")

# 2. Probar Query Builder
print("\n\n🔍 TEST 2: Query Builder")
print("-"*70)

from src.utils.query_builder import QueryBuilder

builder = QueryBuilder()

print("\n📋 Queries de AI Coding:")
ai_queries = builder.get_queries_by_category('ai_coding', max_queries=3)
for q in ai_queries:
    print(f"   - {q}")

print("\n📋 Queries prioritarias:")
priority = builder.get_high_priority_queries(count=5)
for q in priority:
    print(f"   - {q}")

# 3. Probar sistema completo mejorado
print("\n\n🔄 TEST 3: Sistema Completo Mejorado")
print("-"*70)

from src.agents.continuous_collector_agent import ContinuousCollectorAgent

agent = ContinuousCollectorAgent(interval_minutes=30, max_age_hours=4)
news = agent.run_once()

print(f"\n\n{'='*70}")
print(f"✅ RESULTADO FINAL:")
print(f"   Total noticias frescas: {len(news)}")
print(f"{'='*70}")

# Analizar por fuente
from collections import Counter
sources = Counter(n.get('source', 'Unknown') for n in news)

print(f"\n📊 DESGLOSE POR FUENTE:")
for source, count in sources.most_common():
    print(f"   {source}: {count} noticias")

# Mostrar releases con breaking changes
breaking_releases = [n for n in news if n.get('has_breaking_changes')]
if breaking_releases:
    print(f"\n⚠️  {len(breaking_releases)} RELEASES CON BREAKING CHANGES:")
    for r in breaking_releases:
        print(f"   - {r['title']}")

# Guardar para siguiente paso
import json
with open('data/improved_realtime_news.json', 'w', encoding='utf-8') as f:
    json.dump(news, f, ensure_ascii=False, indent=2)

print(f"\n💾 Guardado en: data/improved_realtime_news.json")
print(f"\n🎉 ¡Sistema mejorado funcionando!")
