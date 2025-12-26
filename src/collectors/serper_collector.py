"""
Serper API Collector - Google Search en tiempo real

Serper.dev proporciona acceso a Google Search con:
- 2,500 búsquedas GRATIS/mes
- Filtros temporales (última hora, día, semana)
- Resultados en tiempo real
- Muy barato después: $0.005 por búsqueda

Documentación: https://serper.dev/docs
"""

import os
import requests
from typing import List, Dict
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class SerperCollector:
    """
    Recopilador usando Serper (Google Search API).
    
    Características:
    - Google Search en tiempo real
    - Filtros temporales precisos
    - 2,500 búsquedas gratis/mes
    """
    
    def __init__(self, api_key: str = None):
        """
        Inicializa el collector de Serper.
        
        Args:
            api_key: API key de Serper (o usa SERPER_API_KEY del .env)
        """
        self.api_key = api_key or os.getenv("SERPER_API_KEY")
        if not self.api_key:
            print("⚠️  No se encontró SERPER_API_KEY. Este collector no funcionará.")
        
        self.base_url = "https://google.serper.dev/search"
    
    def search(
        self,
        query: str,
        num_results: int = 10,
        time_filter: str = "d"  # h=hour, d=day, w=week, m=month
    ) -> List[Dict]:
        """
        Busca en Google vía Serper.
        
        Args:
            query: Búsqueda
            num_results: Número de resultados
            time_filter: Filtro temporal
                - "h" = última hora
                - "d" = último día
                - "w" = última semana
                - "m" = último mes
                
        Returns:
            Lista de noticias
        """
        if not self.api_key:
            return []
        
        print(f"\n🔍 Serper (Google): {query}")
        print(f"   Filtro temporal: {time_filter} | Resultados: {num_results}")
        
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'q': query,
            'num': num_results,
            'tbs': f'qdr:{time_filter}'  # qdr = query date restrict
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            # Extraer resultados orgánicos
            organic = data.get('organic', [])
            print(f"   ✅ {len(organic)} resultados")
            
            news_list = []
            for item in organic:
                news_list.append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'summary': item.get('snippet', ''),
                    'full_content': item.get('snippet', ''),
                    'published': item.get('date', datetime.now().isoformat()),
                    'source': 'Serper (Google)',
                    'position': item.get('position', 0)
                })
            
            return news_list
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error en Serper: {str(e)}")
            return []
    
    def collect_multiple_queries(
        self,
        queries: List[str],
        num_results_per_query: int = 10,
        time_filter: str = "d"
    ) -> List[Dict]:
        """
        Ejecuta múltiples búsquedas.
        
        Args:
            queries: Lista de búsquedas
            num_results_per_query: Resultados por búsqueda
            time_filter: Filtro temporal
            
        Returns:
            Lista combinada de noticias
        """
        all_news = []
        
        for query in queries:
            news = self.search(
                query=query,
                num_results=num_results_per_query,
                time_filter=time_filter
            )
            all_news.extend(news)
        
        return all_news


# Ejemplo de uso
if __name__ == "__main__":
    collector = SerperCollector()
    
    # Buscar noticias de la última hora
    news = collector.collect_multiple_queries(
        queries=[
            "Cursor IDE AI coding",
            "OpenAI latest news",
            "TypeScript new release",
            "Nvidia AI chips"
        ],
        num_results_per_query=5,
        time_filter="h"  # Última HORA
    )
    
    print(f"\n📰 Total: {len(news)} noticias")
    for n in news[:3]:
        print(f"   - {n['title']}")
