"""
Tweet Generator - Genera tweets a partir de noticias

Este módulo toma noticias y las convierte en tweets atractivos.
Puedes usar templates simples o integrar IA (OpenAI) para hacerlo más sofisticado.
"""

import json
import random
from pathlib import Path
from typing import List, Dict
from datetime import datetime


class TweetGenerator:
    """Generador de tweets a partir de noticias."""
    
    # Templates para generar tweets (puedes agregar más!)
    TEMPLATES = [
        "🚀 {title}\n\n{link}",
        "💡 {title}\n\n👉 {link}",
        "🔥 Noticia tech: {title}\n\nMás info: {link}",
        "⚡ {title}\n\n🔗 {link}",
        "📢 {title}\n\nLee más: {link}",
        "🎯 Te puede interesar:\n{title}\n\n{link}",
    ]
    
    # Emojis para categorías
    CATEGORY_EMOJIS = {
        'ai': '🤖',
        'startup': '🚀',
        'tech': '💻',
        'programming': '👨‍💻',
        'security': '🔒',
        'mobile': '📱',
        'web': '🌐',
        'data': '📊',
        'cloud': '☁️',
    }
    
    def __init__(self, news_file: str = "data/news.json"):
        """
        Inicializa el generador de tweets.
        
        Args:
            news_file: Ruta al archivo con las noticias
        """
        self.news_file = Path(news_file)
        self.max_tweet_length = 280  # Límite de Twitter
    
    def load_news(self) -> List[Dict]:
        """Carga las noticias desde el archivo JSON."""
        if not self.news_file.exists():
            print(f"⚠️  No se encontró el archivo de noticias: {self.news_file}")
            return []
        
        with open(self.news_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate(self, limit: int = 10) -> List[Dict]:
        """
        Genera tweets a partir de las noticias disponibles.
        
        Args:
            limit: Número máximo de tweets a generar
            
        Returns:
            Lista de tweets generados
        """
        news = self.load_news()
        
        if not news:
            print("⚠️  No hay noticias disponibles para generar tweets.")
            return []
        
        print(f"🤖 Generando hasta {limit} tweets desde {len(news)} noticias...")
        
        tweets = []
        for news_item in news[:limit]:
            try:
                tweet = self._generate_single_tweet(news_item)
                if tweet:
                    tweets.append(tweet)
            except Exception as e:
                print(f"❌ Error generando tweet: {str(e)}")
        
        print(f"✅ {len(tweets)} tweets generados exitosamente!")
        return tweets
    
    def _generate_single_tweet(self, news_item: Dict) -> Dict:
        """
        Genera un solo tweet a partir de una noticia.
        
        Args:
            news_item: Diccionario con la información de la noticia
            
        Returns:
            Diccionario con el tweet generado
        """
        # Seleccionar template aleatorio
        template = random.choice(self.TEMPLATES)
        
        # Acortar título si es muy largo
        title = self._shorten_title(news_item['title'])
        
        # Generar el texto del tweet
        tweet_text = template.format(
            title=title,
            link=news_item['link']
        )
        
        # Verificar longitud
        if len(tweet_text) > self.max_tweet_length:
            tweet_text = self._truncate_tweet(tweet_text)
        
        return {
            'text': tweet_text,
            'source': news_item['source'],
            'original_title': news_item['title'],
            'link': news_item['link'],
            'category': news_item.get('category', 'tech'),
            'generated_at': datetime.now().isoformat(),
            'published': False  # Marcar como no publicado
        }
    
    def _shorten_title(self, title: str, max_length: int = 180) -> str:
        """
        Acorta el título si es muy largo.
        
        Args:
            title: Título original
            max_length: Longitud máxima
            
        Returns:
            Título acortado
        """
        if len(title) <= max_length:
            return title
        
        # Cortar en el último espacio antes del límite
        shortened = title[:max_length].rsplit(' ', 1)[0]
        return shortened + "..."
    
    def _truncate_tweet(self, tweet: str) -> str:
        """
        Trunca un tweet que es muy largo.
        
        Args:
            tweet: Tweet original
            
        Returns:
            Tweet truncado
        """
        # Encontrar el link (generalmente al final)
        parts = tweet.split('\n')
        link = parts[-1] if parts[-1].startswith('http') else ''
        
        # Calcular espacio disponible para el texto
        available = self.max_tweet_length - len(link) - 5  # 5 para espacios y "..."
        
        text = ' '.join(parts[:-1]) if link else tweet
        text = text[:available] + "..."
        
        return f"{text}\n{link}" if link else text
    
    def save_tweets(self, tweets: List[Dict], output_path: str = "data/tweets.json"):
        """
        Guarda los tweets generados en un archivo JSON.
        
        Args:
            tweets: Lista de tweets a guardar
            output_path: Ruta del archivo de salida
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(tweets, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Tweets guardados en: {output_path}")


# Ejemplo de uso
if __name__ == "__main__":
    # Crear el generador
    generator = TweetGenerator()
    
    # Generar tweets
    tweets = generator.generate(limit=10)
    
    # Guardar tweets
    if tweets:
        generator.save_tweets(tweets)
        
        # Mostrar los tweets generados
        print("\n📝 Tweets generados:")
        for i, tweet in enumerate(tweets, 1):
            print(f"\n{i}. {tweet['text']}")
            print(f"   Caracteres: {len(tweet['text'])}/280")

