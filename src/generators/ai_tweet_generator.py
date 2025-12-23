"""
AI Tweet Generator - Generador inteligente de tweets con OpenAI

Este generador usa GPT para crear múltiples versiones de tweets
mucho más inteligentes y atractivas que los templates básicos.
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from dotenv import load_dotenv

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm.openai_provider import OpenAIProvider


class AITweetGenerator:
    """
    Generador de tweets con IA.
    
    Genera 2 versiones periodísticas por cada noticia:
    1. Inglés - Estilo periodista informativo
    2. Español - Estilo periodista informativo
    """
    
    def __init__(
        self,
        news_file: str = "data/selected_news.json",
        model: str = "gpt-3.5-turbo"
    ):
        """
        Inicializa el generador con IA.
        
        Args:
            news_file: Ruta al archivo con noticias
            model: Modelo de OpenAI a usar
        """
        self.news_file = Path(news_file)
        self.model = model
        
        # Cargar API key
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError(
                "❌ No se encontró OPENAI_API_KEY. "
                "Agrega tu API key al archivo .env"
            )
        
        self.provider = OpenAIProvider(api_key, model)
        
    def load_news(self) -> List[Dict]:
        """Carga las noticias desde el archivo JSON."""
        if not self.news_file.exists():
            print(f"⚠️  No se encontró el archivo: {self.news_file}")
            return []
        
        with open(self.news_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_all(self, limit: int = None) -> List[Dict]:
        """
        Genera threads técnicos y explicativos para todas las noticias.
        
        Args:
            limit: Máximo número de noticias a procesar
            
        Returns:
            Lista de tweets generados (formato simplificado: text + source)
        """
        news_list = self.load_news()
        
        if not news_list:
            print("⚠️  No hay noticias para procesar")
            return []
        
        if limit:
            news_list = news_list[:limit]
        
        print(f"🤖 Generando threads técnicos y explicativos para {len(news_list)} noticias...")
        print(f"   Modelo: {self.model}")
        print(f"   Estilo: ANÁLISIS TÉCNICO PROFUNDO")
        print(f"   Formato: Threads (si es necesario)\n")
        
        all_tweets = []
        
        for i, news_item in enumerate(news_list, 1):
            print(f"\n{'='*60}")
            print(f"📰 Noticia {i}/{len(news_list)}")
            print(f"   {news_item['title'][:60]}...")
            print(f"{'='*60}")
            
            try:
                # Generar thread técnico
                thread = self.provider.generate_tweet_thread(
                    title=news_item['title'],
                    summary=news_item.get('summary', ''),
                    full_content=news_item.get('full_content', ''),
                    source=news_item.get('source', ''),
                    link=news_item.get('link', '')
                )
                
                # Los tweets ya vienen en formato simplificado
                all_tweets.extend(thread)
                
                # Mostrar preview (separar por idioma)
                english_tweets = [t for t in thread if t.get('language') == 'en']
                spanish_tweets = [t for t in thread if t.get('language') == 'es']
                
                print(f"\n✅ Threads generados:")
                
                if english_tweets:
                    print(f"   🇬🇧 Inglés ({len(english_tweets)} tweets):")
                    if english_tweets[0].get('hook'):
                        print(f"      💡 {english_tweets[0]['hook'][:60]}...")
                    print(f"      📝 {english_tweets[0]['text'][:60]}...")
                
                if spanish_tweets:
                    print(f"   🇪🇸 Español ({len(spanish_tweets)} tweets):")
                    if spanish_tweets[0].get('hook'):
                        print(f"      💡 {spanish_tweets[0]['hook'][:60]}...")
                    print(f"      📝 {spanish_tweets[0]['text'][:60]}...")
                
            except Exception as e:
                print(f"❌ Error procesando noticia: {str(e)}")
                continue
        
        print(f"\n{'='*60}")
        print(f"✅ Generación completada:")
        print(f"   📊 {len(news_list)} noticias procesadas")
        print(f"   📝 {len(all_tweets)} tweets generados")
        english = sum(1 for t in all_tweets if t.get('language') == 'en')
        spanish = sum(1 for t in all_tweets if t.get('language') == 'es')
        print(f"   🇬🇧 {english} tweets en inglés")
        print(f"   🇪🇸 {spanish} tweets en español")
        print(f"{'='*60}")
        
        return all_tweets
    
    def save_tweets(
        self,
        tweets: List[Dict],
        output_path: str = "data/ai_tweets.json"
    ):
        """
        Guarda los tweets generados con IA.
        
        Args:
            tweets: Lista de tweets
            output_path: Ruta del archivo de salida
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(tweets, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Tweets guardados en: {output_path}")
        
    def display_tweets(self, tweets: List[Dict], limit: int = 2):
        """
        Muestra un preview de los tweets generados.
        
        Args:
            tweets: Lista de tweets
            limit: Número de noticias a mostrar
        """
        print("\n" + "="*70)
        print("📝 PREVIEW DE TWEETS GENERADOS")
        print("="*70)
        
        # Agrupar por fuente y idioma
        by_source = {}
        for tweet in tweets:
            source = tweet['source']
            lang = tweet.get('language', 'en')
            key = (source, lang)
            
            if key not in by_source:
                by_source[key] = []
            by_source[key].append(tweet)
        
        # Agrupar por fuente (sin idioma)
        by_source_only = {}
        for (source, lang), thread in by_source.items():
            if source not in by_source_only:
                by_source_only[source] = {'en': [], 'es': []}
            by_source_only[source][lang] = thread
        
        # Mostrar las primeras N noticias
        for i, (source, threads) in enumerate(list(by_source_only.items())[:limit], 1):
            print(f"\n{'='*70}")
            print(f"📰 Noticia {i}")
            print(f"   Fuente: {source}")
            print(f"{'='*70}")
            
            # Mostrar versión en inglés
            if threads['en']:
                print(f"\n   🇬🇧 VERSIÓN EN INGLÉS ({len(threads['en'])} tweets)")
                print(f"   {'-'*66}")
                
                # Mostrar hook
                if threads['en'][0].get('hook'):
                    print(f"\n   💡 HOOK:")
                    print(f"   {threads['en'][0]['hook']}")
                    print(f"   📏 {len(threads['en'][0]['hook'])} caracteres")
                
                # Mostrar tweets
                print(f"\n   📝 THREAD:")
                for tweet in threads['en']:
                    print(f"\n   {tweet.get('thread_position', '1/1')}")
                    print(f"   {tweet['text']}")
                    print(f"   📏 {len(tweet['text'])} caracteres")
            
            # Mostrar versión en español
            if threads['es']:
                print(f"\n   🇪🇸 VERSIÓN EN ESPAÑOL ({len(threads['es'])} tweets)")
                print(f"   {'-'*66}")
                
                # Mostrar hook
                if threads['es'][0].get('hook'):
                    print(f"\n   💡 HOOK:")
                    print(f"   {threads['es'][0]['hook']}")
                    print(f"   📏 {len(threads['es'][0]['hook'])} caracteres")
                
                # Mostrar tweets
                print(f"\n   📝 THREAD:")
                for tweet in threads['es']:
                    print(f"\n   {tweet.get('thread_position', '1/1')}")
                    print(f"   {tweet['text']}")
                    print(f"   📏 {len(tweet['text'])} caracteres")


# Ejemplo de uso
if __name__ == "__main__":
    try:
        # Crear generador
        generator = AITweetGenerator(model="gpt-3.5-turbo")
        
        # Generar tweets
        tweets = generator.generate_all(limit=2)  # Limitar a 2 noticias para probar
        
        if tweets:
            # Guardar
            generator.save_tweets(tweets)
            
            # Mostrar preview
            generator.display_tweets(tweets)
            
    except ValueError as e:
        print(f"\n{e}")
        print("\n💡 Para usar el generador con IA:")
        print("   1. Agrega tu OpenAI API key al archivo .env:")
        print("      OPENAI_API_KEY=sk-...")
        print("   2. Vuelve a ejecutar este script")

