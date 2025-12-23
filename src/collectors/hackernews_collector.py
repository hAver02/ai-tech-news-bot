"""
Hacker News Collector - Recopila posts trending de Hacker News

Hacker News tiene una API pública GRATIS sin límites.
Es una de las mejores fuentes de noticias tech.

API Docs: https://github.com/HackerNews/API
"""

import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict


class HackerNewsCollector:
    """Recolector de noticias desde Hacker News API."""
    
    BASE_URL = "https://hacker-news.firebaseio.com/v0"
    
    def __init__(self):
        """Inicializa el recolector de Hacker News."""
        pass
    
    def collect(
        self,
        story_type: str = 'top',
        max_items: int = 30,
        min_score: int = 50
    ) -> List[Dict]:
        """
        Recopila historias de Hacker News.
        
        Args:
            story_type: Tipo de historias ('top', 'new', 'best', 'ask', 'show', 'job')
            max_items: Máximo de historias a recopilar
            min_score: Puntuación mínima requerida
            
        Returns:
            Lista de historias recopiladas
        """
        print(f"📡 Recopilando desde Hacker News ({story_type} stories)...")
        
        try:
            stories = self._fetch_stories(story_type, max_items, min_score)
            print(f"  ✅ Hacker News: {len(stories)} historias")
            return stories
        except Exception as e:
            print(f"  ❌ Error en Hacker News: {str(e)}")
            return []
    
    def _fetch_stories(
        self,
        story_type: str,
        max_items: int,
        min_score: int
    ) -> List[Dict]:
        """
        Obtiene historias de Hacker News API.
        
        Args:
            story_type: Tipo de historias
            max_items: Máximo de items
            min_score: Score mínimo
            
        Returns:
            Lista de historias
        """
        # Obtener IDs de las top stories
        stories_url = f"{self.BASE_URL}/{story_type}stories.json"
        response = requests.get(stories_url, timeout=10)
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code}")
        
        story_ids = response.json()[:max_items * 2]  # Pedimos más para filtrar
        
        stories = []
        
        for story_id in story_ids:
            if len(stories) >= max_items:
                break
            
            try:
                # Obtener detalles de cada historia
                item_url = f"{self.BASE_URL}/item/{story_id}.json"
                item_response = requests.get(item_url, timeout=5)
                
                if item_response.status_code != 200:
                    continue
                
                item = item_response.json()
                
                # Filtrar solo stories (no jobs, polls, etc.)
                if item.get('type') != 'story':
                    continue
                
                # Filtrar por score
                score = item.get('score', 0)
                if score < min_score:
                    continue
                
                # Parsear fecha
                published = None
                if item.get('time'):
                    published = datetime.fromtimestamp(item['time'])
                
                # Extraer información relevante
                story = {
                    'title': item.get('title', ''),
                    'link': item.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                    'summary': item.get('text', '')[:500] if item.get('text') else '',
                    'published': published.isoformat() if published else None,
                    'source': 'Hacker News',
                    'author': item.get('by', ''),
                    'score': score,
                    'num_comments': item.get('descendants', 0),
                    'category': 'tech',
                    'collected_at': datetime.now().isoformat(),
                    'collector': 'hackernews',
                    'hn_id': story_id,
                    'hn_url': f"https://news.ycombinator.com/item?id={story_id}"
                }
                
                stories.append(story)
                
            except Exception as e:
                print(f"  ⚠️  Error obteniendo item {story_id}: {str(e)}")
                continue
        
        return stories
    
    def collect_multiple_types(
        self,
        story_types: List[str] = None,
        max_items_per_type: int = 15
    ) -> List[Dict]:
        """
        Recopila historias de múltiples tipos.
        
        Args:
            story_types: Lista de tipos de historias
            max_items_per_type: Máximo de items por tipo
            
        Returns:
            Lista de todas las historias
        """
        if story_types is None:
            story_types = ['top', 'best']
        
        all_stories = []
        
        for story_type in story_types:
            try:
                stories = self.collect(
                    story_type=story_type,
                    max_items=max_items_per_type
                )
                all_stories.extend(stories)
            except Exception as e:
                print(f"❌ Error en tipo {story_type}: {str(e)}")
        
        return all_stories
    
    def save_to_file(self, stories: List[Dict], output_path: str = "data/hackernews.json"):
        """
        Guarda las historias recopiladas en un archivo JSON.
        
        Args:
            stories: Lista de historias a guardar
            output_path: Ruta del archivo de salida
        """
        import json
        
        output_file = Path(output_path)
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(stories, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Historias de Hacker News guardadas en: {output_path}")


# Ejemplo de uso
if __name__ == "__main__":
    # Crear el recolector
    collector = HackerNewsCollector()
    
    # Recopilar top stories
    stories = collector.collect(story_type='top', max_items=30, min_score=50)
    
    # O recopilar de múltiples tipos
    # stories = collector.collect_multiple_types(
    #     story_types=['top', 'best', 'show'],
    #     max_items_per_type=10
    # )
    
    # Guardar en archivo
    if stories:
        collector.save_to_file(stories)
        
        # Mostrar las primeras 5 historias
        print("\n📰 Primeras 5 historias:")
        for i, story in enumerate(stories[:5], 1):
            print(f"\n{i}. {story['title']}")
            print(f"   👍 {story['score']} points | 💬 {story['num_comments']} comments")
            print(f"   👤 {story['author']}")
            print(f"   🔗 {story['link']}")
    else:
        print("\n⚠️  No se recopilaron historias.")
