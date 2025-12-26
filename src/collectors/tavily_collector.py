"""
Tavily AI Search Collector - Búsqueda en tiempo real con IA

Tavily es una API de búsqueda optimizada para LLMs que devuelve:
- Resultados MUY recientes (últimas horas)
- Contenido ya procesado y limpio
- Contexto completo
- Muy barato: $0.001 por búsqueda

Documentación: https://docs.tavily.com
"""

import os
import requests
from typing import List, Dict
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class TavilyCollector:
    """
    Recopilador de noticias usando Tavily AI Search API.
    
    Características:
    - Búsqueda en tiempo real
    - Filtros por dominio
    - Filtros por fecha
    - Búsqueda avanzada
    """
    
    def __init__(self, api_key: str = None):
        """
        Inicializa el collector de Tavily.
        
        Args:
            api_key: API key de Tavily (o usa TAVILY_API_KEY del .env)
        """
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            print("⚠️  No se encontró TAVILY_API_KEY. Este collector no funcionará.")
        
        self.base_url = "https://api.tavily.com/search"
    
    def search(
        self,
        query: str,
        max_results: int = 10,
        search_depth: str = "advanced",
        include_domains: List[str] = None,
        days: int = 1
    ) -> List[Dict]:
        """
        Busca noticias en tiempo real con Tavily.
        
        Args:
            query: Búsqueda (ej: "OpenAI OR Anthropic OR Cursor")
            max_results: Máximo resultados (default: 10)
            search_depth: "basic" o "advanced" (advanced es mejor pero más caro)
            include_domains: Lista de dominios a incluir
            days: Días hacia atrás (1 = últimas 24h)
            
        Returns:
            Lista de noticias
        """
        if not self.api_key:
            return []
        
        print(f"\n🔍 Tavily Search: {query}")
        print(f"   Parámetros: max={max_results}, depth={search_depth}, days={days}")
        
        payload = {
            "api_key": self.api_key,
            "query": query,
            "max_results": max_results,
            "search_depth": search_depth,
            "include_answer": False,
            "include_raw_content": False
        }
        
        if include_domains:
            payload["include_domains"] = include_domains
        
        try:
            response = requests.post(self.base_url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            results = data.get('results', [])
            print(f"   ✅ {len(results)} resultados")
            
            # Convertir a formato estándar
            news_list = []
            for item in results:
                news_list.append({
                    'title': item.get('title', ''),
                    'link': item.get('url', ''),
                    'summary': item.get('content', '')[:500],
                    'full_content': item.get('content', ''),
                    'published': datetime.now().isoformat(),
                    'source': 'Tavily AI',
                    'score': item.get('score', 0),
                    'published_date': item.get('published_date', '')
                })
            
            return news_list
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error en Tavily: {str(e)}")
            return []
    
    def collect_multiple_queries(
        self,
        queries: List[str],
        max_results_per_query: int = 10
    ) -> List[Dict]:
        """
        Ejecuta múltiples búsquedas.
        
        Args:
            queries: Lista de búsquedas
            max_results_per_query: Resultados por búsqueda
            
        Returns:
            Lista combinada de noticias
        """
        all_news = []
        
        for query in queries:
            news = self.search(
                query=query,
                max_results=max_results_per_query,
                search_depth="advanced"
            )
            all_news.extend(news)
        
        return all_news


# Ejemplo de uso
if __name__ == "__main__":
    collector = TavilyCollector()
    
    # Buscar noticias tech recientes
    news = collector.collect_multiple_queries(
        queries=[
            "Cursor IDE OR AI coding assistants",
            "OpenAI OR Anthropic OR Claude",
            "TypeScript OR Next.js OR React",
            "Nvidia OR GPU shortage OR AI chips"
        ],
        max_results_per_query=5
    )
    
    print(f"\n📰 Total: {len(news)} noticias")
    for n in news[:3]:
        print(f"   - {n['title']}")
