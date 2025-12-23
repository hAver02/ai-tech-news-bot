"""
Reddit Collector - Recopila posts trending de subreddits tech

Reddit API es gratis y no requiere aprobación especial.
Obtén tus credenciales en: https://www.reddit.com/prefs/apps
"""

import praw
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict
import yaml
import os
from dotenv import load_dotenv


class RedditCollector:
    """Recolector de posts de Reddit."""
    
    def __init__(self, config_path: str = "config/sources.yaml"):
        """
        Inicializa el recolector de Reddit.
        
        Args:
            config_path: Ruta al archivo de configuración
        """
        self.config_path = Path(config_path)
        self.subreddits = self._load_subreddits()
        
        # Cargar credenciales
        load_dotenv()
        client_id = os.getenv("REDDIT_CLIENT_ID")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        user_agent = os.getenv("REDDIT_USER_AGENT", "TechNewsBot/1.0")
        
        if not client_id or not client_secret:
            print("⚠️  No se encontraron credenciales de Reddit.")
            print("   Este collector es opcional. Para usarlo:")
            print("   1. Crea una app en: https://www.reddit.com/prefs/apps")
            print("   2. Agrega REDDIT_CLIENT_ID y REDDIT_CLIENT_SECRET a .env")
            self.reddit = None
        else:
            try:
                self.reddit = praw.Reddit(
                    client_id=client_id,
                    client_secret=client_secret,
                    user_agent=user_agent
                )
                # Test de conexión
                self.reddit.user.me()
            except Exception as e:
                print(f"⚠️  Error conectando con Reddit: {str(e)}")
                self.reddit = None
    
    def _load_subreddits(self) -> List[Dict]:
        """Carga la lista de subreddits desde el archivo de configuración."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config.get('reddit_sources', [])
        except FileNotFoundError:
            print(f"⚠️  Archivo de configuración no encontrado: {self.config_path}")
            return []
    
    def collect(
        self,
        time_filter: str = 'day',
        min_score: int = 50
    ) -> List[Dict]:
        """
        Recopila posts trending de subreddits configurados.
        
        Args:
            time_filter: Filtro de tiempo ('hour', 'day', 'week', 'month')
            min_score: Puntaje mínimo de upvotes
            
        Returns:
            Lista de posts recopilados
        """
        if not self.reddit:
            print("❌ Reddit no está configurado. Saltando...")
            return []
        
        all_posts = []
        
        print(f"📡 Recopilando desde Reddit ({len(self.subreddits)} subreddits)...")
        
        for sub_config in self.subreddits:
            try:
                posts = self._collect_from_subreddit(
                    sub_config,
                    time_filter,
                    min_score
                )
                all_posts.extend(posts)
                print(f"  ✅ r/{sub_config['subreddit']}: {len(posts)} posts")
            except Exception as e:
                print(f"  ❌ Error en r/{sub_config['subreddit']}: {str(e)}")
        
        print(f"\n📊 Total Reddit: {len(all_posts)} posts")
        return all_posts
    
    def _collect_from_subreddit(
        self,
        sub_config: Dict,
        time_filter: str,
        min_score: int
    ) -> List[Dict]:
        """
        Recopila posts de un subreddit específico.
        
        Args:
            sub_config: Configuración del subreddit
            time_filter: Filtro de tiempo
            min_score: Puntaje mínimo
            
        Returns:
            Lista de posts del subreddit
        """
        subreddit = self.reddit.subreddit(sub_config['subreddit'])
        limit = sub_config.get('limit', 10)
        
        posts = []
        
        # Obtener posts hot/trending
        for submission in subreddit.hot(limit=limit * 2):  # Pedimos más para filtrar
            # Filtrar por score
            if submission.score < min_score:
                continue
            
            # Filtrar stickied posts y anuncios
            if submission.stickied or submission.distinguished:
                continue
            
            # Parsear fecha
            published = datetime.fromtimestamp(
                submission.created_utc,
                tz=timezone.utc
            )
            
            # Extraer información relevante
            post = {
                'title': submission.title,
                'link': submission.url,
                'summary': submission.selftext[:500] if submission.selftext else '',
                'published': published.isoformat(),
                'source': f"Reddit - r/{sub_config['subreddit']}",
                'author': str(submission.author) if submission.author else '[deleted]',
                'score': submission.score,
                'num_comments': submission.num_comments,
                'category': 'tech',
                'collected_at': datetime.now(timezone.utc).isoformat(),
                'collector': 'reddit',
                'reddit_id': submission.id,
                'permalink': f"https://reddit.com{submission.permalink}"
            }
            
            posts.append(post)
            
            if len(posts) >= limit:
                break
        
        return posts
    
    def save_to_file(self, posts: List[Dict], output_path: str = "data/reddit.json"):
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
    # Crear el recolector
    collector = RedditCollector()
    
    # Recopilar posts del día con mínimo 50 upvotes
    posts = collector.collect(time_filter='day', min_score=50)
    
    # Guardar en archivo
    if posts:
        collector.save_to_file(posts)
        
        # Mostrar los primeros 3 posts
        print("\n📰 Primeros 3 posts:")
        for i, post in enumerate(posts[:3], 1):
            print(f"\n{i}. {post['title']}")
            print(f"   👍 {post['score']} upvotes | 💬 {post['num_comments']} comments")
            print(f"   📍 {post['source']}")
            print(f"   🔗 {post['link']}")
    else:
        print("\n⚠️  No se recopilaron posts. Verifica tu configuración.")

