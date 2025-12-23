"""
The Guardian API Collector - Recopila noticias desde The Guardian

The Guardian ofrece una API GRATIS con 5000 requests por día.
Es una de las APIs más generosas disponibles.

Obtén tu API key gratis en: https://open-platform.theguardian.com/access/
"""

import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
import os
from dotenv import load_dotenv


class GuardianCollector:
    """Recolector de noticias desde The Guardian API."""
    
    BASE_URL = "https://content.guardianapis.com/search"
    
    def __init__(self, api_key: str = None):
        """
        Inicializa el recolector de The Guardian.
        
        Args:
            api_key: API key de The Guardian (opcional, se carga de .env)
        """
        if api_key:
            self.api_key = api_key
        else:
            load_dotenv()
            self.api_key = os.getenv("GUARDIAN_API_KEY")
            
        if not self.api_key:
            print("⚠️  No se encontró GUARDIAN_API_KEY. Este collector no funcionará.")
            print("   Obtén una API key GRATIS (5000 requests/día) en:")
            print("   https://open-platform.theguardian.com/access/")
    
    def collect(
        self,
        max_age_hours: int = 24,
        max_results: int = 50,
        section: str = "technology"
    ) -> List[Dict]:
        """
        Recopila noticias de The Guardian.
        
        Args:
            max_age_hours: Máxima antigüedad de las noticias en horas
            max_results: Máximo de resultados
            section: Sección del periódico (technology, science, business, etc.)
            
        Returns:
            Lista de noticias recopiladas
        """
        if not self.api_key:
            print("❌ No se puede recopilar sin API key")
            return []
        
        all_news = []
        from_date = (datetime.now() - timedelta(hours=max_age_hours)).strftime('%Y-%m-%d')
        
        print(f"📡 Recopilando desde The Guardian (sección: {section})...")
        
        try:
            news = self._fetch_articles(from_date, max_results, section)
            all_news.extend(news)
            print(f"  ✅ The Guardian: {len(news)} noticias")
        except Exception as e:
            print(f"  ❌ Error en The Guardian: {str(e)}")
        
        print(f"\n📊 Total The Guardian: {len(all_news)} noticias")
        return all_news
    
    def _fetch_articles(
        self,
        from_date: str,
        max_results: int,
        section: str
    ) -> List[Dict]:
        """
        Obtiene artículos de The Guardian API.
        
        Args:
            from_date: Fecha desde cuando buscar (YYYY-MM-DD)
            max_results: Máximo de resultados
            section: Sección del periódico
            
        Returns:
            Lista de noticias
        """
        params = {
            'section': section,
            'from-date': from_date,
            'page-size': min(max_results, 50),  # Max 50 por request
            'show-fields': 'headline,trailText,body,thumbnail,byline',
            'show-tags': 'keyword',
            'order-by': 'newest',
            'api-key': self.api_key
        }
        
        response = requests.get(self.BASE_URL, params=params, timeout=10)
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code} - {response.text}")
        
        data = response.json()
        
        if data.get('response', {}).get('status') != 'ok':
            raise Exception(f"API error: {data.get('message', 'Unknown error')}")
        
        results = data.get('response', {}).get('results', [])
        news = []
        
        for article in results:
            # Parsear fecha
            published = None
            if article.get('webPublicationDate'):
                try:
                    published = datetime.fromisoformat(
                        article['webPublicationDate'].replace('Z', '+00:00')
                    )
                except:
                    published = None
            
            fields = article.get('fields', {})
            
            # Extraer información relevante
            news_item = {
                'title': fields.get('headline', article.get('webTitle', '')),
                'link': article.get('webUrl', ''),
                'summary': fields.get('trailText', ''),
                'content': fields.get('body', '')[:500],  # Primeros 500 chars
                'published': published.isoformat() if published else None,
                'source': 'The Guardian',
                'author': fields.get('byline', ''),
                'category': article.get('sectionName', section),
                'collected_at': datetime.now().isoformat(),
                'image_url': fields.get('thumbnail', ''),
                'collector': 'guardian',
                'section': article.get('sectionId', '')
            }
            
            news.append(news_item)
        
        return news
    
    def collect_multiple_sections(
        self,
        sections: List[str] = None,
        max_age_hours: int = 24,
        max_results_per_section: int = 20
    ) -> List[Dict]:
        """
        Recopila noticias de múltiples secciones.
        
        Args:
            sections: Lista de secciones (None = default sections)
            max_age_hours: Máxima antigüedad en horas
            max_results_per_section: Máximo de resultados por sección
            
        Returns:
            Lista de todas las noticias
        """
        if sections is None:
            sections = ['technology', 'science', 'business', 'media']
        
        all_news = []
        
        for section in sections:
            try:
                news = self.collect(
                    max_age_hours=max_age_hours,
                    max_results=max_results_per_section,
                    section=section
                )
                all_news.extend(news)
            except Exception as e:
                print(f"❌ Error en sección {section}: {str(e)}")
        
        return all_news
    
    def save_to_file(self, news: List[Dict], output_path: str = "data/guardian.json"):
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
        
        print(f"💾 Noticias de The Guardian guardadas en: {output_path}")


# Ejemplo de uso
if __name__ == "__main__":
    # Crear el recolector
    collector = GuardianCollector()
    
    # Recopilar noticias de tecnología
    news = collector.collect(max_age_hours=24, max_results=30, section='technology')
    
    # O recopilar de múltiples secciones
    # news = collector.collect_multiple_sections(
    #     sections=['technology', 'science', 'business'],
    #     max_results_per_section=15
    # )
    
    # Guardar en archivo
    if news:
        collector.save_to_file(news)
        
        # Mostrar las primeras 3 noticias
        print("\n📰 Primeras 3 noticias:")
        for i, item in enumerate(news[:3], 1):
            print(f"\n{i}. {item['title']}")
            print(f"   Fuente: {item['source']}")
            print(f"   Sección: {item['category']}")
            print(f"   Link: {item['link']}")
    else:
        print("\n⚠️  No se recopilaron noticias. Verifica tu API key.")
