#!/usr/bin/env python3
"""
Script de Automatización - Ejecutar 2 veces al día

Este script ejecuta el flujo completo:
1. Recopila noticias
2. Selecciona las mejores con el agente
3. Genera tweets

Úsalo con cron para automatizar:
- 9:00 AM - Primera ejecución del día
- 6:00 PM - Segunda ejecución del día
"""

import sys
from pathlib import Path
from datetime import datetime
import logging

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from collectors.rss_collector import RSSCollector
from agent import NewsAgent
from generators.tweet_generator import TweetGenerator


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/automation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def run_automated_workflow():
    """Ejecuta el flujo completo automatizado."""
    
    logger.info("="*60)
    logger.info("🚀 INICIANDO FLUJO AUTOMATIZADO")
    logger.info("="*60)
    
    try:
        # Paso 1: Recopilar noticias
        logger.info("\n📡 PASO 1: Recopilando noticias...")
        collector = RSSCollector()
        news = collector.collect(max_age_hours=12)  # Últimas 12 horas
        
        if not news:
            logger.warning("⚠️  No se recopilaron noticias. Finalizando.")
            return False
        
        collector.save_to_file(news)
        logger.info(f"✅ {len(news)} noticias recopiladas")
        
        # Paso 2: Seleccionar mejores noticias
        logger.info("\n🤖 PASO 2: Seleccionando mejores noticias...")
        agent = NewsAgent()
        selected = agent.process_news(news, max_tweets=5)
        
        if not selected:
            logger.warning("⚠️  No se seleccionaron noticias. Finalizando.")
            return False
        
        agent.save_selected_news(selected)
        logger.info(f"✅ {len(selected)} noticias seleccionadas")
        
        # Paso 3: Generar tweets
        logger.info("\n📝 PASO 3: Generando tweets...")
        generator = TweetGenerator("data/selected_news.json")
        tweets = generator.generate(limit=len(selected))
        
        if not tweets:
            logger.warning("⚠️  No se generaron tweets. Finalizando.")
            return False
        
        # Guardar tweets con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"data/tweets_{timestamp}.json"
        generator.save_tweets(tweets, output_path)
        
        # También guardar en el archivo principal
        generator.save_tweets(tweets)
        
        logger.info(f"✅ {len(tweets)} tweets generados")
        
        # Resumen
        logger.info("\n" + "="*60)
        logger.info("✨ FLUJO COMPLETADO EXITOSAMENTE")
        logger.info(f"   📊 Noticias procesadas: {len(news)}")
        logger.info(f"   🎯 Noticias seleccionadas: {len(selected)}")
        logger.info(f"   📝 Tweets generados: {len(tweets)}")
        logger.info("="*60)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en el flujo automatizado: {str(e)}", exc_info=True)
        return False


if __name__ == "__main__":
    # Crear directorios necesarios
    Path("data").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    
    success = run_automated_workflow()
    sys.exit(0 if success else 1)

