"""
NewsData.io Collector - Recopila noticias desde NewsData.io API

NewsData.io ofrece plan GRATIS con 200 requests por día.
Soporta 50+ idiomas incluido español.

Obtén tu API key gratis en: https://newsdata.io/register
"""

import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
import os
from dotenv import load_dotenv


class NewsDataCollector:
    """Recolector de noticias desde NewsData.io API."""
    
    BASE_URL = "https://newsdata.io/api/1/news"
    
    def __init__(self, api_key: str = None):
        """
        Inicializa el recolector de NewsData.io.
        
        Args:
            api_key: API key de NewsData.io (opcional, se carga de .env)
        """
        if api_key:
            self.api_key = api_key
        else:
            load_dotenv()
            self.api_key = os.getenv("NEWSDATA_API_KEY")
            
        if not self.api_key:
            print("⚠️  No se encontró NEWSDATA_API_KEY. Este collector no funcionará.")
            print("   Obtén una API key GRATIS (200 requests/día) en:")
            print("   https://newsdata.io/register")
    
    def collect(
        self,
        query: str = "technology",
        language: str = "en",
        max_results: int = 10,
        category: str = None
    ) -> List[Dict]:
        """
        Recopila noticias de NewsData.io.
        
        Args:
            query: Término de búsqueda
            language: Código de idioma (en, es, etc.)
            max_results: Máximo de resultados
            category: Categoría (technology, science, business, etc.)
            
        Returns:
            Lista de noticias recopiladas
        """
        if not self.api_key:
            print("❌ No se puede recopilar sin API key")
            return []
        
        print(f"📡 Recopilando desde NewsData.io (query: '{query}')...")
        
        try:
            news = self._fetch_articles(query, language, max_results, category)
            print(f"  ✅ NewsData.io: {len(news)} noticias")
            return news
        except Exception as e:
            print(f"  ❌ Error en NewsData.io: {str(e)}")
            return []
    
    def _fetch_articles(
        self,
        query: str,
        language: str,
        max_results: int,
        category: str
    ) -> List[Dict]:
        """
        Obtiene artículos de NewsData.io API.
        
        Args:
            query: Término de búsqueda
            language: Código de idioma
            max_results: Máximo de resultados
            category: Categoría opcional
            
        Returns:
            Lista de noticias
        """
        params = {
            'apikey': self.api_key,
            'q': query,
            'language': language,
            'size': min(max_results, 10)  # Max 10 en plan free
        }
        
        if category:
            params['category'] = category
        
        response = requests.get(self.BASE_URL, params=params, timeout=10)
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code} - {response.text}")
        
        data = response.json()
        
        if data.get('status') != 'success':
            raise Exception(f"API error: {data.get('results', {}).get('message', 'Unknown error')}")
        
        results = data.get('results', [])
        news = []
        
        for article in results:
            # Parsear fecha
            published = None
            if article.get('pubDate'):
                try:
                    published = datetime.fromisoformat(
                        article['pubDate'].replace('Z', '+00:00')
                    )
                except:
                    published = None
            
            # Extraer información relevante
            news_item = {
                'title': article.get('title', ''),
                'link': article.get('link', ''),
                'summary': article.get('description', ''),
                'content': article.get('content', '')[:500] if article.get('content') else '',
                'published': published.isoformat() if published else None,
                'source': article.get('source_id', 'NewsData.io'),
                'author': ', '.join(article.get('creator', [])) if article.get('creator') else '',
                'category': ', '.join(article.get('category', [])) if article.get('category') else 'tech',
                'collected_at': datetime.now().isoformat(),
                'image_url': article.get('image_url', ''),
                'collector': 'newsdata',
                'language': article.get('language', language)
            }
            
            news.append(news_item)
        
        return news
    
    def collect_multiple_queries(
        self,
        queries: List[Dict],
        max_results_per_query: int = 10
    ) -> List[Dict]:
        """
        Recopila noticias de múltiples queries.
        
        Args:
            queries: Lista de dicts con 'query', 'language', 'category' (opcional)
            max_results_per_query: Máximo de resultados por query
            
        Returns:
            Lista de todas las noticias
        """
        all_news = []
        
        for query_config in queries:
            try:
                news = self.collect(
                    query=query_config.get('query', 'technology'),
                    language=query_config.get('language', 'en'),
                    max_results=max_results_per_query,
                    category=query_config.get('category')
                )
                all_news.extend(news)
            except Exception as e:
                print(f"❌ Error en query '{query_config.get('query')}': {str(e)}")
        
        return all_news
    
    def save_to_file(self, news: List[Dict], output_path: str = "data/newsdata.json"):
        """
        Guarda las noticias recopiladas en un archivo JSON.
        
        Args:
            news: Lista de noticias a guardar
            output_path: Ruta del archivo de salida
        """
        import json
        
        output_file = Path(output_path)
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(news, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Noticias de NewsData.io guardadas en: {output_path}")


# Ejemplo de uso
if __name__ == "__main__":
    # Crear el recolector
    collector = NewsDataCollector()
    
    # Recopilar noticias de tecnología en inglés
    news = collector.collect(query="artificial intelligence", language="en", max_results=10)
    
    # O recopilar de múltiples queries
    # news = collector.collect_multiple_queries([
    #     {'query': 'inteligencia artificial', 'language': 'es'},
    #     {'query': 'tecnología', 'language': 'es'},
    #     {'query': 'startup', 'language': 'es'}
    # ])
    
    # Guardar en archivo
    if news:
        collector.save_to_file(news)
        
        # Mostrar las primeras 3 noticias
        print("\n📰 Primeras 3 noticias:")
        for i, item in enumerate(news[:3], 1):
            print(f"\n{i}. {item['title']}")
            print(f"   Fuente: {item['source']}")
            print(f"   Link: {item['link']}")
    else:
        print("\n⚠️  No se recopilaron noticias. Verifica tu API key.")
