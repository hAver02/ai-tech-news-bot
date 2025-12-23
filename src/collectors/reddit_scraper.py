"""
Reddit Scraper - Recopila posts de Reddit sin usar la API oficial

Usa el endpoint JSON público de Reddit (old.reddit.com)
NO requiere API keys ni autenticación.

Endpoint: https://old.reddit.com/r/subreddit/.json
"""

import requests
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict
import time


class RedditScraper:
    """Scraper de posts de Reddit usando JSON público."""
    
    BASE_URL = "https://old.reddit.com"
    
    def __init__(self):
        """Inicializa el scraper de Reddit."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; TechNewsBot/1.0)'
        }
    
    def collect(
        self,
        subreddit: str = 'technology',
        limit: int = 25,
        min_score: int = 50,
        time_filter: str = 'hot'
    ) -> List[Dict]:
        """
        Recopila posts de un subreddit.
        
        Args:
            subreddit: Nombre del subreddit (sin r/)
            limit: Máximo de posts a recopilar
            min_score: Puntuación mínima requerida
            time_filter: Filtro ('hot', 'new', 'top', 'rising')
            
        Returns:
            Lista de posts recopilados
        """
        print(f"📡 Scrapeando Reddit - r/{subreddit} ({time_filter})...")
        
        try:
            posts = self._fetch_posts(subreddit, limit, min_score, time_filter)
            print(f"  ✅ r/{subreddit}: {len(posts)} posts")
            return posts
        except Exception as e:
            print(f"  ❌ Error en r/{subreddit}: {str(e)}")
            return []
    
    def _fetch_posts(
        self,
        subreddit: str,
        limit: int,
        min_score: int,
        time_filter: str
    ) -> List[Dict]:
        """
        Obtiene posts de Reddit mediante JSON público.
        
        Args:
            subreddit: Nombre del subreddit
            limit: Límite de posts
            min_score: Score mínimo
            time_filter: Filtro de tiempo
            
        Returns:
            Lista de posts
        """
        # Construir URL
        if time_filter == 'hot':
            url = f"{self.BASE_URL}/r/{subreddit}/.json"
        else:
            url = f"{self.BASE_URL}/r/{subreddit}/{time_filter}/.json"
        
        params = {
            'limit': limit * 2  # Pedimos más para filtrar
        }
        
        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=10
        )
        
        if response.status_code != 200:
            raise Exception(f"HTTP error: {response.status_code}")
        
        data = response.json()
        
        if 'data' not in data or 'children' not in data['data']:
            raise Exception("Formato de respuesta inesperado")
        
        posts = []
        
        for child in data['data']['children']:
            post_data = child.get('data', {})
            
            # Filtrar stickied posts
            if post_data.get('stickied', False):
                continue
            
            # Filtrar por score
            score = post_data.get('score', 0)
            if score < min_score:
                continue
            
            # Parsear fecha
            published = None
            if post_data.get('created_utc'):
                published = datetime.fromtimestamp(
                    post_data['created_utc'],
                    tz=timezone.utc
                )
            
            # Extraer información relevante
            post = {
                'title': post_data.get('title', ''),
                'link': post_data.get('url', ''),
                'summary': post_data.get('selftext', '')[:500] if post_data.get('selftext') else '',
                'published': published.isoformat() if published else None,
                'source': f"Reddit - r/{subreddit}",
                'author': post_data.get('author', '[deleted]'),
                'score': score,
                'num_comments': post_data.get('num_comments', 0),
                'category': 'tech',
                'collected_at': datetime.now(timezone.utc).isoformat(),
                'collector': 'reddit_scraper',
                'reddit_id': post_data.get('id', ''),
                'permalink': f"https://reddit.com{post_data.get('permalink', '')}",
                'subreddit': subreddit
            }
            
            posts.append(post)
            
            if len(posts) >= limit:
                break
        
        return posts
    
    def collect_multiple_subreddits(
        self,
        subreddits: List[str] = None,
        limit_per_subreddit: int = 15,
        min_score: int = 50
    ) -> List[Dict]:
        """
        Recopila posts de múltiples subreddits.
        
        Args:
            subreddits: Lista de subreddits
            limit_per_subreddit: Límite por subreddit
            min_score: Score mínimo
            
        Returns:
            Lista de todos los posts
        """
        if subreddits is None:
            subreddits = [
                'technology',
                'programming',
                'Python',
                'javascript',
                'MachineLearning',
                'artificial',
                'startups'
            ]
        
        all_posts = []
        
        for subreddit in subreddits:
            try:
                posts = self.collect(
                    subreddit=subreddit,
                    limit=limit_per_subreddit,
                    min_score=min_score
                )
                all_posts.extend(posts)
                
                # Rate limiting - ser respetuoso
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Error en r/{subreddit}: {str(e)}")
        
        return all_posts
    
    def save_to_file(self, posts: List[Dict], output_path: str = "data/reddit_scraped.json"):
        """
        Guarda los posts recopilados en un archivo JSON.
        
        Args:
            posts: Lista de posts a guardar
            output_path: Ruta del archivo de salida
        """
        import json
        
        output_file = Path(output_path)
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Posts de Reddit guardados en: {output_path}")


# Ejemplo de uso
if __name__ == "__main__":
    # Crear el scraper
    scraper = RedditScraper()
    
    # Scrapear un subreddit
    posts = scraper.collect(
        subreddit='technology',
        limit=25,
        min_score=100,
        time_filter='hot'
    )
    
    # O scrapear múltiples subreddits
    # posts = scraper.collect_multiple_subreddits(
    #     subreddits=['technology', 'programming', 'Python'],
    #     limit_per_subreddit=10,
    #     min_score=50
    # )
    
    # Guardar en archivo
    if posts:
        scraper.save_to_file(posts)
        
        # Mostrar los primeros 5 posts
        print("\n📰 Primeros 5 posts:")
        for i, post in enumerate(posts[:5], 1):
            print(f"\n{i}. {post['title']}")
            print(f"   👍 {post['score']} upvotes | 💬 {post['num_comments']} comments")
            print(f"   📍 r/{post['subreddit']} by u/{post['author']}")
            print(f"   🔗 {post['link'][:80]}...")
    else:
        print("\n⚠️  No se scrapearon posts.")
