"""
OpenAI Provider - Integración con OpenAI GPT

Este módulo maneja toda la interacción con la API de OpenAI:
- Scoring inteligente de noticias
- Generación de múltiples versiones de tweets
"""

from openai import OpenAI
from typing import List, Dict
import json


class OpenAIProvider:
    """
    Proveedor de OpenAI para scoring y generación de tweets.
    
    Este proveedor usa GPT para:
    1. Calificar noticias de forma inteligente
    2. Generar 3 versiones de tweets por noticia
    """
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Inicializa el proveedor de OpenAI.
        
        Args:
            api_key: Tu API key de OpenAI
            model: Modelo a usar (gpt-3.5-turbo, gpt-4, gpt-4-turbo, etc.)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        
    def score_news(self, title: str, summary: str, source: str = "") -> Dict:
        """
        Califica una noticia usando GPT.
        
        Args:
            title: Título de la noticia
            summary: Resumen/descripción
            source: Fuente de la noticia
            
        Returns:
            Dict con score y razón
        """
        
        prompt = f"""Eres un experto en noticias tecnológicas y startups.

Califica esta noticia de 0 a 100 según:
- Relevancia para la comunidad tech
- Importancia del tema
- Novedad/actualidad
- Impacto en la industria

Noticia:
Título: {title}
Resumen: {summary}
Fuente: {source}

Responde SOLO en formato JSON:
{{
    "score": <número del 0-100>,
    "reason": "<breve razón en español>"
}}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un experto analista de noticias tech."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Bajo para ser consistente
                max_tokens=150
            )
            
            result = response.choices[0].message.content.strip()
            
            # Parsear JSON
            data = json.loads(result)
            
            return {
                'score': float(data.get('score', 0)),
                'reason': data.get('reason', 'Sin razón'),
                'model_used': self.model
            }
            
        except Exception as e:
            print(f"⚠️  Error en scoring con OpenAI: {str(e)}")
            return {
                'score': 0,
                'reason': f'Error: {str(e)}',
                'model_used': self.model
            }
    
    def generate_tweet_thread(
        self,
        title: str,
        summary: str,
        full_content: str = "",
        source: str = "",
        link: str = ""
    ) -> List[Dict]:
        """
        Genera UN THREAD técnico y explicativo (puede ser múltiples tweets).
        
        Args:
            title: Título de la noticia
            summary: Resumen
            full_content: Contenido completo (si está disponible)
            source: Fuente
            
        Returns:
            Lista de tweets (thread) con formato simplificado
        """
        
        # Combinar toda la información disponible
        content_for_analysis = f"{title}\n\n{summary}"
        if full_content:
            content_for_analysis += f"\n\n{full_content[:2000]}"  # Max 2000 chars
        
        prompt = f"""Eres un ANALISTA TÉCNICO que explica noticias tech de forma DIRECTA, CONVERSACIONAL y CON DATOS CONCRETOS.

Noticia:
{content_for_analysis}

Fuente: {source}

Tu misión: EXPLICAR QUÉ PASÓ de forma directa con datos, nombres propios y preguntas que generen interacción.

ESTILO REQUERIDO:
- AFIRMACIONES DIRECTAS con datos concretos
- NOMBRES PROPIOS y cifras específicas
- PUNTOS con símbolos (✓, ①②③, →)
- PÁRRAFOS CORTOS y separados
- PREGUNTAS RETÓRICAS y finales para engagement
- Lenguaje conversacional pero profesional
- NO incluyas URLs ni links
- NO uses hashtags
- NO abuses de emojis

TEMAS PRIORITARIOS (enfócate si aplica):
• Agentes IA: Cursor, Lovable, Claude, OpenAI, Vercel, Gemini
• Hardware: componentes, escasez (RAM), cierres de fábricas, conflictos
• Código/DB: TypeScript, Supabase, Python, nuevas librerías
• Ciberseguridad, Cloud/DevOps, Startups tech

HOOK INICIAL (MUY IMPORTANTE):
- Genera un HOOK CORTO, DIRECTO e IMPACTANTE
- Máximo 2-3 líneas cortas
- Usa un TONO CONVERSACIONAL y profesional
- Incluye PREGUNTAS RETÓRICAS si aplica
- USA SÍMBOLOS: ✓, ①②③, →, • (no abuses de emojis)
- Termina con PREGUNTA para engagement: "¿Cómo lo ves?", "¿Qué opinas?", "¿Te lo esperabas?"

EJEMPLOS DE BUEN ESTILO (basado en tu cuenta):
  ✅ "Microsoft quiere eliminar todo su código de C y C++.\n\n¿Y con qué lo van a sustituir? Rust.\n\n1 ingeniero, 1 mes, 1 millón de líneas.\n\nObjetivo 2030. ¿Cómo lo ves?"
  
  ✅ "Por qué la IA no sustituye a Programadores Junior.\n\nExplicado por el CEO de AWS Matt Garman:\n\n① Dominan mejor las herramientas de IA\n② Menos caros\n③ Rompe la cadena de talento\n\n¿Qué opinas?"
  
  ✅ "OpenAI acaba de revelar datos preocupantes.\n\nReportes de explotación infantil aumentaron 300% este año.\n\nLa IA generativa tiene un lado oscuro.\n\n¿Qué medidas tomarías?"

FORMATO:
- Párrafos cortos y separados
- Datos concretos y nombres propios
- Pregunta final para interacción
- Profesional pero accesible

FORMATO DEL THREAD:
- Si cabe en 1 tweet (280 chars): un solo tweet (SIN incluir el hook en el texto)
- Si necesitas más: divide en 2-4 tweets numerados
- Los tweets NO deben incluir el hook (va separado)
- USA PUNTOS CON SÍMBOLOS: ✓, ①②③, → para listar
- PÁRRAFOS CORTOS, separados con línea en blanco
- DATOS CONCRETOS y nombres propios
- Estilo CONVERSACIONAL y directo

GENERA AMBAS VERSIONES (Inglés Y Español):

RESPONDE SOLO ESTE JSON:
{{
  "hook_english": "Microsoft wants to eliminate all C/C++ code.\n\nReplacing it with Rust.\n\n1 engineer, 1 month, 1M lines.\n\nTarget: 2030. What do you think?",
  "thread_english": [
    "1/3 [explicación directa con puntos ✓ o ①②③]",
    "2/3 [continuación con datos concretos]",
    "3/3 [final con implicaciones]"
  ],
  "hook_spanish": "Microsoft quiere eliminar todo su código de C/C++.\n\n¿Con qué lo sustituyen? Rust.\n\n1 ingeniero, 1 mes, 1M líneas.\n\nObjetivo: 2030. ¿Cómo lo ves?",
  "thread_spanish": [
    "1/3 [explicación directa con puntos ✓ o ①②③]",
    "2/3 [continuación con datos concretos]",
    "3/3 [final con implicaciones]"
  ]
}}

IMPORTANTE: 
- Cada tweet debe tener máximo 280 caracteres
- El HOOK va SEPARADO (no en el texto del tweet)
- El hook debe ser CORTO (máximo 3-4 líneas cortas)
- Usa \\n\\n para separar párrafos en el hook
- Ambas versiones (inglés y español) deben tener el mismo número de tweets
- Numera los tweets si son más de 1 (ej: "1/3 ...", "2/3 ...", "3/3 ...")
- TERMINA el hook con pregunta: "¿Cómo lo ves?", "What do you think?", etc."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a technical analyst who explains tech news in depth. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,  # Balance creatividad/precisión
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            result = response.choices[0].message.content.strip()
            
            # Parsear JSON
            try:
                data = json.loads(result)
            except json.JSONDecodeError:
                import re
                json_match = re.search(r'\{.*\}', result, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group())
                else:
                    raise
            
            # Crear los tweets de ambos threads (inglés y español)
            hook_english = data.get('hook_english', '').strip()
            thread_english = data.get('thread_english', [])
            hook_spanish = data.get('hook_spanish', '').strip()
            thread_spanish = data.get('thread_spanish', [])
            tweets = []
            
            # Thread en inglés
            for i, tweet_text in enumerate(thread_english, 1):
                tweets.append({
                    'hook': hook_english,
                    'text': tweet_text.strip(),
                    'link': link,
                    'source': source,
                    'language': 'en',
                    'thread_position': f"{i}/{len(thread_english)}",
                    'is_thread': len(thread_english) > 1
                })
            
            # Thread en español
            for i, tweet_text in enumerate(thread_spanish, 1):
                tweets.append({
                    'hook': hook_spanish,
                    'text': tweet_text.strip(),
                    'link': link,
                    'source': source,
                    'language': 'es',
                    'thread_position': f"{i}/{len(thread_spanish)}",
                    'is_thread': len(thread_spanish) > 1
                })
            
            return tweets
            
        except Exception as e:
            print(f"⚠️  Error generando thread con OpenAI: {str(e)}")
            
            # Fallback simple
            return [{
                'text': f"{title}\n\n{summary[:200]}",
                'source': source,
                'thread_position': "1/1",
                'is_thread': False,
                'error': str(e)
            }]


# Ejemplo de uso
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    # Cargar API key
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("⚠️  No se encontró OPENAI_API_KEY en .env")
        exit(1)
    
    # Crear proveedor
    provider = OpenAIProvider(api_key)
    
    # Ejemplo de noticia
    title = "OpenAI launches GPT-4 Turbo with 128K context window"
    summary = "OpenAI announced GPT-4 Turbo, featuring a 128,000 token context window, improved instruction following, and lower pricing."
    link = "https://openai.com/blog/gpt-4-turbo"
    
    print("🧠 Calificando noticia con GPT...")
    score_result = provider.score_news(title, summary)
    print(f"   Score: {score_result['score']}/100")
    print(f"   Razón: {score_result['reason']}")
    
    print("\n📝 Generando 3 versiones de tweets...")
    versions = provider.generate_tweet_versions(title, summary, link)
    
    for v in versions:
        print(f"\n{'='*60}")
        print(f"Versión {v['version']}: {v['style']}")
        print(f"Audiencia: {v['audience']}")
        print(f"{'='*60}")
        print(v['text'])
        print(f"\nCaracteres: {len(v['text'])}/280")

