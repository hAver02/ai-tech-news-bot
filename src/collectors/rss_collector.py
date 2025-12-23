"""
RSS Collector - Recopila noticias desde RSS feeds

Este módulo es el MÁS FÁCIL de implementar y no requiere API keys.
Perfecto para empezar a aprender Python.
"""

import feedparser
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict


class RSSCollector:
    """Recolector de noticias desde RSS feeds."""
    
    def __init__(self, config_path: str = "config/sources.yaml"):
        """
        Inicializa el recolector RSS.
        
        Args:
            config_path: Ruta al archivo de configuración
        """
        self.config_path = Path(config_path)
        self.feeds = self._load_feeds()
    
    def _load_feeds(self) -> List[Dict]:
        """Carga la lista de RSS feeds desde el archivo de configuración."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config.get('rss_feeds', [])
        except FileNotFoundError:
            print(f"⚠️  Archivo de configuración no encontrado: {self.config_path}")
            return []
    
    def collect(self, max_age_hours: int = 24) -> List[Dict]:
        """
        Recopila noticias de todos los RSS feeds configurados.
        
        Args:
            max_age_hours: Máxima antigüedad de las noticias en horas
            
        Returns:
            Lista de noticias recopiladas
        """
        all_news = []
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        print(f"📡 Recopilando desde {len(self.feeds)} fuentes RSS...")
        
        for feed_config in self.feeds:
            try:
                news = self._collect_from_feed(feed_config, cutoff_time)
                all_news.extend(news)
                print(f"  ✅ {feed_config['name']}: {len(news)} noticias")
            except Exception as e:
                print(f"  ❌ Error en {feed_config['name']}: {str(e)}")
        
        print(f"\n📊 Total recopilado: {len(all_news)} noticias")
        return all_news
    
    def _collect_from_feed(self, feed_config: Dict, cutoff_time: datetime) -> List[Dict]:
        """
        Recopila noticias de un RSS feed específico.
        
        Args:
            feed_config: Configuración del feed
            cutoff_time: Tiempo de corte para filtrar noticias antiguas
            
        Returns:
            Lista de noticias del feed
        """
        feed = feedparser.parse(feed_config['url'])
        news = []
        
        for entry in feed.entries:
            # Parsear fecha de publicación
            published = None
            if hasattr(entry, 'published_parsed'):
                published = datetime(*entry.published_parsed[:6])
            
            # Filtrar por antigüedad
            if published and published < cutoff_time:
                continue
            
            # Extraer información relevante
            news_item = {
                'title': entry.get('title', ''),
                'link': entry.get('link', ''),
                'summary': entry.get('summary', ''),
                'published': published.isoformat() if published else None,
                'source': feed_config['name'],
                'category': feed_config.get('category', 'tech'),
                'collected_at': datetime.now().isoformat()
            }
            
            news.append(news_item)
        
        return news
    
    def save_to_file(self, news: List[Dict], output_path: str = "data/news.json"):
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
        
        print(f"💾 Noticias guardadas en: {output_path}")


# Ejemplo de uso
if __name__ == "__main__":
    # Crear el recolector
    collector = RSSCollector()
    
    # Recopilar noticias de las últimas 24 horas
    news = collector.collect(max_age_hours=24)
    
    # Guardar en archivo
    collector.save_to_file(news)
    
    # Mostrar las primeras 3 noticias
    print("\n📰 Primeras 3 noticias:")
    for i, item in enumerate(news[:3], 1):
        print(f"\n{i}. {item['title']}")
        print(f"   Fuente: {item['source']}")
        print(f"   Link: {item['link']}")

