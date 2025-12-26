"""
Algolia HN Collector - Hacker News con búsqueda avanzada

Algolia HN API proporciona:
- Búsqueda por keywords
- Filtros temporales EXACTOS (por timestamp)
- 100% GRATIS
- Actualizado en tiempo real

Documentación: https://hn.algolia.com/api
"""

import requests
from typing import List, Dict
from datetime import datetime, timedelta


class AlgoliaHNCollector:
    """
    Recopilador de Hacker News vía Algolia Search API.
    
    Características:
    - Búsqueda por keywords
    - Filtros temporales precisos
    - Ordenado por fecha
    - 100% gratuito
    """
    
    def __init__(self):
        """Inicializa el collector de Algolia HN."""
        self.base_url = "https://hn.algolia.com/api/v1"
    
    def search(
        self,
        query: str,
        max_results: int = 20,
        max_age_hours: int = 24,
        min_points: int = 10
    ) -> List[Dict]:
        """
        Busca en Hacker News con filtros.
        
        Args:
            query: Búsqueda (ej: "TypeScript OR Rust")
            max_results: Máximo resultados
            max_age_hours: Antigüedad máxima en horas
            min_points: Puntos mínimos
            
        Returns:
            Lista de noticias
        """
        print(f"\n🔍 Algolia HN: {query}")
        print(f"   Max age: {max_age_hours}h | Min points: {min_points}")
        
        # Calcular timestamp de corte
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        timestamp = int(cutoff_time.timestamp())
        
        params = {
            'query': query,
            'tags': 'story',
            'numericFilters': f'created_at_i>{timestamp},points>={min_points}',
            'hitsPerPage': max_results
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/search_by_date",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            hits = data.get('hits', [])
            print(f"   ✅ {len(hits)} historias")
            
            news_list = []
            for hit in hits:
                # Convertir timestamp a ISO
                created_at = datetime.fromtimestamp(
                    hit.get('created_at_i', 0)
                ).isoformat()
                
                news_list.append({
                    'title': hit.get('title', ''),
                    'link': hit.get('url', f"https://news.ycombinator.com/item?id={hit.get('objectID')}"),
                    'summary': hit.get('story_text', '') or f"HN Story | {hit.get('points', 0)} points | {hit.get('num_comments', 0)} comments",
                    'full_content': hit.get('story_text', ''),
                    'published': created_at,
                    'source': 'Hacker News (Algolia)',
                    'score': hit.get('points', 0),
                    'comments': hit.get('num_comments', 0)
                })
            
            return news_list
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error en Algolia HN: {str(e)}")
            return []
    
    def collect_multiple_queries(
        self,
        queries: List[str],
        max_results_per_query: int = 15,
        max_age_hours: int = 12
    ) -> List[Dict]:
        """
        Ejecuta múltiples búsquedas.
        
        Args:
            queries: Lista de búsquedas
            max_results_per_query: Resultados por búsqueda
            max_age_hours: Antigüedad máxima
            
        Returns:
            Lista combinada de noticias
        """
        all_news = []
        
        for query in queries:
            news = self.search(
                query=query,
                max_results=max_results_per_query,
                max_age_hours=max_age_hours,
                min_points=10
            )
            all_news.extend(news)
        
        return all_news


# Ejemplo de uso
if __name__ == "__main__":
    collector = AlgoliaHNCollector()
    
    # Buscar noticias de últimas 6 horas
    news = collector.collect_multiple_queries(
        queries=[
            "Cursor OR AI coding",
            "TypeScript OR Next.js",
            "Nvidia OR GPU",
            "OpenAI OR Anthropic"
        ],
        max_results_per_query=10,
        max_age_hours=6  # Últimas 6 HORAS
    )
    
    print(f"\n📰 Total: {len(news)} noticias")
    for n in news[:5]:
        print(f"   - [{n['score']} pts] {n['title']}")
