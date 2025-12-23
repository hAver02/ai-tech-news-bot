"""
News Agent - Agente inteligente selector de noticias

Este es el "cerebro" del sistema. Coordina:
1. Filtrado básico de noticias
2. Scoring/puntuación por relevancia
3. Selección de las mejores noticias
"""

import json
from pathlib import Path
from typing import List, Dict

from utils.news_filter import NewsFilter
from utils.news_scorer import NewsScorer


class NewsAgent:
    """
    Agente inteligente que selecciona las mejores noticias.
    
    Este agente:
    - Aplica filtros básicos (duplicados, antigüedad, etc.)
    - Califica cada noticia por relevancia
    - Selecciona las top N noticias para generar tweets
    """
    
    def __init__(self, priorities_config: str = "config/priorities.yaml"):
        """
        Inicializa el agente.
        
        Args:
            priorities_config: Ruta al archivo de configuración
        """
        self.scorer = NewsScorer(priorities_config)
        self.filter = NewsFilter()
        
    def process_news(
        self,
        news_list: List[Dict],
        max_tweets: int = None
    ) -> List[Dict]:
        """
        Procesa noticias y selecciona las mejores.
        
        Args:
            news_list: Lista de todas las noticias recopiladas
            max_tweets: Máximo número de tweets a generar
            
        Returns:
            Lista de las mejores noticias seleccionadas
        """
        print("\n" + "="*60)
        print("🤖 AGENTE SELECTOR DE NOTICIAS")
        print("="*60)
        
        if not news_list:
            print("⚠️  No hay noticias para procesar")
            return []
        
        print(f"\n📊 Noticias recopiladas: {len(news_list)}")
        
        # Paso 1: Filtrado básico
        print("\n🔍 PASO 1: Filtrado básico")
        filtered_news = self.filter.apply_all_filters(news_list)
        
        if not filtered_news:
            print("⚠️  No hay noticias después del filtrado")
            return []
        
        # Paso 2: Scoring y selección
        print("\n🧠 PASO 2: Análisis de relevancia")
        top_news = self.scorer.get_top_news(filtered_news, limit=max_tweets)
        
        if not top_news:
            print("⚠️  No hay noticias que cumplan el puntaje mínimo")
            return []
        
        # Mostrar resumen
        print("\n" + "="*60)
        print(f"✅ RESULTADO: {len(top_news)} noticias seleccionadas")
        print("="*60)
        
        return top_news
    
    def save_selected_news(
        self,
        news_list: List[Dict],
        output_path: str = "data/selected_news.json"
    ):
        """
        Guarda las noticias seleccionadas en un archivo.
        
        Args:
            news_list: Lista de noticias seleccionadas
            output_path: Ruta del archivo de salida
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Noticias seleccionadas guardadas en: {output_path}")


# Ejemplo de uso
if __name__ == "__main__":
    # Cargar noticias recopiladas
    with open("data/news.json", 'r', encoding='utf-8') as f:
        all_news = json.load(f)
    
    # Crear agente
    agent = NewsAgent()
    
    # Procesar y seleccionar mejores noticias
    selected_news = agent.process_news(all_news, max_tweets=5)
    
    # Guardar resultado
    if selected_news:
        agent.save_selected_news(selected_news)
        
        print("\n📝 Noticias seleccionadas:")
        for i, news in enumerate(selected_news, 1):
            score = news.get('relevance_score', 0)
            print(f"\n{i}. [{score:.1f} pts] {news['title']}")
            print(f"   📰 {news['source']}")
            print(f"   🔗 {news['link']}")

