"""
TechNews Tweet Generator - Punto de entrada principal

Este es el archivo principal que coordina todo el sistema.
"""

import argparse
import json
from pathlib import Path
from datetime import datetime

from collectors.rss_collector import RSSCollector
from collectors.news_api_collector import NewsAPICollector
from collectors.hackernews_collector import HackerNewsCollector
from collectors.reddit_scraper import RedditScraper
from collectors.devto_collector import DevToCollector
from collectors.newsdata_collector import NewsDataCollector
from collectors.guardian_collector import GuardianCollector
from generators.tweet_generator import TweetGenerator
from generators.ai_tweet_generator import AITweetGenerator
from agent import NewsAgent


def collect_news():
    """Recopila noticias de todas las fuentes configuradas."""
    print("🔍 Recopilando noticias tecnológicas desde TODAS las fuentes...\n")
    
    all_news = []
    stats = {}
    
    # Fuente 1: RSS Feeds
    print("📡 Fuente #1: RSS Feeds")
    print("-" * 60)
    rss_collector = RSSCollector()
    rss_news = rss_collector.collect(max_age_hours=24)
    all_news.extend(rss_news)
    stats['RSS Feeds'] = len(rss_news)
    
    # Fuente 2: News API
    print("\n📡 Fuente #2: News API")
    print("-" * 60)
    news_api_collector = NewsAPICollector()
    news_api_news = news_api_collector.collect(max_age_hours=24, max_results_per_query=10)
    all_news.extend(news_api_news)
    stats['News API'] = len(news_api_news)
    
    # Fuente 3: Hacker News
    print("\n📡 Fuente #3: Hacker News")
    print("-" * 60)
    hn_collector = HackerNewsCollector()
    
    # Top stories (noticias populares)
    hn_top = hn_collector.collect(story_type='top', max_items=20, min_score=50)
    print(f"  ✅ HN Top: {len(hn_top)} historias")
    
    # New stories (noticias recientes, últimas 2-3 horas)
    hn_new = hn_collector.collect(story_type='new', max_items=30, min_score=20)
    print(f"  ✅ HN New: {len(hn_new)} historias")
    
    # Best stories (mejores del día)
    hn_best = hn_collector.collect(story_type='best', max_items=15, min_score=40)
    print(f"  ✅ HN Best: {len(hn_best)} historias")
    
    all_news.extend(hn_top)
    all_news.extend(hn_new)
    all_news.extend(hn_best)
    stats['Hacker News'] = len(hn_top) + len(hn_new) + len(hn_best)
    
    # Fuente 4: Reddit
    print("\n📡 Fuente #4: Reddit (Scraping)")
    print("-" * 60)
    # DESACTIVADO - Reddit tiene noticias no oficiales
    # reddit_scraper = RedditScraper()
    # reddit_news = reddit_scraper.collect_multiple_subreddits(
    #     subreddits=['technology', 'programming', 'Python', 'artificial', 'MachineLearning'],
    #     limit_per_subreddit=10,
    #     min_score=50
    # )
    # all_news.extend(reddit_news)
    # stats['Reddit'] = len(reddit_news)
    stats['Reddit'] = 0  # Desactivado
    
    # Fuente 5: Dev.to
    print("\n📡 Fuente #5: Dev.to")
    print("-" * 60)
    devto_collector = DevToCollector()
    devto_news = devto_collector.collect_multiple_tags(
        tags=[
            'python', 'javascript', 'typescript', 'ai', 'webdev',
            'react', 'nextjs', 'rust', 'machinelearning', 
            'nodejs', 'devops', 'cloud', 'programming'
        ],
        per_page_per_tag=5,  # Menos por tag pero más tags
        min_reactions=3  # Menos restrictivo
    )
    all_news.extend(devto_news)
    stats['Dev.to'] = len(devto_news)
    
    # Fuente 6: NewsData.io
    print("\n📡 Fuente #6: NewsData.io")
    print("-" * 60)
    try:
        newsdata_collector = NewsDataCollector()
        newsdata_news = newsdata_collector.collect_multiple_queries(
            queries=[
                {'query': 'AI', 'language': 'en'},
                {'query': 'programming', 'language': 'en'},
                {'query': 'machine learning', 'language': 'en'},
                {'query': 'software development', 'language': 'en'},
                {'query': 'technology startup', 'language': 'en'}
            ],
            max_results_per_query=10
        )
        all_news.extend(newsdata_news)
        stats['NewsData.io'] = len(newsdata_news)
    except Exception as e:
        print(f"  ⚠️  Error en NewsData.io: {str(e)}")
        stats['NewsData.io'] = 0
    
    # Fuente 7: The Guardian
    print("\n📡 Fuente #7: The Guardian")
    print("-" * 60)
    try:
        guardian_collector = GuardianCollector()
        guardian_news = guardian_collector.collect_multiple_sections(
            sections=['technology', 'science', 'business'],
            max_results_per_section=20
        )
        all_news.extend(guardian_news)
        stats['The Guardian'] = len(guardian_news)
    except Exception as e:
        print(f"  ⚠️  Error en The Guardian: {str(e)}")
        stats['The Guardian'] = 0
    
    # Guardar todas las noticias combinadas
    if all_news:
        import json
        from pathlib import Path
        
        output_file = Path("data/news.json")
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_news, f, ensure_ascii=False, indent=2)
        
        print("\n" + "=" * 60)
        print(f"✅ TOTAL: {len(all_news)} noticias recopiladas")
        for source, count in stats.items():
            print(f"   - {source}: {count} noticias")
        print("=" * 60)
        print(f"💾 Guardadas en: data/news.json")
    else:
        print("⚠️  No se recopilaron noticias de ninguna fuente")
    
    return all_news


def select_news():
    """Selecciona las mejores noticias usando el agente inteligente."""
    print("\n🤖 Seleccionando mejores noticias...")
    
    # Cargar noticias recopiladas
    news_file = Path("data/news.json")
    if not news_file.exists():
        print("⚠️  No hay noticias recopiladas. Ejecuta 'collect' primero.")
        return []
    
    with open(news_file, 'r', encoding='utf-8') as f:
        all_news = json.load(f)
    
    # Usar agente para seleccionar (mostrar top 15 para review manual)
    agent = NewsAgent()
    selected = agent.process_news(all_news, max_tweets=15)
    
    if selected:
        agent.save_selected_news(selected)
    
    return selected


def review_news():
    """Revisa y califica manualmente las noticias seleccionadas para entrenar el modelo."""
    print("\n" + "="*70)
    print("📝 REVISIÓN MANUAL DE NOTICIAS")
    print("="*70)
    print("\nRevisa cada noticia y marca si te sirve o no.")
    print("El modelo ML aprenderá de tus decisiones.\n")
    
    # Cargar noticias seleccionadas
    selected_file = Path("data/selected_news.json")
    if not selected_file.exists():
        print("⚠️  No hay noticias seleccionadas. Ejecuta 'select' primero.")
        return
    
    with open(selected_file, 'r', encoding='utf-8') as f:
        news_list = json.load(f)
    
    if not news_list:
        print("⚠️  No hay noticias para revisar.")
        return
    
    # Cargar modelo ML
    from ml.news_selector_model import NewsSelectorModel
    model = NewsSelectorModel()
    
    # Intentar cargar modelo entrenado previo
    try:
        model.load_model()
        print("✅ Modelo ML cargado (se actualizará con tu feedback)\n")
    except:
        print("📊 Modelo ML nuevo (se entrenará con tu feedback)\n")
    
    approved_news = []
    feedback_data = []
    
    for i, news in enumerate(news_list, 1):
        print("="*70)
        print(f"\n📰 NOTICIA {i}/{len(news_list)}")
        print(f"Score actual: {news.get('relevance_score', 0):.1f} pts")
        print("-"*70)
        print(f"\n📌 Título: {news['title']}")
        print(f"📰 Fuente: {news.get('source', 'N/A')}")
        print(f"🔗 Link: {news.get('link', 'N/A')[:80]}...")
        if news.get('summary'):
            print(f"\n📝 Resumen:\n{news['summary'][:200]}...")
        
        print("\n" + "-"*70)
        
        # Preguntar al usuario
        while True:
            choice = input("\n¿Esta noticia te sirve? [s=sí / n=no / x=salir]: ").lower().strip()
            
            if choice == 'x':
                print("\n🛑 Revisión cancelada.")
                break
            
            if choice in ['s', 'n']:
                label = 1 if choice == 's' else 0
                
                # Guardar feedback
                feedback_data.append({
                    'news': news,
                    'label': label
                })
                
                if choice == 's':
                    approved_news.append(news)
                    print("   ✅ Marcada como BUENA")
                else:
                    print("   ❌ Marcada como NO RELEVANTE")
                
                break
            else:
                print("   ⚠️  Opción inválida. Usa 's', 'n' o 'x'")
        
        if choice == 'x':
            break
    
    # Entrenar modelo con el feedback
    if feedback_data:
        print("\n" + "="*70)
        print("🧠 ENTRENANDO MODELO ML CON TU FEEDBACK")
        print("="*70)
        
        for item in feedback_data:
            model.add_feedback(item['news'], item['label'])
        
        # Guardar modelo actualizado
        model.save_model()
        
        print(f"\n✅ Modelo entrenado con {len(feedback_data)} ejemplos")
        print(f"   📊 Aceptadas: {sum(1 for x in feedback_data if x['label'] == 1)}")
        print(f"   📊 Rechazadas: {sum(1 for x in feedback_data if x['label'] == 0)}")
    
    # Guardar noticias aprobadas para generar tweets
    if approved_news:
        output_file = Path("data/approved_news.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(approved_news, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 {len(approved_news)} noticias aprobadas guardadas en: data/approved_news.json")
        print("   Ejecuta 'python src/main.py generate' para crear tweets")
    
    print("\n" + "="*70)


def generate_tweets():
    """Genera tweets con IA a partir de las noticias seleccionadas."""
    print("\n📝 Generando tweets con IA...")
    
    # Prioridad: aprobadas manualmente > seleccionadas > todas
    approved_file = Path("data/approved_news.json")
    selected_file = Path("data/selected_news.json")
    news_file = Path("data/news.json")
    
    if approved_file.exists():
        print("   ✅ Usando noticias APROBADAS manualmente...")
        input_file = approved_file
    elif selected_file.exists():
        print("   📰 Usando noticias seleccionadas por el agente...")
        input_file = selected_file
    elif news_file.exists():
        print("   📰 Usando todas las noticias recopiladas...")
        input_file = news_file
    else:
        print("⚠️  No hay noticias disponibles. Ejecuta 'collect' primero.")
        return []
    
    try:
        # Usar generador con IA (2 versiones periodísticas)
        generator = AITweetGenerator(str(input_file))
        tweets = generator.generate_all(limit=5)  # Max 5 noticias
        
        if tweets:
            generator.save_tweets(tweets)
            print(f"\n✅ {len(tweets)} tweets generados exitosamente!")
            print(f"   💾 Guardados en: data/ai_tweets.json")
            
            # Mostrar preview
            generator.display_tweets(tweets, limit=2)
        
        return tweets
        
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("   Usando generador básico como fallback...")
        
        # Fallback al generador básico
        generator = TweetGenerator(str(input_file))
        tweets = generator.generate(limit=10)
        
        if tweets:
            generator.save_tweets(tweets)
            print(f"✅ {len(tweets)} tweets generados (básicos)")
        
        return tweets


def validate_news_with_llm():
    """Valida noticias recopiladas usando el agente LLM validador."""
    print("\n🤖 Validando noticias con Agente LLM...")
    
    # Cargar noticias
    news_file = Path("data/news.json")
    if not news_file.exists():
        print("⚠️  No hay noticias para validar. Ejecuta 'collect' primero.")
        return
    
    with open(news_file, 'r', encoding='utf-8') as f:
        all_news = json.load(f)
    
    print(f"📰 Cargadas {len(all_news)} noticias")
    
    # Importar agente
    from agents.news_validator_agent import NewsValidatorAgent
    
    # Crear y ejecutar agente
    agent = NewsValidatorAgent()
    validated_news = agent.validate_batch(
        all_news,
        min_relevance=60,
        min_quality=60,
        require_recent=True
    )
    
    # Guardar resultado
    if validated_news:
        output_file = Path("data/validated_news.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(validated_news, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ {len(validated_news)} noticias validadas")
        print(f"💾 Guardadas en: {output_file}")
        print(f"\nEjecuta 'python src/main.py select' para procesar las validadas")
    else:
        print("\n❌ Ninguna noticia pasó la validación")


def start_continuous_collector():
    """Inicia el agente recopilador continuo."""
    print("\n🔄 Iniciando Agente Recopilador Continuo...")
    
    # Importar agente
    from agents.continuous_collector_agent import ContinuousCollectorAgent
    
    # Crear agente
    agent = ContinuousCollectorAgent(
        interval_minutes=30,  # Cada 30 minutos
        max_age_hours=4       # Solo últimas 4 horas
    )
    
    # Preguntar duración
    print("\n¿Cuántas horas quieres que busque noticias?")
    print("  0 = infinito (hasta Ctrl+C)")
    print("  1-24 = horas específicas")
    
    try:
        duration = int(input("Horas: ").strip())
        if duration == 0:
            duration = None
    except:
        duration = 2  # Default: 2 horas
        print(f"Usando default: {duration} horas")
    
    # Ejecutar
    agent.run_continuously(duration_hours=duration)


def list_tweets():
    """Muestra los tweets pendientes de publicar."""
    print("📝 Tweets pendientes:")
    
    tweets_file = Path("data/tweets.json")
    if tweets_file.exists():
        with open(tweets_file, 'r', encoding='utf-8') as f:
            tweets = json.load(f)
            
        for i, tweet in enumerate(tweets, 1):
            print(f"\n{i}. {tweet.get('text', '')}")
            print(f"   Fuente: {tweet.get('source', 'N/A')}")
    else:
        print("No hay tweets pendientes.")


def main():
    """Función principal con menú de comandos."""
    
    parser = argparse.ArgumentParser(
        description="TechNews Tweet Generator - Sistema de generación de tweets tech"
    )
    
    parser.add_argument(
        'command',
        choices=['collect', 'select', 'review', 'generate', 'list', 'all', 'validate', 'watch'],
        help='Comando a ejecutar'
    )
    
    args = parser.parse_args()
    
    # Crear directorios si no existen
    Path("data").mkdir(exist_ok=True)
    
    if args.command == 'collect':
        collect_news()
    elif args.command == 'select':
        select_news()
    elif args.command == 'review':
        review_news()
    elif args.command == 'generate':
        generate_tweets()
    elif args.command == 'list':
        list_tweets()
    elif args.command == 'validate':
        validate_news_with_llm()
    elif args.command == 'watch':
        start_continuous_collector()
    elif args.command == 'all':
        # Flujo completo con agente
        news = collect_news()
        if news:
            selected = select_news()
            if selected:
                generate_tweets()
                list_tweets()
            else:
                print("\n⚠️  No se seleccionaron noticias para generar tweets")
        else:
            print("\n⚠️  No se recopilaron noticias")


if __name__ == "__main__":
    main()

