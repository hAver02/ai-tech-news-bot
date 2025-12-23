"""
News API Collector - Recopila noticias desde News API

News API te da acceso a miles de fuentes de noticias.
Plan gratuito: 100 requests por día.

Obtén tu API key gratis en: https://newsapi.org/register
"""

import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
import yaml
import os
from dotenv import load_dotenv


class NewsAPICollector:
    """Recolector de noticias desde News API."""
    
    BASE_URL = "https://newsapi.org/v2/everything"
    
    def __init__(self, config_path: str = "config/sources.yaml", api_key: str = None):
        """
        Inicializa el recolector de News API.
        
        Args:
            config_path: Ruta al archivo de configuración
            api_key: API key de News API (opcional, se carga de .env)
        """
        self.config_path = Path(config_path)
        self.queries = self._load_queries()
        
        # Cargar API key
        if api_key:
            self.api_key = api_key
        else:
            load_dotenv()
            self.api_key = os.getenv("NEWS_API_KEY")
            
        if not self.api_key:
            print("⚠️  No se encontró NEWS_API_KEY. Este collector no funcionará.")
            print("   Obtén una API key gratis en: https://newsapi.org/register")
    
    def _load_queries(self) -> List[Dict]:
        """Carga las queries de News API desde el archivo de configuración."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config.get('news_api_queries', [])
        except FileNotFoundError:
            print(f"⚠️  Archivo de configuración no encontrado: {self.config_path}")
            return []
    
    def collect(
        self,
        max_age_hours: int = 24,
        max_results_per_query: int = 10
    ) -> List[Dict]:
        """
        Recopila noticias de News API.
        
        Args:
            max_age_hours: Máxima antigüedad de las noticias en horas
            max_results_per_query: Máximo de resultados por query
            
        Returns:
            Lista de noticias recopiladas
        """
        if not self.api_key:
            print("❌ No se puede recopilar sin API key")
            return []
        
        all_news = []
        from_date = (datetime.now() - timedelta(hours=max_age_hours)).isoformat()
        
        print(f"📡 Recopilando desde News API ({len(self.queries)} queries)...")
        
        for query_config in self.queries:
            try:
                news = self._collect_from_query(
                    query_config,
                    from_date,
                    max_results_per_query
                )
                all_news.extend(news)
                print(f"  ✅ '{query_config['query']}': {len(news)} noticias")
            except Exception as e:
                print(f"  ❌ Error en query '{query_config['query']}': {str(e)}")
        
        print(f"\n📊 Total News API: {len(all_news)} noticias")
        return all_news
    
    def _collect_from_query(
        self,
        query_config: Dict,
        from_date: str,
        max_results: int
    ) -> List[Dict]:
        """
        Recopila noticias de una query específica.
        
        Args:
            query_config: Configuración de la query
            from_date: Fecha desde cuando buscar (ISO format)
            max_results: Máximo de resultados
            
        Returns:
            Lista de noticias de la query
        """
        params = {
            'q': query_config['query'],
            'language': query_config.get('language', 'en'),
            'sortBy': 'publishedAt',
            'from': from_date,
            'pageSize': max_results,
            'apiKey': self.api_key
        }
        
        response = requests.get(self.BASE_URL, params=params, timeout=10)
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code} - {response.text}")
        
        data = response.json()
        
        if data.get('status') != 'ok':
            raise Exception(f"API error: {data.get('message', 'Unknown error')}")
        
        articles = data.get('articles', [])
        news = []
        
        for article in articles:
            # Parsear fecha
            published = None
            if article.get('publishedAt'):
                try:
                    published = datetime.fromisoformat(
                        article['publishedAt'].replace('Z', '+00:00')
                    )
                except:
                    published = None
            
            # Extraer información relevante
            news_item = {
                'title': article.get('title', ''),
                'link': article.get('url', ''),
                'summary': article.get('description', ''),
                'content': article.get('content', ''),
                'published': published.isoformat() if published else None,
                'source': article.get('source', {}).get('name', 'News API'),
                'author': article.get('author', ''),
                'category': 'tech',  # Podemos categorizarlo mejor después
                'collected_at': datetime.now().isoformat(),
                'image_url': article.get('urlToImage', ''),
                'collector': 'news_api'
            }
            
            news.append(news_item)
        
        return news
    
    def save_to_file(self, news: List[Dict], output_path: str = "data/news_api.json"):
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
        
        print(f"💾 Noticias de News API guardadas en: {output_path}")


# Ejemplo de uso
if __name__ == "__main__":
    # Crear el recolector
    collector = NewsAPICollector()
    
    # Recopilar noticias de las últimas 24 horas
    news = collector.collect(max_age_hours=24, max_results_per_query=10)
    
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

