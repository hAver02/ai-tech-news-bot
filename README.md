# 🤖 AI Tech News Tweet Generator

Sistema inteligente que **recopila noticias tecnológicas**, las **filtra con ML**, y genera **tweets técnicos profesionales** en inglés y español.

---

## ✨ Características

### 🔍 **Recopilación Multi-Fuente**
- ✅ **57 RSS feeds** (blogs oficiales de empresas tech)
- ✅ **Hacker News** API (top stories)
- ✅ **Dev.to** API (artículos técnicos)
- ✅ **News API** (noticias tech globales)
- ❌ Reddit desactivado (fuentes no oficiales)

### 🧠 **Machine Learning + Filtrado Inteligente**
- ✅ Sistema de **scoring automático** por keywords
- ✅ **Review manual** con entrenamiento continuo
- ✅ El modelo **aprende** de tus decisiones
- ✅ Mejora automáticamente con cada uso

### 🐦 **Generación de Tweets con IA (OpenAI)**
- ✅ **Hooks conversacionales** que generan engagement
- ✅ **Threads técnicos** explicativos y educativos
- ✅ **Bilingüe** (inglés y español)
- ✅ Estilo **directo y profesional**
- ✅ Incluye **links** a fuentes originales

---

## 🏢 Fuentes Oficiales

### **Agentes IA & Dev Tools**
- OpenAI Blog, Anthropic (Claude), Vercel, Cursor
- Supabase, Prisma, GitHub, Replit

### **Lenguajes & Frameworks**
- TypeScript, Rust, Python, React, Node.js, Deno

### **Empresas Tech**
- Google AI, Microsoft Developer, Meta Engineering
- Netflix Tech, Uber Engineering, Airbnb Engineering
- Stripe, Cloudflare

### **Hardware**
- Nvidia Blog, Intel Newsroom

---

## 🚀 Instalación

### **1. Requisitos**
```bash
Python 3.8+
pip
virtualenv (opcional pero recomendado)
```

### **2. Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/python-twitter.git
cd python-twitter
```

### **3. Crear entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### **4. Instalar dependencias**
```bash
pip install -r requirements.txt
```

### **5. Configurar variables de entorno**
```bash
cp env.example .env
```

**Edita `.env` y agrega tus API keys:**
```bash
OPENAI_API_KEY=tu_clave_openai
NEWS_API_KEY=tu_clave_newsapi  # Opcional
```

---

## 📖 Uso

### **Flujo Completo**

#### **1. Recopilar Noticias**
```bash
python src/main.py collect
```
- Recopila ~50-80 noticias de todas las fuentes
- Guarda en `data/news.json`

#### **2. Pre-seleccionar Candidatas**
```bash
python src/main.py select
```
- Filtra y puntúa automáticamente
- Muestra top 12-15 candidatas
- Guarda en `data/selected_news.json`

#### **3. 🆕 Review Manual (Entrenar ML)**
```bash
python src/main.py review
```
- **TÚ decides** qué noticias sirven
- El **modelo ML aprende** de tus decisiones
- Guarda aprobadas en `data/approved_news.json`
- Entrena y mejora automáticamente

#### **4. Generar Tweets**
```bash
python src/main.py generate
```
- Genera tweets con OpenAI GPT
- Solo para noticias aprobadas
- Formato: hooks + threads técnicos
- Bilingüe (inglés y español)
- Guarda en `data/ai_tweets.json`

---

## 🔄 Flujo Diario Recomendado

```bash
# Opción A: Paso a paso
python src/main.py collect
python src/main.py select
python src/main.py review    # TÚ DECIDES
python src/main.py generate

# Opción B: Todo automático (sin review)
python src/main.py all
```

---

## 📊 Estructura del Proyecto

```
python-twitter/
├── src/
│   ├── main.py                    # Entry point
│   ├── agent.py                   # Agente selector
│   ├── collectors/                # Recopiladores
│   │   ├── rss_collector.py
│   │   ├── hackernews_collector.py
│   │   └── devto_collector.py
│   ├── generators/                # Generadores de tweets
│   │   └── ai_tweet_generator.py
│   ├── llm/                       # OpenAI provider
│   │   └── openai_provider.py
│   ├── ml/                        # Machine Learning
│   │   └── news_selector_model.py
│   └── utils/                     # Utilidades
│       ├── news_filter.py
│       ├── news_scorer.py
│       └── content_enricher.py
├── config/
│   ├── sources.yaml               # RSS feeds y fuentes
│   └── priorities.yaml            # Keywords y scoring
├── data/                          # Datos generados
│   ├── news.json
│   ├── selected_news.json
│   ├── approved_news.json
│   ├── ai_tweets.json
│   └── ml_model.pkl
├── requirements.txt
├── .env                           # API keys (NO subir)
└── README.md
```

---

## 🧠 Machine Learning

### **¿Cómo Funciona?**

1. **Primera Review:**
   - Marcas 10-15 noticias como buenas/malas
   - El modelo analiza patrones
   - Entrena y guarda (`ml_model.pkl`)

2. **Siguientes Reviews:**
   - Carga el modelo previo
   - Aprende de nuevas decisiones
   - Mejora continuamente

3. **Después de 20-30 Reviews:**
   - Predice con ~80% de precisión
   - Auto-filtra mejor
   - Menos trabajo manual

### **Features que Analiza:**
- Keywords en título y contenido
- Fuente de la noticia
- Engagement (score, comentarios)
- Longitud del título
- Categorías y tags

---

## ⚙️ Configuración Avanzada

### **Ajustar Prioridades**

Edita `config/priorities.yaml`:

```yaml
# Keywords de ULTRA ALTA prioridad
ultra_high_priority_keywords:
  - "TypeScript 6"
  - "Next.js 16"
  - "Cursor IDE"
  - "v0 by Vercel"

# Score mínimo para pasar el filtro
scoring:
  min_score: 30  # Aumenta para ser más estricto
```

### **Agregar Fuentes RSS**

Edita `config/sources.yaml`:

```yaml
rss_feeds:
  - name: "Mi Blog Favorito"
    url: "https://ejemplo.com/feed.xml"
    category: "tech"
```

---

## 🎯 Temas Prioritarios

El sistema está optimizado para:

1. **Agentes IA**: Cursor, Lovable, Claude, OpenAI, Vercel, Replit
2. **Hardware**: GPU/RAM shortage, TSMC, Nvidia, Intel, AMD
3. **Código/DB**: TypeScript, Supabase, Prisma, Python, Rust, React
4. **Lanzamientos**: Nuevas versiones, releases, announces

---

## 📝 Ejemplo de Output

### **Hook Generado:**
```
Microsoft quiere eliminar todo su código de C/C++.

¿Con qué lo sustituyen? Rust.

1 ingeniero, 1 mes, 1M líneas.

Objetivo: 2030. ¿Cómo lo ves?
```

### **Thread Técnico:**
```
1/3 Microsoft está migrando todo su código base de C/C++ a Rust 
para mejorar seguridad de memoria y rendimiento.

2/3 Rust ofrece mayor seguridad sin sacrificar velocidad. El cambio
afectará millones de líneas de código en productos clave.

3/3 Este movimiento podría marcar un antes y después en la industria. 
¿Veremos más empresas siguiendo el ejemplo?

🔗 https://thurrott.com/...
```

---

## 🤝 Contribuir

¡Contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📄 Licencia

MIT License - ver archivo `LICENSE`

---

## 🔗 Links Útiles

- [Guía de Review Manual](GUIA_REVIEW_MANUAL.md)
- [Guía de APIs Gratuitas](GUIA_APIS_GRATUITAS.md)
- [Guía ML + Enrichment](GUIA_ML_ENRIQUECIMIENTO.md)
- [OpenAI API Docs](https://platform.openai.com/docs)

---

## 🚀 Estado del Proyecto

- ✅ Recopilación multi-fuente
- ✅ Filtrado inteligente con scoring
- ✅ Machine Learning con feedback loop
- ✅ Generación de tweets bilingües
- ✅ Review manual interactivo
- ⏳ Publicación automática en Twitter (próximamente)
- ⏳ Dashboard web (próximamente)

---

## 💡 Tips

### **Para Mejores Resultados:**
1. Haz review de al menos 15-20 noticias inicialmente
2. Sé consistente en tus criterios
3. Revisa regularmente para mantener el modelo actualizado
4. Ajusta `min_score` según tus necesidades

### **Troubleshooting:**
- Si hay pocas noticias: Baja el `min_score` en `priorities.yaml`
- Si hay demasiadas: Aumenta el `min_score`
- Para más fuentes: Agrega RSS feeds en `sources.yaml`

---

**⭐ Si te gusta el proyecto, dale una estrella en GitHub!**

---

Hecho con ❤️ por [luchi](https://github.com/tu-usuario)
