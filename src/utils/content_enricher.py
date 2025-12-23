"""
Content Enricher - Enriquece noticias con contexto adicional

Extrae el contenido completo del artículo, comentarios relevantes,
y genera metadata adicional para mejorar la selección y generación de tweets.
"""

import requests
from bs4 import BeautifulSoup
from pathlib import Path
from typing import Dict, List, Optional
import time
from datetime import datetime


class ContentEnricher:
    """Enriquece noticias con contexto adicional."""
    
    def __init__(self):
        """Inicializa el enriquecedor de contenido."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
    
    def enrich_news(self, news_item: Dict) -> Dict:
        """
        Enriquece una noticia con contexto adicional.
        
        Args:
            news_item: Noticia a enriquecer
            
        Returns:
            Noticia enriquecida con contexto adicional
        """
        enriched = news_item.copy()
        
        print(f"🔍 Enriqueciendo: {news_item.get('title', '')[:60]}...")
        
        try:
            # 1. Extraer contenido completo del artículo
            article_content = self._extract_article_content(news_item.get('link', ''))
            if article_content:
                enriched['full_content'] = article_content
                enriched['content_length'] = len(article_content)
            
            # 2. Extraer comentarios si viene de HN o Reddit
            comments = self._extract_comments(news_item)
            if comments:
                enriched['top_comments'] = comments
                enriched['num_quality_comments'] = len(comments)
            
            # 3. Extraer keywords del contenido
            if article_content:
                keywords = self._extract_keywords(article_content)
                enriched['extracted_keywords'] = keywords
            
            # 4. Calcular score de engagement
            engagement_score = self._calculate_engagement_score(news_item)
            enriched['engagement_score'] = engagement_score
            
            # 5. Metadata de enriquecimiento
            enriched['enriched_at'] = datetime.now().isoformat()
            enriched['enrichment_status'] = 'success'
            
            print(f"   ✅ Enriquecida exitosamente")
            
        except Exception as e:
            print(f"   ⚠️  Error enriqueciendo: {str(e)}")
            enriched['enrichment_status'] = 'partial'
            enriched['enrichment_error'] = str(e)
        
        return enriched
    
    def _extract_article_content(self, url: str) -> Optional[str]:
        """
        Extrae el contenido completo de un artículo.
        
        Args:
            url: URL del artículo
            
        Returns:
            Contenido del artículo o None
        """
        if not url or url.startswith('https://news.ycombinator.com'):
            return None
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Eliminar elementos no deseados
            for element in soup(['script', 'style', 'nav', 'footer', 'aside', 'header']):
                element.decompose()
            
            # Intentar encontrar el contenido principal
            content = None
            
            # Estrategia 1: Buscar <article>
            article = soup.find('article')
            if article:
                content = article.get_text(separator=' ', strip=True)
            
            # Estrategia 2: Buscar divs con clases comunes de contenido
            if not content:
                for class_name in ['article-content', 'post-content', 'entry-content', 'content', 'main-content']:
                    div = soup.find('div', class_=class_name)
                    if div:
                        content = div.get_text(separator=' ', strip=True)
                        break
            
            # Estrategia 3: Buscar todos los párrafos
            if not content:
                paragraphs = soup.find_all('p')
                if len(paragraphs) > 3:
                    content = ' '.join([p.get_text(strip=True) for p in paragraphs])
            
            # Limpiar y truncar
            if content:
                content = ' '.join(content.split())  # Normalizar espacios
                content = content[:5000]  # Máximo 5000 caracteres
                return content
            
            return None
            
        except Exception as e:
            return None
    
    def _extract_comments(self, news_item: Dict) -> List[Dict]:
        """
        Extrae comentarios relevantes de HN o Reddit.
        
        Args:
            news_item: Noticia
            
        Returns:
            Lista de comentarios top
        """
        collector = news_item.get('collector', '')
        
        # Extraer comentarios de Hacker News
        if collector == 'hackernews' and news_item.get('hn_id'):
            return self._extract_hn_comments(news_item['hn_id'])
        
        # Extraer comentarios de Reddit
        if collector == 'reddit_scraper' and news_item.get('reddit_id'):
            return self._extract_reddit_comments(news_item['subreddit'], news_item['reddit_id'])
        
        return []
    
    def _extract_hn_comments(self, item_id: str, max_comments: int = 5) -> List[Dict]:
        """
        Extrae comentarios top de Hacker News.
        
        Args:
            item_id: ID del item en HN
            max_comments: Máximo de comentarios a extraer
            
        Returns:
            Lista de comentarios
        """
        try:
            url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
            response = requests.get(url, timeout=5)
            
            if response.status_code != 200:
                return []
            
            item = response.json()
            kids = item.get('kids', [])[:max_comments]
            
            comments = []
            for kid_id in kids:
                try:
                    comment_url = f"https://hacker-news.firebaseio.com/v0/item/{kid_id}.json"
                    comment_response = requests.get(comment_url, timeout=5)
                    
                    if comment_response.status_code == 200:
                        comment = comment_response.json()
                        if comment.get('text'):
                            # Limpiar HTML del texto
                            soup = BeautifulSoup(comment['text'], 'html.parser')
                            text = soup.get_text(strip=True)
                            
                            comments.append({
                                'author': comment.get('by', 'anonymous'),
                                'text': text[:500],  # Máximo 500 chars
                                'score': comment.get('score', 0)
                            })
                    
                    time.sleep(0.1)  # Rate limiting
                    
                except:
                    continue
            
            return comments
            
        except Exception as e:
            return []
    
    def _extract_reddit_comments(self, subreddit: str, post_id: str, max_comments: int = 5) -> List[Dict]:
        """
        Extrae comentarios top de Reddit.
        
        Args:
            subreddit: Nombre del subreddit
            post_id: ID del post
            max_comments: Máximo de comentarios
            
        Returns:
            Lista de comentarios
        """
        try:
            url = f"https://old.reddit.com/r/{subreddit}/comments/{post_id}/.json"
            headers = {'User-Agent': 'Mozilla/5.0'}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            
            if len(data) < 2:
                return []
            
            comments_data = data[1]['data']['children']
            comments = []
            
            for comment in comments_data[:max_comments]:
                comment_data = comment.get('data', {})
                
                if comment_data.get('body'):
                    comments.append({
                        'author': comment_data.get('author', 'anonymous'),
                        'text': comment_data['body'][:500],
                        'score': comment_data.get('score', 0)
                    })
            
            return comments
            
        except Exception as e:
            return []
    
    def _extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """
        Extrae keywords principales del texto.
        
        Simple implementación basada en frecuencia.
        Para producción: usar NLP (spaCy, NLTK, etc.)
        
        Args:
            text: Texto a analizar
            max_keywords: Máximo de keywords
            
        Returns:
            Lista de keywords
        """
        # Palabras a ignorar (stop words)
        stop_words = {
            'the', 'is', 'at', 'which', 'on', 'a', 'an', 'as', 'are', 'was', 'were',
            'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'and', 'or', 'but', 'in', 'to',
            'for', 'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during'
        }
        
        # Tokenizar y contar
        words = text.lower().split()
        word_freq = {}
        
        for word in words:
            # Limpiar palabra
            word = ''.join(c for c in word if c.isalnum())
            
            # Filtrar
            if len(word) > 3 and word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Ordenar por frecuencia
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, freq in sorted_words[:max_keywords]]
    
    def _calculate_engagement_score(self, news_item: Dict) -> float:
        """
        Calcula un score de engagement basado en métricas disponibles.
        
        Args:
            news_item: Noticia
            
        Returns:
            Score de engagement (0-100)
        """
        score = 0.0
        
        # Score de puntos/upvotes
        if 'score' in news_item:
            score += min(news_item['score'] / 10, 40)  # Max 40 puntos
        
        # Número de comentarios
        if 'num_comments' in news_item:
            score += min(news_item['num_comments'] / 5, 30)  # Max 30 puntos
        
        # Reacciones (Dev.to)
        if 'reactions' in news_item:
            score += min(news_item['reactions'] / 2, 20)  # Max 20 puntos
        
        # Bonus por fuente confiable
        source = news_item.get('source', '')
        trusted_sources = ['Hacker News', 'Ars Technica', 'MIT Technology Review']
        if any(trusted in source for trusted in trusted_sources):
            score += 10
        
        return min(score, 100)
    
    def enrich_multiple(self, news_items: List[Dict], delay: float = 1.0) -> List[Dict]:
        """
        Enriquece múltiples noticias.
        
        Args:
            news_items: Lista de noticias
            delay: Delay entre requests (rate limiting)
            
        Returns:
            Lista de noticias enriquecidas
        """
        enriched_items = []
        
        print(f"\n🔍 Enriqueciendo {len(news_items)} noticias...")
        
        for i, item in enumerate(news_items, 1):
            print(f"\n[{i}/{len(news_items)}]")
            enriched = self.enrich_news(item)
            enriched_items.append(enriched)
            
            # Rate limiting
            if i < len(news_items):
                time.sleep(delay)
        
        print(f"\n✅ {len(enriched_items)} noticias enriquecidas")
        
        return enriched_items


# Ejemplo de uso
if __name__ == "__main__":
    import json
    
    # Cargar noticias
    with open('data/selected_news.json', 'r', encoding='utf-8') as f:
        news = json.load(f)
    
    # Enriquecer
    enricher = ContentEnricher()
    enriched_news = enricher.enrich_multiple(news, delay=2.0)
    
    # Guardar
    with open('data/enriched_news.json', 'w', encoding='utf-8') as f:
        json.dump(enriched_news, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Guardado en: data/enriched_news.json")
