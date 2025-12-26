"""
Continuous Collector Agent - Agente que busca noticias continuamente

Este agente:
1. Busca noticias cada X minutos
2. Solo trae noticias MUY recientes (últimas 2-4 horas)
3. Prioriza fuentes en tiempo real
4. Evita duplicados
"""

import time
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Set, Optional
import hashlib


class ContinuousCollectorAgent:
    """
    Agente que recopila noticias continuamente en tiempo real.
    
    Características:
    - Ejecución periódica automática
    - Solo noticias MUY recientes
    - Detección de duplicados
    - Prioriza "new" y "breaking" stories
    """
    
    def __init__(
        self,
        interval_minutes: int = 30,
        max_age_hours: int = 4,
        storage_path: str = "data/realtime_news.json"
    ):
        """
        Inicializa el agente recopilador continuo.
        
        Args:
            interval_minutes: Minutos entre recopilaciones
            max_age_hours: Máxima antigüedad de noticias (horas)
            storage_path: Ruta para guardar noticias
        """
        self.interval_minutes = interval_minutes
        self.max_age_hours = max_age_hours
        self.storage_path = Path(storage_path)
        self.seen_urls: Set[str] = set()
        
        # Cargar URLs vistas si existen
        self._load_seen_urls()
    
    def _load_seen_urls(self):
        """Carga las URLs ya vistas para evitar duplicados."""
        seen_file = Path("data/seen_urls.txt")
        if seen_file.exists():
            with open(seen_file, 'r') as f:
                self.seen_urls = set(line.strip() for line in f)
    
    def _save_seen_urls(self):
        """Guarda las URLs vistas."""
        seen_file = Path("data/seen_urls.txt")
        seen_file.parent.mkdir(exist_ok=True)
        with open(seen_file, 'w') as f:
            for url in self.seen_urls:
                f.write(f"{url}\n")
    
    def _is_duplicate(self, news_item: Dict) -> bool:
        """
        Verifica si la noticia es duplicada.
        
        Args:
            news_item: Noticia a verificar
            
        Returns:
            True si es duplicada
        """
        url = news_item.get('link', '')
        title = news_item.get('title', '')
        
        # Verificar por URL
        if url and url in self.seen_urls:
            return True
        
        # Verificar por hash del título
        title_hash = hashlib.md5(title.encode()).hexdigest()
        if title_hash in self.seen_urls:
            return True
        
        return False
    
    def _mark_as_seen(self, news_item: Dict):
        """Marca una noticia como vista."""
        url = news_item.get('link', '')
        title = news_item.get('title', '')
        
        if url:
            self.seen_urls.add(url)
        
        title_hash = hashlib.md5(title.encode()).hexdigest()
        self.seen_urls.add(title_hash)
    
    def collect_realtime_news(self) -> List[Dict]:
        """
        Recopila noticias en tiempo real de fuentes rápidas.
        
        Returns:
            Lista de noticias nuevas y recientes
        """
        from src.collectors.hackernews_collector import HackerNewsCollector
        from src.collectors.devto_collector import DevToCollector
        from src.collectors.algolia_hn_collector import AlgoliaHNCollector
        from src.collectors.github_trending_collector import GitHubTrendingCollector
        from src.collectors.github_releases_collector import GitHubReleasesCollector
        from src.collectors.tavily_collector import TavilyCollector
        from src.collectors.serper_collector import SerperCollector
        from src.collectors.producthunt_collector import ProductHuntCollector
        from src.utils.query_builder import QueryBuilder
        
        print(f"\n🔄 AGENTE RECOPILADOR CONTINUO")
        print(f"   Buscando noticias de las últimas {self.max_age_hours} horas...")
        print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        all_news = []
        
        # Cargar query builder
        query_builder = QueryBuilder()
        
        # 1. Algolia HN (GRATIS - búsqueda con filtros temporales)
        print(f"\n   📡 Algolia HN Search (tiempo real)")
        algolia = AlgoliaHNCollector()
        algolia_news = algolia.collect_multiple_queries(
            queries=[
                "Cursor OR AI coding",
                "TypeScript OR Next.js OR React",
                "Nvidia OR GPU OR AI chips",
                "OpenAI OR Anthropic OR Claude",
                "Rust OR Python OR JavaScript"
            ],
            max_results_per_query=8,
            max_age_hours=self.max_age_hours
        )
        print(f"      ✅ {len(algolia_news)} historias")
        all_news.extend(algolia_news)
        
        # 2. GitHub Trending (GRATIS)
        print(f"\n   ⭐ GitHub Trending")
        gh_trending = GitHubTrendingCollector()
        gh_news = gh_trending.collect_multiple_languages(
            languages=['python', 'typescript', 'rust', 'go', 'javascript'],
            max_results_per_language=3
        )
        print(f"      ✅ {len(gh_news)} repos trending")
        all_news.extend(gh_news)
        
        # 3. GitHub Releases (GRATIS - releases oficiales)
        print(f"\n   📦 GitHub Releases")
        gh_releases = GitHubReleasesCollector()
        releases = gh_releases.collect_all(
            max_releases_per_repo=2,
            max_age_days=7
        )
        print(f"      ✅ {len(releases)} releases oficiales")
        all_news.extend(releases)
        
        # 4. Tavily AI (DE PAGO - queries ESPECÍFICAS)
        tavily = TavilyCollector()
        if tavily.api_key:
            print(f"\n   🔍 Tavily AI Search (queries específicas)")
            # Usar queries de alta prioridad
            priority_queries = query_builder.get_high_priority_queries(count=6)
            tavily_news = tavily.collect_multiple_queries(
                queries=priority_queries,
                max_results_per_query=4
            )
            print(f"      ✅ {len(tavily_news)} noticias")
            all_news.extend(tavily_news)
        
        # 5. Serper (DE PAGO - queries ESPECÍFICAS)
        serper = SerperCollector()
        if serper.api_key:
            print(f"\n   🔍 Serper (Google Search - queries específicas)")
            # Usar queries específicas de AI coding y hardware
            ai_coding = query_builder.get_queries_by_category('ai_coding', max_queries=3)
            hardware = query_builder.get_queries_by_category('hardware_ai', max_queries=3)
            queries = ai_coding + hardware
            
            serper_news = serper.collect_multiple_queries(
                queries=queries,
                num_results_per_query=4,
                time_filter="h" if self.max_age_hours <= 6 else "d"
            )
            print(f"      ✅ {len(serper_news)} noticias")
            all_news.extend(serper_news)
        
        # 6. Product Hunt (GRATIS - requiere API key)
        ph = ProductHuntCollector()
        if ph.api_key:
            print(f"\n   🚀 Product Hunt")
            ph_news = ph.collect_today(max_results=10)
            print(f"      ✅ {len(ph_news)} productos")
            all_news.extend(ph_news)
        
        # 7. Hacker News "new" (GRATIS - fallback)
        print(f"\n   📡 Hacker News (new stories)")
        hn = HackerNewsCollector()
        hn_new = hn.collect(story_type='new', max_items=30, min_score=10)
        print(f"      ✅ {len(hn_new)} historias nuevas")
        all_news.extend(hn_new)
        
        # 8. Dev.to (GRATIS)
        print(f"\n   📡 Dev.to (latest articles)")
        devto = DevToCollector()
        devto_news = devto.collect_multiple_tags(
            tags=['ai', 'typescript', 'nextjs', 'rust', 'supabase'],
            per_page_per_tag=3,
            min_reactions=0
        )
        print(f"      ✅ {len(devto_news)} artículos nuevos")
        all_news.extend(devto_news)
        
        # Filtrar por antigüedad y duplicados
        cutoff_time = datetime.now() - timedelta(hours=self.max_age_hours)
        fresh_news = []
        stats = {'total': len(all_news), 'duplicates': 0, 'old': 0, 'new': 0}
        
        for news in all_news:
            # Verificar duplicado
            if self._is_duplicate(news):
                stats['duplicates'] += 1
                continue
            
            # Verificar antigüedad
            published = news.get('published', '')
            if published:
                try:
                    from dateutil import parser
                    pub_date = parser.parse(published)
                    if pub_date.timestamp() < cutoff_time.timestamp():
                        stats['old'] += 1
                        continue
                except:
                    pass
            
            # Noticia válida
            fresh_news.append(news)
            self._mark_as_seen(news)
            stats['new'] += 1
        
        print(f"\n   📊 RESULTADO:")
        print(f"      Total recopiladas: {stats['total']}")
        print(f"      🆕 Nuevas: {stats['new']}")
        print(f"      🔄 Duplicadas: {stats['duplicates']}")
        print(f"      ⏰ Antiguas: {stats['old']}")
        
        # Guardar URLs vistas
        self._save_seen_urls()
        
        return fresh_news
    
    def save_news(self, news_list: List[Dict]):
        """
        Guarda noticias en archivo.
        
        Args:
            news_list: Lista de noticias
        """
        self.storage_path.parent.mkdir(exist_ok=True)
        
        # Cargar noticias existentes
        existing_news = []
        if self.storage_path.exists():
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                existing_news = json.load(f)
        
        # Agregar nuevas
        existing_news.extend(news_list)
        
        # Limitar a últimas 200 noticias
        if len(existing_news) > 200:
            existing_news = existing_news[-200:]
        
        # Guardar
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(existing_news, f, ensure_ascii=False, indent=2)
        
        print(f"   💾 Guardadas en: {self.storage_path}")
    
    def run_once(self) -> List[Dict]:
        """
        Ejecuta una recopilación única.
        
        Returns:
            Lista de noticias recopiladas
        """
        fresh_news = self.collect_realtime_news()
        
        if fresh_news:
            self.save_news(fresh_news)
        
        return fresh_news
    
    def run_continuously(self, duration_hours: Optional[int] = None):
        """
        Ejecuta el agente continuamente.
        
        Args:
            duration_hours: Duración en horas (None = infinito)
        """
        start_time = time.time()
        iteration = 0
        
        print(f"\n🚀 AGENTE RECOPILADOR CONTINUO INICIADO")
        print(f"   Interval: cada {self.interval_minutes} minutos")
        print(f"   Antigüedad máxima: {self.max_age_hours} horas")
        if duration_hours:
            print(f"   Duración: {duration_hours} horas")
        else:
            print(f"   Duración: infinito (Ctrl+C para detener)")
        
        try:
            while True:
                iteration += 1
                
                print(f"\n{'='*70}")
                print(f"🔄 ITERACIÓN #{iteration}")
                print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'='*70}")
                
                # Recopilar
                fresh_news = self.run_once()
                
                # Verificar duración
                if duration_hours:
                    elapsed = (time.time() - start_time) / 3600
                    if elapsed >= duration_hours:
                        print(f"\n⏰ Duración completada: {duration_hours}h")
                        break
                
                # Esperar próxima iteración
                print(f"\n⏸️  Esperando {self.interval_minutes} minutos...")
                time.sleep(self.interval_minutes * 60)
                
        except KeyboardInterrupt:
            print(f"\n\n🛑 Agente detenido por el usuario")
            print(f"   Total iteraciones: {iteration}")
            print(f"   URLs vistas: {len(self.seen_urls)}")


# Ejemplo de uso
if __name__ == "__main__":
    agent = ContinuousCollectorAgent(
        interval_minutes=30,  # Cada 30 minutos
        max_age_hours=4       # Solo últimas 4 horas
    )
    
    # Opción 1: Una sola ejecución
    # agent.run_once()
    
    # Opción 2: Continuo por 2 horas
    agent.run_continuously(duration_hours=2)
