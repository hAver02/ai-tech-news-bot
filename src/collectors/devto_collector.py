"""
Dev.to Collector - Recopila artículos de Dev.to

Dev.to tiene una API pública GRATIS sin límites y sin autenticación.
Excelente fuente de tutoriales y noticias de desarrollo.

API Docs: https://developers.forem.com/api
"""

import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict


class DevToCollector:
    """Recolector de artículos desde Dev.to API."""
    
    BASE_URL = "https://dev.to/api"
    
    def __init__(self):
        """Inicializa el recolector de Dev.to."""
        pass
    
    def collect(
        self,
        tag: str = None,
        top: int = None,
        per_page: int = 30,
        min_reactions: int = 10
    ) -> List[Dict]:
        """
        Recopila artículos de Dev.to.
        
        Args:
            tag: Filtrar por tag (python, javascript, react, etc.)
            top: Filtrar por top (número de días: 7, 30, etc.)
            per_page: Número de artículos por página (max 1000)
            min_reactions: Mínimo de reacciones (likes)
            
        Returns:
            Lista de artículos recopilados
        """
        print(f"📡 Recopilando desde Dev.to (tag: {tag or 'all'})...")
        
        try:
            articles = self._fetch_articles(tag, top, per_page, min_reactions)
            print(f"  ✅ Dev.to: {len(articles)} artículos")
            return articles
        except Exception as e:
            print(f"  ❌ Error en Dev.to: {str(e)}")
            return []
    
    def _fetch_articles(
        self,
        tag: str,
        top: int,
        per_page: int,
        min_reactions: int
    ) -> List[Dict]:
        """
        Obtiene artículos de Dev.to API.
        
        Args:
            tag: Tag para filtrar
            top: Top days
            per_page: Artículos por página
            min_reactions: Reacciones mínimas
            
        Returns:
            Lista de artículos
        """
        url = f"{self.BASE_URL}/articles"
        
        params = {
            'per_page': min(per_page, 1000)
        }
        
        if tag:
            params['tag'] = tag
        
        if top:
            params['top'] = top
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code}")
        
        articles_data = response.json()
        
        articles = []
        
        for article in articles_data:
            # Filtrar por reacciones
            reactions = article.get('public_reactions_count', 0)
            if reactions < min_reactions:
                continue
            
            # Parsear fecha
            published = None
            if article.get('published_at'):
                try:
                    published = datetime.fromisoformat(
                        article['published_at'].replace('Z', '+00:00')
                    )
                except:
                    published = None
            
            # Extraer información relevante
            article_item = {
                'title': article.get('title', ''),
                'link': article.get('url', ''),
                'summary': article.get('description', ''),
                'published': published.isoformat() if published else None,
                'source': 'Dev.to',
                'author': article.get('user', {}).get('name', ''),
                'author_username': article.get('user', {}).get('username', ''),
                'reactions': reactions,
                'comments': article.get('comments_count', 0),
                'tags': article.get('tag_list', []),
                'category': 'dev',
                'collected_at': datetime.now().isoformat(),
                'collector': 'devto',
                'cover_image': article.get('cover_image', ''),
                'reading_time': article.get('reading_time_minutes', 0)
            }
            
            articles.append(article_item)
        
        return articles
    
    def collect_multiple_tags(
        self,
        tags: List[str] = None,
        per_page_per_tag: int = 15,
        min_reactions: int = 10
    ) -> List[Dict]:
        """
        Recopila artículos de múltiples tags.
        
        Args:
            tags: Lista de tags
            per_page_per_tag: Artículos por tag
            min_reactions: Reacciones mínimas
            
        Returns:
            Lista de todos los artículos
        """
        if tags is None:
            tags = [
                'python',
                'javascript',
                'react',
                'webdev',
                'ai',
                'machinelearning',
                'devops',
                'opensource'
            ]
        
        all_articles = []
        
        for tag in tags:
            try:
                articles = self.collect(
                    tag=tag,
                    per_page=per_page_per_tag,
                    min_reactions=min_reactions
                )
                all_articles.extend(articles)
            except Exception as e:
                print(f"❌ Error en tag '{tag}': {str(e)}")
        
        return all_articles
    
    def collect_top_this_week(
        self,
        per_page: int = 30,
        min_reactions: int = 50
    ) -> List[Dict]:
        """
        Recopila los artículos top de esta semana.
        
        Args:
            per_page: Número de artículos
            min_reactions: Reacciones mínimas
            
        Returns:
            Lista de artículos top
        """
        print("📡 Recopilando top articles de esta semana desde Dev.to...")
        
        return self.collect(
            top=7,  # Top de los últimos 7 días
            per_page=per_page,
            min_reactions=min_reactions
        )
    
    def save_to_file(self, articles: List[Dict], output_path: str = "data/devto.json"):
        """
        Guarda los artículos recopilados en un archivo JSON.
        
        Args:
            articles: Lista de artículos a guardar
            output_path: Ruta del archivo de salida
        """
        import json
        
        output_file = Path(output_path)
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Artículos de Dev.to guardados en: {output_path}")


# Ejemplo de uso
if __name__ == "__main__":
    # Crear el recolector
    collector = DevToCollector()
    
    # Recopilar artículos recientes sin filtro de reactions
    articles = collector.collect(tag='python', per_page=30, min_reactions=0)
    
    # O recopilar top de la semana
    # articles = collector.collect_top_this_week(per_page=30, min_reactions=50)
    
    # O recopilar de múltiples tags
    # articles = collector.collect_multiple_tags(
    #     tags=['python', 'javascript', 'ai', 'react'],
    #     per_page_per_tag=10
    # )
    
    # Guardar en archivo
    if articles:
        collector.save_to_file(articles)
        
        # Mostrar los primeros 5 artículos
        print("\n📰 Primeros 5 artículos:")
        for i, article in enumerate(articles[:5], 1):
            print(f"\n{i}. {article['title']}")
            print(f"   ❤️  {article['reactions']} reactions | 💬 {article['comments']} comments")
            print(f"   👤 {article['author']} (@{article['author_username']})")
            print(f"   🏷️  Tags: {', '.join(article['tags'][:3])}")
            print(f"   📚 {article['reading_time']} min read")
            print(f"   🔗 {article['link']}")
    else:
        print("\n⚠️  No se recopilaron artículos.")
