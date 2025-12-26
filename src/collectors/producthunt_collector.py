"""
Product Hunt Collector - Lanzamientos tech del día

Product Hunt API proporciona:
- Productos lanzados HOY
- Solo tech/startups
- 100% GRATIS
- Alta calidad (curateado)

Documentación: https://api.producthunt.com/v2/docs
"""

import os
import requests
from typing import List, Dict
from datetime import datetime


class ProductHuntCollector:
    """
    Recopilador de lanzamientos de Product Hunt.
    
    Características:
    - Productos del día
    - Solo tech
    - 100% gratuito
    """
    
    def __init__(self, api_key: str = None):
        """
        Inicializa el collector de Product Hunt.
        
        Args:
            api_key: API key de PH (o usa PRODUCTHUNT_API_KEY del .env)
        """
        self.api_key = api_key or os.getenv("PRODUCTHUNT_API_KEY")
        if not self.api_key:
            print("⚠️  No se encontró PRODUCTHUNT_API_KEY. Este collector no funcionará.")
        
        self.base_url = "https://api.producthunt.com/v2/api/graphql"
    
    def collect_today(self, max_results: int = 20) -> List[Dict]:
        """
        Recopila productos lanzados hoy.
        
        Args:
            max_results: Máximo productos
            
        Returns:
            Lista de productos/noticias
        """
        if not self.api_key:
            return []
        
        print(f"\n🚀 Product Hunt: productos del día")
        print(f"   Max resultados: {max_results}")
        
        query = '''
        query {
          posts(order: NEWEST, first: %d) {
            edges {
              node {
                id
                name
                tagline
                description
                votesCount
                commentsCount
                createdAt
                url
                website
                topics {
                  edges {
                    node {
                      name
                    }
                  }
                }
              }
            }
          }
        }
        ''' % max_results
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json={'query': query},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            posts = data.get('data', {}).get('posts', {}).get('edges', [])
            print(f"   ✅ {len(posts)} productos")
            
            news_list = []
            for edge in posts:
                node = edge.get('node', {})
                
                # Extraer topics
                topics = [
                    t.get('node', {}).get('name', '')
                    for t in node.get('topics', {}).get('edges', [])
                ]
                
                news_list.append({
                    'title': f"🚀 {node.get('name', '')}: {node.get('tagline', '')}",
                    'link': node.get('url', ''),
                    'summary': node.get('description', '')[:500],
                    'full_content': node.get('description', ''),
                    'published': node.get('createdAt', datetime.now().isoformat()),
                    'source': 'Product Hunt',
                    'score': node.get('votesCount', 0),
                    'comments': node.get('commentsCount', 0),
                    'topics': topics,
                    'website': node.get('website', '')
                })
            
            return news_list
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error en Product Hunt: {str(e)}")
            return []
        except Exception as e:
            print(f"   ❌ Error parseando Product Hunt: {str(e)}")
            return []


# Ejemplo de uso
if __name__ == "__main__":
    collector = ProductHuntCollector()
    
    products = collector.collect_today(max_results=10)
    
    print(f"\n📰 Total: {len(products)} productos")
    for p in products[:3]:
        print(f"   - [{p['score']} votos] {p['title']}")
