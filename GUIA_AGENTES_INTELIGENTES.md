# 🤖 Guía: Agentes Inteligentes

## 🎯 ¿Qué Son?

Dos agentes **super inteligentes** que mejoran drásticamente la calidad y frescura de las noticias:

### **Agente 1: Validador LLM** 🧠
Usa **OpenAI GPT** para analizar cada noticia y determinar:
- ✅ ¿Es **reciente**? (últimas 24h)
- ✅ ¿Es **relevante** para tus temas? (AI, Hardware, Código)
- ✅ ¿Tiene **calidad técnica**?
- ✅ ¿Qué **temas** coinciden?

### **Agente 2: Recopilador Continuo** 🔄
Busca noticias **constantemente** (cada 30 min):
- ✅ Solo noticias de **últimas 2-4 horas**
- ✅ Fuentes en **tiempo real** (HN new, Dev.to latest)
- ✅ Detecta **duplicados**
- ✅ Ejecución **automática**

---

## 🚀 Uso

### **1. Validar Noticias con LLM**

```bash
# 1. Recopilar noticias normalmente
python src/main.py collect

# 2. Validar con el agente LLM
python src/main.py validate
```

**¿Qué hace?**
- Analiza cada noticia con GPT
- Descarta antiguas o irrelevantes
- Asigna scores de relevancia y calidad
- Guarda solo las mejores en `data/validated_news.json`

**Ejemplo de output:**
```
🤖 AGENTE VALIDADOR LLM
   Validando 85 noticias...

   [1/85] Validando: Nvidia buying AI chip startup Groq...
      ✅ Válida: R=95/100, Q=90/100
         Temas: Hardware, AI chips, Acquisitions

   [2/85] Validando: E-scooter history London...
      ❌ Rechazada: Relevancia baja (20/100)

   📊 RESULTADO:
      ✅ Válidas: 15
      ❌ Rechazadas antiguas: 20
      ❌ Rechazadas irrelevantes: 40
      ❌ Rechazadas baja calidad: 10
```

---

### **2. Recopilador Continuo (Modo Watch)**

```bash
python src/main.py watch
```

**¿Qué hace?**
- Busca noticias cada 30 minutos
- Solo trae las MÁS RECIENTES (últimas 4h)
- Evita duplicados automáticamente
- Se detiene cuando le digas (o Ctrl+C)

**Prompt interactivo:**
```
🔄 Iniciando Agente Recopilador Continuo...

¿Cuántas horas quieres que busque noticias?
  0 = infinito (hasta Ctrl+C)
  1-24 = horas específicas

Horas: 2
```

**Ejemplo de output:**
```
🔄 AGENTE RECOPILADOR CONTINUO INICIADO
   Interval: cada 30 minutos
   Antigüedad máxima: 4 horas
   Duración: 2 horas

======================================================================
🔄 ITERACIÓN #1
   2025-12-24 19:30:00
======================================================================

🔄 AGENTE RECOPILADOR CONTINUO
   Buscando noticias de las últimas 4 horas...

   📡 Hacker News (new stories - tiempo real)
      ✅ 50 historias nuevas

   📡 Dev.to (latest articles)
      ✅ 20 artículos nuevos

   📊 RESULTADO:
      🆕 Nuevas: 25
      🔄 Duplicadas: 30
      ⏰ Antiguas: 15

   💾 Guardadas en: data/realtime_news.json

⏸️  Esperando 30 minutos...

======================================================================
🔄 ITERACIÓN #2
   2025-12-24 20:00:00
======================================================================
...
```

---

## 📋 Workflow Completo

### **Opción A: Con Validación LLM (Recomendado)**

```bash
# 1. Recopilar noticias (85 noticias)
python src/main.py collect

# 2. Validar con LLM (→ 15 noticias de calidad)
python src/main.py validate

# 3. Seleccionar las mejores
python src/main.py select

# 4. Review manual (entrenar ML)
python src/main.py review

# 5. Generar tweets
python src/main.py generate
```

**Resultado:**
- Solo noticias **recientes** (<24h)
- Solo noticias **relevantes** (>60/100)
- Solo noticias de **calidad** (>60/100)
- **Mejor eficiencia** en review manual

---

### **Opción B: Modo Continuo (Para tener siempre noticias frescas)**

```bash
# Terminal 1: Recopilador continuo (déjalo corriendo)
python src/main.py watch

# Terminal 2: Cada hora, procesar las nuevas
python src/main.py validate
python src/main.py select
python src/main.py review
python src/main.py generate
```

**Resultado:**
- Noticias **ultra frescas** (<4h)
- Actualización **continua**
- **Sin duplicados**
- Cero trabajo manual

---

## ⚙️ Configuración

### **Agente Validador LLM**

Edita `src/agents/news_validator_agent.py`:

```python
# Filtros
min_relevance = 60    # Aumenta para ser más estricto
min_quality = 60      # Aumenta para más calidad
require_recent = True # False = acepta noticias antiguas

# Temas prioritarios (personaliza)
self.priority_topics = [
    "Agentes IA (Cursor, Claude, OpenAI)",
    "Hardware (Nvidia, AMD, Intel)",
    "TypeScript, Rust, Python",
    # Agrega los tuyos
]
```

---

### **Agente Recopilador Continuo**

Edita `src/agents/continuous_collector_agent.py`:

```python
agent = ContinuousCollectorAgent(
    interval_minutes=30,  # Cambiar frecuencia
    max_age_hours=4       # Cambiar antigüedad máxima
)
```

---

## 💡 Casos de Uso

### **Caso 1: Necesito solo lo MÁS reciente**

```bash
# Recopilador continuo (solo últimas 4h)
python src/main.py watch

# Duración: 1 hora
# Resultado: 10-20 noticias ultra frescas
```

---

### **Caso 2: Quiero filtrado inteligente**

```bash
# Recopilación normal
python src/main.py collect

# Validación LLM (descarta 70% basura)
python src/main.py validate

# Resultado: Solo 15 noticias de calidad
```

---

### **Caso 3: Sistema autónomo 24/7**

```bash
# Cron job: cada hora
0 * * * * cd /path && source venv/bin/activate && python src/main.py watch

# O usa systemd service (Linux)
# O launchd (macOS)
```

---

## 📊 Comparativa

| Método | Noticias | Calidad | Frescura | Duplicados |
|--------|----------|---------|----------|------------|
| **Sin agentes** | 85 | Media | 24h | Algunos |
| **Con Validador** | 15 | Alta | <24h | Pocos |
| **Con Continuo** | 25/30min | Alta | <4h | 0 |
| **Ambos** | 10-15 | Muy Alta | <4h | 0 |

---

## 🎯 Ventajas

### **Validador LLM:**
- ✅ **Calidad garantizada** (GPT analiza c/u)
- ✅ **Relevancia alta** (tus temas específicos)
- ✅ **Menos basura** (descarta 70-80%)
- ✅ **Ahorra tiempo** en review manual

### **Recopilador Continuo:**
- ✅ **Ultra fresco** (<4h)
- ✅ **Automático** (corre solo)
- ✅ **Sin duplicados** (tracking inteligente)
- ✅ **Escalable** (ajusta frecuencia)

---

## 🔥 Combinación Poderosa

```bash
# Setup una vez
python src/main.py watch  # Terminal 1 (déjalo corriendo)

# Cada hora (automatiza con cron)
python src/main.py validate
python src/main.py select
python src/main.py review
python src/main.py generate
```

**Resultado:**
- **10-15 noticias** de **altísima calidad**
- **Ultra frescas** (<4h)
- **Cero duplicados**
- **Totalmente automatizable**

---

## 💰 Costos

### **Validador LLM:**
- Usa OpenAI GPT-3.5-turbo
- ~200 tokens por noticia
- 85 noticias = ~17,000 tokens
- Costo: **~$0.02 por validación**

### **Recopilador Continuo:**
- Solo APIs gratuitas
- Costo: **$0**

**Total diario (con validación):**
- 3 validaciones/día = **$0.06/día**
- **$1.80/mes**

---

## 🆘 Troubleshooting

### **Validador no funciona:**
```bash
# Verifica OpenAI API key
grep OPENAI_API_KEY .env
```

### **Recopilador no detecta duplicados:**
```bash
# Elimina cache
rm data/seen_urls.txt
```

### **Muy pocas noticias pasan validación:**
```python
# Baja los filtros en validate
min_relevance = 40  # Era 60
min_quality = 40    # Era 60
```

---

🚀 **¡Disfruta de noticias de máxima calidad y frescura!**
