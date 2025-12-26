"""
News Validator Agent - Agente LLM que valida relevancia y frescura de noticias

Este agente usa OpenAI GPT para:
1. Analizar si la noticia es reciente (últimas horas)
2. Evaluar relevancia según preferencias del usuario
3. Detectar duplicados semánticos
4. Dar score de calidad
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from openai import OpenAI
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class NewsValidatorAgent:
    """
    Agente inteligente que valida noticias usando LLM.
    
    Este agente analiza cada noticia y determina:
    - ¿Es suficientemente reciente?
    - ¿Es relevante para mis intereses?
    - ¿Tiene buena calidad?
    - ¿Es duplicada?
    """
    
    def __init__(self, model: str = "gpt-3.5-turbo"):
        """
        Inicializa el agente validador.
        
        Args:
            model: Modelo de OpenAI a usar
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY no encontrada en variables de entorno")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        
        # Temas prioritarios ULTRA ESPECÍFICOS
        self.priority_topics = {
            "AI Coding (Muy Alto)": [
                "Cursor IDE features, updates, benchmarks",
                "Windsurf, Lovable, Bolt.new, Replit Agent",
                "Claude Sonnet 4.5 coding capabilities",
                "Aider, Cline, Continue.dev",
                "GitHub Copilot workspace, chat modes"
            ],
            "Hardware AI (Muy Alto)": [
                "Nvidia H100/H200/B200 availability, pricing",
                "AMD MI300X benchmarks, adoption",
                "GPU memory bandwidth issues",
                "Chip shortage, supply chain",
                "Groq LPU, Cerebras, new AI accelerators"
            ],
            "Frameworks/Frontend (Alto)": [
                "Next.js (App Router, Server Actions, Turbopack)",
                "React 19 (Compiler, Server Components)",
                "TypeScript breaking changes, new features",
                "Svelte 5 runes, Astro 5, Remix updates"
            ],
            "Databases/Backend (Alto)": [
                "Supabase (realtime, edge functions, vector)",
                "Prisma ORM improvements, performance",
                "PostgreSQL 17, Turso, Neon, PlanetScale",
                "Redis, MongoDB updates relevantes"
            ],
            "Systems/Rust (Medio)": [
                "Rust async runtime, stabilizations",
                "Tauri vs Electron performance",
                "Rust web frameworks (Axum, Actix)",
                "Systems programming innovations"
            ],
            "AI Models (Medio)": [
                "Claude, GPT-4, Gemini updates TÉCNICOS",
                "Llama, Mixtral, Qwen benchmarks",
                "Model APIs, pricing changes",
                "Fine-tuning, embeddings"
            ],
            "Startups/Business (Bajo)": [
                "Solo si: Acquisitions tech-relevantes",
                "Funding de AI infrastructure/dev tools",
                "Decisiones técnicas de empresas (migrations)"
            ]
        }
        
        # LO QUE NO QUIERO (muy importante)
        self.exclude_topics = [
            "Gaming (excepto tech arquitectura)",
            "Política/regulación (excepto impacto directo dev)",
            "Funding genérico sin detalle técnico",
            "Tutoriales básicos/introductorios",
            "Clickbait, controversial topics",
            "Celebrity tech news",
            "Product marketing sin sustancia técnica"
        ]
    
    def validate_news(self, news_item: Dict) -> Dict:
        """
        Valida una noticia individual usando LLM.
        
        Args:
            news_item: Diccionario con la información de la noticia
            
        Returns:
            Dict con validación: {
                'is_valid': bool,
                'is_recent': bool,
                'relevance_score': float (0-100),
                'quality_score': float (0-100),
                'reason': str,
                'topics_matched': List[str]
            }
        """
        title = news_item.get('title', '')
        summary = news_item.get('summary', '')
        source = news_item.get('source', '')
        published = news_item.get('published', '')
        
        # Prompt MEJORADO para el LLM
        topics_text = "\n".join([
            f"{category}:\n" + "\n".join(f"  - {item}" for item in items)
            for category, items in self.priority_topics.items()
        ])
        
        exclude_text = "\n".join(f"- {topic}" for topic in self.exclude_topics)
        
        prompt = f"""Analiza esta noticia tech y determina su relevancia TÉCNICA.

NOTICIA:
Título: {title}
Resumen: {summary}
Fuente: {source}
Publicada: {published}

INTERESES ULTRA ESPECÍFICOS (en orden de prioridad):
{topics_text}

NO ME INTERESA:
{exclude_text}

CRITERIOS DE EVALUACIÓN:

RELEVANCIA (0-100):
- 90-100: Perfectamente alineado (releases oficiales, breaking changes, benchmarks)
- 70-89: Muy relevante (updates importantes, technical deep dives)
- 50-69: Relevante (noticias tech sólidas)
- 30-49: Parcialmente relevante
- 0-29: Poco o nada relevante

CALIDAD (0-100):
- 90-100: Profundidad técnica excepcional, fuente oficial
- 70-89: Contenido técnico sólido, bien documentado
- 50-69: Información correcta pero no profunda
- 30-49: Superficial o marketing-heavy
- 0-29: Clickbait, sin sustancia técnica

RESPONDE SOLO CON JSON (sin markdown, sin explicaciones extra):
{{
  "is_recent": true,
  "relevance_score": 85,
  "quality_score": 90,
  "reason": "Next.js 15 release con Turbopack - muy relevante para frameworks",
  "topics_matched": ["Frameworks/Frontend"]
}}

IMPORTANTE:
- is_recent: true si <24h, false si más antiguo
- Sé ESTRICTO con relevance_score (solo 80+ si es realmente importante)
- Penaliza clickbait, tutoriales básicos, noticias genéricas
- Prioriza: official releases, breaking changes, benchmarks, technical decisions
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un experto analista de noticias tech que evalúa relevancia y calidad."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Parsear JSON
            validation = json.loads(result_text)
            
            # Agregar campo is_valid
            validation['is_valid'] = (
                validation.get('is_recent', False) and 
                validation.get('relevance_score', 0) >= 50 and
                validation.get('quality_score', 0) >= 50
            )
            
            return validation
            
        except Exception as e:
            print(f"⚠️  Error validando noticia: {str(e)}")
            return {
                'is_valid': False,
                'is_recent': False,
                'relevance_score': 0,
                'quality_score': 0,
                'reason': f'Error: {str(e)}',
                'topics_matched': []
            }
    
    def validate_batch(
        self, 
        news_list: List[Dict],
        min_relevance: int = 50,
        min_quality: int = 50,
        require_recent: bool = True
    ) -> List[Dict]:
        """
        Valida un lote de noticias.
        
        Args:
            news_list: Lista de noticias
            min_relevance: Score mínimo de relevancia
            min_quality: Score mínimo de calidad
            require_recent: Si requiere que sean recientes
            
        Returns:
            Lista de noticias validadas con metadata
        """
        print(f"\n🤖 AGENTE VALIDADOR LLM")
        print(f"   Validando {len(news_list)} noticias...")
        print(f"   Filtros: relevance>={min_relevance}, quality>={min_quality}, recent={require_recent}")
        
        validated_news = []
        stats = {
            'total': len(news_list),
            'valid': 0,
            'rejected_old': 0,
            'rejected_irrelevant': 0,
            'rejected_low_quality': 0
        }
        
        for i, news in enumerate(news_list, 1):
            print(f"\n   [{i}/{len(news_list)}] Validando: {news.get('title', '')[:60]}...")
            
            validation = self.validate_news(news)
            
            # Agregar validación a la noticia
            news['validation'] = validation
            
            # Verificar si pasa los filtros
            if require_recent and not validation['is_recent']:
                stats['rejected_old'] += 1
                print(f"      ❌ Rechazada: No reciente")
                continue
            
            if validation['relevance_score'] < min_relevance:
                stats['rejected_irrelevant'] += 1
                print(f"      ❌ Rechazada: Relevancia baja ({validation['relevance_score']}/100)")
                continue
            
            if validation['quality_score'] < min_quality:
                stats['rejected_low_quality'] += 1
                print(f"      ❌ Rechazada: Calidad baja ({validation['quality_score']}/100)")
                continue
            
            # Noticia válida
            stats['valid'] += 1
            validated_news.append(news)
            print(f"      ✅ Válida: R={validation['relevance_score']}/100, Q={validation['quality_score']}/100")
            print(f"         Temas: {', '.join(validation['topics_matched'])}")
        
        # Resumen
        print(f"\n   📊 RESULTADO:")
        print(f"      Total procesadas: {stats['total']}")
        print(f"      ✅ Válidas: {stats['valid']}")
        print(f"      ❌ Rechazadas antiguas: {stats['rejected_old']}")
        print(f"      ❌ Rechazadas irrelevantes: {stats['rejected_irrelevant']}")
        print(f"      ❌ Rechazadas baja calidad: {stats['rejected_low_quality']}")
        
        return validated_news


# Ejemplo de uso
if __name__ == "__main__":
    import json
    from pathlib import Path
    
    # Cargar noticias
    news_file = Path("../../data/news.json")
    if news_file.exists():
        with open(news_file, 'r', encoding='utf-8') as f:
            all_news = json.load(f)
        
        print(f"📰 Cargadas {len(all_news)} noticias")
        
        # Crear agente
        agent = NewsValidatorAgent()
        
        # Validar primeras 10 noticias (test)
        validated = agent.validate_batch(
            all_news[:10],
            min_relevance=60,
            min_quality=60,
            require_recent=True
        )
        
        print(f"\n✅ {len(validated)} noticias pasaron la validación")
        
        # Guardar resultado
        output_file = Path("../../data/validated_news.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(validated, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Guardadas en: {output_file}")
