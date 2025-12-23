"""
News Scorer - Sistema de puntuación de noticias

Este módulo califica cada noticia según su relevancia e importancia.
Es como un "agente" que decide qué noticias son más importantes.
"""

import yaml
from pathlib import Path
from typing import Dict, List
import re


class NewsScorer:
    """
    Califica noticias según keywords y criterios de prioridad.
    
    El scoring funciona así:
    - Keywords de alta prioridad: +10 puntos
    - Keywords de media prioridad: +5 puntos  
    - Keywords de baja prioridad: +2 puntos
    - Si está en el título: x2 multiplicador
    - Fuente prioritaria: +5 puntos
    - Keywords excluidas: -50 puntos (descarta)
    """
    
    def __init__(self, config_path: str = "config/priorities.yaml"):
        """
        Inicializa el scorer con la configuración de prioridades.
        
        Args:
            config_path: Ruta al archivo de configuración
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Carga la configuración de prioridades."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"⚠️  Archivo de configuración no encontrado: {self.config_path}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Configuración por defecto si no existe el archivo."""
        return {
            'high_priority_keywords': ['AI', 'startup', 'breakthrough'],
            'medium_priority_keywords': ['Python', 'technology'],
            'low_priority_keywords': ['tech', 'new'],
            'exclude_keywords': ['NSFW'],
            'priority_sources': [],
            'scoring': {
                'min_score': 10,
                'title_weight': 2.0,
                'max_tweets_per_run': 5
            }
        }
    
    def score_news(self, news_item: Dict) -> float:
        """
        Calcula el puntaje de relevancia de una noticia.
        
        Args:
            news_item: Diccionario con la información de la noticia
            
        Returns:
            Puntaje de relevancia (float)
        """
        score = 0.0
        title = news_item.get('title', '').lower()
        summary = news_item.get('summary', '').lower()
        source = news_item.get('source', '')
        
        # Combinar título y resumen para análisis
        full_text = f"{title} {summary}"
        
        # 1. Verificar palabras excluidas (descarta inmediatamente)
        exclude_keywords = self.config.get('exclude_keywords', [])
        for keyword in exclude_keywords:
            if keyword.lower() in full_text:
                return -100  # Puntaje muy negativo para descartar
        
        # 2. Keywords de ULTRA ALTA prioridad (lanzamientos, versiones)
        ultra_high_keywords = self.config.get('ultra_high_priority_keywords', [])
        for keyword in ultra_high_keywords:
            keyword_lower = keyword.lower()
            # Buscar en resumen
            if keyword_lower in summary:
                score += 25
            # Buscar en título (vale MUCHO más)
            if keyword_lower in title:
                score += 25 * self.config['scoring']['title_weight']
        
        # 3. Keywords de ALTA prioridad
        high_keywords = self.config.get('high_priority_keywords', [])
        for keyword in high_keywords:
            keyword_lower = keyword.lower()
            # Buscar en resumen
            if keyword_lower in summary:
                score += 18
            # Buscar en título (vale más)
            if keyword_lower in title:
                score += 18 * self.config['scoring']['title_weight']
        
        # 4. Keywords de MEDIA prioridad
        medium_keywords = self.config.get('medium_priority_keywords', [])
        for keyword in medium_keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in summary:
                score += 10
            if keyword_lower in title:
                score += 10 * self.config['scoring']['title_weight']
        
        # 5. Keywords de BAJA prioridad
        low_keywords = self.config.get('low_priority_keywords', [])
        for keyword in low_keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in full_text:
                score += 3
        
        # 6. Bonus por fuente prioritaria (fuentes oficiales)
        priority_sources = self.config.get('priority_sources', [])
        if source in priority_sources:
            score += 12  # Más puntos para fuentes oficiales
        
        # 7. Bonus por longitud del título (no muy corto ni muy largo)
        title_length = len(news_item.get('title', ''))
        if 40 <= title_length <= 150:
            score += 5
        
        return score
    
    def score_multiple_news(self, news_list: List[Dict]) -> List[Dict]:
        """
        Califica múltiples noticias y las ordena por relevancia.
        
        Args:
            news_list: Lista de noticias
            
        Returns:
            Lista de noticias con puntajes, ordenada de mayor a menor
        """
        print(f"🧠 Calificando {len(news_list)} noticias...")
        
        # Calcular score para cada noticia
        scored_news = []
        for news_item in news_list:
            score = self.score_news(news_item)
            news_with_score = news_item.copy()
            news_with_score['relevance_score'] = score
            scored_news.append(news_with_score)
        
        # Ordenar por score (mayor a menor)
        scored_news.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Filtrar por puntaje mínimo
        min_score = self.config['scoring'].get('min_score', 10)
        filtered_news = [n for n in scored_news if n['relevance_score'] >= min_score]
        
        print(f"✅ {len(filtered_news)} noticias pasaron el filtro (score mínimo: {min_score})")
        
        return filtered_news
    
    def get_top_news(self, news_list: List[Dict], limit: int = None) -> List[Dict]:
        """
        Obtiene las mejores N noticias.
        
        Args:
            news_list: Lista de noticias
            limit: Número máximo de noticias a retornar
            
        Returns:
            Lista de las mejores noticias
        """
        if limit is None:
            limit = self.config['scoring'].get('max_tweets_per_run', 5)
        
        scored_news = self.score_multiple_news(news_list)
        top_news = scored_news[:limit]
        
        print(f"\n🏆 Top {len(top_news)} noticias seleccionadas:")
        for i, news in enumerate(top_news, 1):
            print(f"   {i}. [{news['relevance_score']:.1f} pts] {news['title'][:60]}...")
        
        return top_news


# Ejemplo de uso
if __name__ == "__main__":
    import json
    
    # Cargar noticias
    with open("data/news.json", 'r', encoding='utf-8') as f:
        news = json.load(f)
    
    # Crear scorer
    scorer = NewsScorer()
    
    # Obtener top noticias
    top_news = scorer.get_top_news(news, limit=5)
    
    # Guardar noticias filtradas
    with open("data/filtered_news.json", 'w', encoding='utf-8') as f:
        json.dump(top_news, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Top noticias guardadas en: data/filtered_news.json")

