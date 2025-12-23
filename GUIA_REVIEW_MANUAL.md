# 📝 Guía: Sistema de Review Manual y Machine Learning

## 🎯 ¿Qué es esto?

Un sistema que **aprende de tus decisiones** para seleccionar automáticamente noticias que te interesan.

---

## 🔄 Flujo de Trabajo

### **1. Recopilar Noticias**
```bash
python src/main.py collect
```
- Recopila ~80-100 noticias de todas las fuentes
- RSS, Hacker News, Reddit, Dev.to, etc.

---

### **2. Pre-seleccionar Candidatas (Automático)**
```bash
python src/main.py select
```
- El agente filtra y puntúa todas las noticias
- Muestra las **top 12-15** candidatas
- Usa keywords y scoring automático
- **Mínimo 30 puntos** para pasar el filtro

---

### **3. 🆕 Review Manual (TÚ DECIDES)**
```bash
python src/main.py review
```

**Esto es lo nuevo:**

1. **Te muestra cada noticia** con:
   - Título completo
   - Fuente
   - Link
   - Resumen
   - Score actual

2. **Tú decides por cada una:**
   - `s` = **SÍ, me sirve** ✅
   - `n` = **NO me sirve** ❌
   - `x` = Salir

3. **El modelo ML aprende:**
   - Analiza qué noticias aceptas
   - Aprende patrones (palabras, fuentes, temas)
   - Se entrena automáticamente
   - Guarda el modelo en `data/ml_model.pkl`

4. **Guarda las aprobadas:**
   - Solo las que marcaste como "SÍ"
   - En `data/approved_news.json`

---

### **4. Generar Tweets**
```bash
python src/main.py generate
```
- Usa **SOLO las noticias aprobadas**
- Genera tweets en inglés y español
- Hooks conversacionales
- Threads técnicos

---

## 🧠 Machine Learning: Cómo Funciona

### **Primera Vez:**
```
📊 Modelo ML nuevo (se entrenará con tu feedback)
```
- No hay modelo previo
- Aprende desde cero con tus decisiones

### **Siguientes Veces:**
```
✅ Modelo ML cargado (se actualizará con tu feedback)
```
- Carga el modelo entrenado
- Se mejora con cada review
- Acumula conocimiento

---

## 📊 Ejemplo de Review Session

```bash
$ python src/main.py review

======================================================================
📝 REVISIÓN MANUAL DE NOTICIAS
======================================================================

Revisa cada noticia y marca si te sirve o no.
El modelo ML aprenderá de tus decisiones.

✅ Modelo ML cargado (se actualizará con tu feedback)

======================================================================

📰 NOTICIA 1/12
Score actual: 187.0 pts
----------------------------------------------------------------------

📌 Título: Turn Claude Code into a Fullstack web app expert 🔌
📰 Fuente: Dev.to
🔗 Link: https://dev.to/wasp/turn-claude-code-into-a-fullstack...

📝 Resumen:
Get Even More Out of Claude Code with the Wasp Plugin. Batteries-
included frameworks are a game changer...

----------------------------------------------------------------------

¿Esta noticia te sirve? [s=sí / n=no / x=salir]: s
   ✅ Marcada como BUENA

======================================================================

📰 NOTICIA 2/12
Score actual: 88.0 pts
----------------------------------------------------------------------

📌 Título: Fabrice Bellard Releases MicroQuickJS
📰 Fuente: Hacker News
🔗 Link: https://github.com/bellard/mquickjs...

----------------------------------------------------------------------

¿Esta noticia te sirve? [s=sí / n=no / x=salir]: n
   ❌ Marcada como NO RELEVANTE

...

======================================================================
🧠 ENTRENANDO MODELO ML CON TU FEEDBACK
======================================================================

✅ Modelo entrenado con 12 ejemplos
   📊 Aceptadas: 4
   📊 Rechazadas: 8

💾 4 noticias aprobadas guardadas en: data/approved_news.json
   Ejecuta 'python src/main.py generate' para crear tweets

======================================================================
```

---

## 🎓 El Modelo Aprende

### **Qué Analiza:**

1. **Keywords en título y contenido**
   - Palabras que aparecen en noticias que aceptas
   - vs palabras en noticias que rechazas

2. **Fuentes preferidas**
   - Hacker News vs Reddit vs Dev.to
   - Aprende cuáles prefieres

3. **Longitud y estructura**
   - Títulos largos vs cortos
   - Con o sin emojis

4. **Engagement metrics**
   - Score, comentarios, reacciones
   - Aprende qué nivel de engagement te interesa

5. **Temas y categorías**
   - Agentes IA vs Hardware vs Código
   - Lanzamientos vs Noticias genéricas

### **Después de 20-30 reviews:**
- El modelo predice con ~80% de precisión
- Automáticamente filtra mejor
- Menos noticias irrelevantes
- Más noticias que te interesan

---

## 📁 Archivos Generados

```
data/
├── news.json              # Todas las noticias recopiladas (~80)
├── selected_news.json     # Candidatas pre-filtradas (~12-15)
├── approved_news.json     # Las que TÚ aprobaste (~3-5)
├── ai_tweets.json         # Tweets generados
└── ml_model.pkl          # Modelo ML entrenado
```

---

## 🚀 Workflow Completo

### **Opción A: Manual Completo**
```bash
# 1. Recopilar
python src/main.py collect

# 2. Pre-seleccionar
python src/main.py select

# 3. TÚ REVISAS (nuevo)
python src/main.py review

# 4. Generar tweets
python src/main.py generate
```

### **Opción B: Semi-automático**
```bash
# 1-2. Recopilar y pre-seleccionar
python src/main.py collect
python src/main.py select

# 3. TÚ REVISAS
python src/main.py review

# 4. Auto-generar
python src/main.py generate
```

---

## 💡 Tips

### **Primera Vez (Sin Modelo):**
- Revisa al menos **10-15 noticias**
- Sé consistente en tus criterios
- El modelo necesita datos para aprender

### **Con Modelo Entrenado:**
- Revisa **5-10 noticias** regularmente
- El modelo mejora continuamente
- Puedes ser más selectivo

### **Para Entrenar Bien:**
- ✅ **SÍ**: Solo noticias que realmente publicarías
- ❌ **NO**: Todo lo que no te interesa
- 🎯 **Objetivo**: Enseñarle tu criterio específico

---

## 📊 Monitoreo del Modelo

El modelo guarda internamente:
- Features (características) de cada noticia
- Labels (tus decisiones: 1=buena, 0=mala)
- Historial de entrenamiento

Archivo: `data/ml_model.pkl`

---

## 🎯 Resultado Final

**Después de 3-4 semanas:**
- El sistema conoce tus preferencias
- Auto-filtra con ~85% de precisión
- Solo revisas 5-7 noticias en vez de 15
- Generas tweets de calidad consistentemente

**El ML hace el trabajo pesado, tú solo validas.**

---

## ⚡ Comandos Rápidos

```bash
# Flujo completo diario
python src/main.py collect && \
python src/main.py select && \
python src/main.py review && \
python src/main.py generate

# Solo review (si ya tienes noticias)
python src/main.py review
```

---

🚀 **¡Empieza a entrenar tu modelo ahora!**
