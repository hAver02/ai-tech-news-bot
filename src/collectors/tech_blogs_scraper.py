"""
Tech Blogs Scraper - Scrapea blogs oficiales de empresas tech

Scrapea blogs de empresas como Google AI, Microsoft, Meta, etc.
que no tienen RSS o tienen contenido adicional en HTML.
"""

import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import time


class TechBlogsScraper:
    """Scraper de blogs oficiales de empresas tech."""
    
    def __init__(self):
        """Inicializa el scraper de blogs tech."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        # Configuración de blogs a scrapear
        self.blogs = {
            'google_ai': {
                'name': 'Google AI Blog',
                'url': 'https://blog.google/technology/ai/',
                'selector': 'article',
                'title_selector': 'h3',
                'link_selector': 'a',
                'summary_selector': 'p'
            },
            'openai': {
                'name': 'OpenAI News',
                'url': 'https://openai.com/news/',
                'selector': 'article',
                'title_selector': 'h3',
                'link_selector': 'a'
            },
            'anthropic': {
                'name': 'Anthropic News',
                'url': 'https://www.anthropic.com/news',
                'selector': 'article',
                'title_selector': 'h2',
                'link_selector': 'a'
            }
        }
    
    def scrape_blog(self, blog_key: str, max_articles: int = 10) -> List[Dict]:
        """
        Scrapea un blog específico.
        
        Args:
            blog_key: Clave del blog a scrapear
            max_articles: Máximo de artículos a extraer
            
        Returns:
            Lista de artículos extraídos
        """
        if blog_key not in self.blogs:
            print(f"⚠️  Blog '{blog_key}' no configurado")
            return []
        
        blog_config = self.blogs[blog_key]
        print(f"📡 Scrapeando {blog_config['name']}...")
        
        try:
            articles = self._scrape_generic_blog(blog_config, max_articles)
            print(f"  ✅ {blog_config['name']}: {len(articles)} artículos")
            return articles
        except Exception as e:
            print(f"  ❌ Error en {blog_config['name']}: {str(e)}")
            return []
    
    def _scrape_generic_blog(
        self,
        config: Dict,
        max_articles: int
    ) -> List[Dict]:
        """
        Scraper genérico para blogs con estructura similar.
        
        Args:
            config: Configuración del blog
            max_articles: Máximo de artículos
            
        Returns:
            Lista de artículos
        """
        response = requests.get(
            config['url'],
            headers=self.headers,
            timeout=15
        )
        
        if response.status_code != 200:
            raise Exception(f"HTTP error: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscar artículos
        article_elements = soup.select(config['selector'])[:max_articles]
        
        articles = []
        
        for article_elem in article_elements:
            try:
                # Extraer título
                title_elem = article_elem.select_one(config['title_selector'])
                if not title_elem:
                    continue
                title = title_elem.get_text(strip=True)
                
                # Extraer link
                link_elem = article_elem.select_one(config['link_selector'])
                if not link_elem:
                    continue
                link = link_elem.get('href', '')
                
                # Hacer link absoluto si es relativo
                if link.startswith('/'):
                    from urllib.parse import urlparse
                    parsed = urlparse(config['url'])
                    link = f"{parsed.scheme}://{parsed.netloc}{link}"
                
                # Extraer summary (opcional)
                summary = ''
                if 'summary_selector' in config:
                    summary_elem = article_elem.select_one(config['summary_selector'])
                    if summary_elem:
                        summary = summary_elem.get_text(strip=True)[:500]
                
                # Crear artículo
                article = {
                    'title': title,
                    'link': link,
                    'summary': summary,
                    'published': None,  # Difícil de extraer sin estructura
                    'source': config['name'],
                    'category': 'tech',
                    'collected_at': datetime.now().isoformat(),
                    'collector': 'tech_blogs_scraper'
                }
                
                articles.append(article)
                
            except Exception as e:
                continue
        
        return articles
    
    def scrape_all_blogs(self, max_articles_per_blog: int = 10) -> List[Dict]:
        """
        Scrapea todos los blogs configurados.
        
        Args:
            max_articles_per_blog: Máximo de artículos por blog
            
        Returns:
            Lista de todos los artículos
        """
        all_articles = []
        
        for blog_key in self.blogs.keys():
            try:
                articles = self.scrape_blog(blog_key, max_articles_per_blog)
                all_articles.extend(articles)
                
                # Rate limiting - ser respetuoso
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Error en blog {blog_key}: {str(e)}")
        
        return all_articles
    
    def add_custom_blog(
        self,
        key: str,
        name: str,
        url: str,
        selector: str,
        title_selector: str,
        link_selector: str,
        summary_selector: str = None
    ):
        """
        Añade un blog personalizado a scrapear.
        
        Args:
            key: Clave única para el blog
            name: Nombre del blog
            url: URL del blog
            selector: Selector CSS para artículos
            title_selector: Selector para título
            link_selector: Selector para link
            summary_selector: Selector para resumen (opcional)
        """
        self.blogs[key] = {
            'name': name,
            'url': url,
            'selector': selector,
            'title_selector': title_selector,
            'link_selector': link_selector
        }
        
        if summary_selector:
            self.blogs[key]['summary_selector'] = summary_selector
        
        print(f"✅ Blog '{name}' añadido para scraping")
    
    def save_to_file(self, articles: List[Dict], output_path: str = "data/tech_blogs.json"):
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
        
        print(f"💾 Artículos de blogs tech guardados en: {output_path}")


# Ejemplo de uso
if __name__ == "__main__":
    # Crear el scraper
    scraper = TechBlogsScraper()
    
    # Añadir un blog personalizado
    # scraper.add_custom_blog(
    #     key='vercel',
    #     name='Vercel Blog',
    #     url='https://vercel.com/blog',
    #     selector='article',
    #     title_selector='h2',
    #     link_selector='a'
    # )
    
    # Scrapear todos los blogs configurados
    articles = scraper.scrape_all_blogs(max_articles_per_blog=10)
    
    # O scrapear un blog específico
    # articles = scraper.scrape_blog('google_ai', max_articles=10)
    
    # Guardar en archivo
    if articles:
        scraper.save_to_file(articles)
        
        # Mostrar los primeros 5 artículos
        print("\n📰 Primeros 5 artículos:")
        for i, article in enumerate(articles[:5], 1):
            print(f"\n{i}. {article['title']}")
            print(f"   🏢 {article['source']}")
            print(f"   🔗 {article['link']}")
            if article['summary']:
                print(f"   📝 {article['summary'][:100]}...")
    else:
        print("\n⚠️  No se scrapearon artículos.")
