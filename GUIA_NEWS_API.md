# 📰 Guía: Cómo Obtener tu News API Key (GRATIS)

News API te da acceso a miles de fuentes de noticias de forma gratuita.

---

## 🎁 Plan Gratuito

- ✅ **100 requests por día** (más que suficiente)
- ✅ Acceso a 80,000+ fuentes
- ✅ Noticias hasta 1 mes de antigüedad
- ✅ No requiere tarjeta de crédito
- ✅ **Totalmente gratis**

---

## 📋 Pasos para Obtener tu API Key

### **Paso 1: Registrarte**

1. Ve a: https://newsapi.org/register
2. Completa el formulario:
   - **Nombre**
   - **Email**
   - **Password**
3. Selecciona "**I'm using this for personal use**"
4. Acepta términos y condiciones
5. Click en "**Submit**"

### **Paso 2: Verificar Email**

1. Revisa tu email
2. Click en el link de verificación

### **Paso 3: Obtener tu API Key**

1. Una vez verificado, verás tu **API Key** en pantalla
2. La key se ve así: `abc123def456...` (32 caracteres)
3. Cópiala

---

## ⚙️ Configurar en tu Proyecto

### **Abrir archivo .env**

```bash
cd /Users/lucianopaz/Desktop/hAver/python-twitter
nano .env
# o
code .env
```

### **Agregar la News API Key**

Tu archivo `.env` debería verse así:

```env
# OpenAI API
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-3.5-turbo

# News API (GRATIS)
NEWS_API_KEY=abc123def456tu_key_aqui
```

### **Guardar el archivo**

---

## 🧪 Probar que Funciona

### **Test 1: Probar solo News API**

```bash
cd /Users/lucianopaz/Desktop/hAver/python-twitter
source venv/bin/activate
python src/collectors/news_api_collector.py
```

Deberías ver:

```
📡 Recopilando desde News API (3 queries)...
  ✅ 'artificial intelligence': 10 noticias
  ✅ 'technology': 10 noticias
  ✅ 'startup': 10 noticias

📊 Total News API: 30 noticias
💾 Noticias de News API guardadas en: data/news_api.json
```

### **Test 2: Probar con todo el sistema**

```bash
python src/main.py collect
```

Ahora verás noticias de **ambas fuentes**:
- RSS Feeds (TechCrunch, Hacker News, etc.)
- News API (miles de fuentes)

---

## ⚙️ Personalizar las Búsquedas

Edita `config/sources.yaml` para cambiar lo que busca:

```yaml
# News API queries
news_api_queries:
  - query: "artificial intelligence"
    language: "en"
    
  - query: "OpenAI OR ChatGPT"
    language: "en"
    
  - query: "inteligencia artificial"
    language: "es"
    
  - query: "Python programming"
    language: "en"
    
  - query: "startup argentina"
    language: "es"
```

**Operadores disponibles:**
- `AND` - ambas palabras deben estar
- `OR` - al menos una palabra
- `NOT` - excluir palabras
- `"exacta"` - frase exacta

**Ejemplos:**
```yaml
- query: "AI AND (OpenAI OR Google)"
- query: "startup NOT crypto"
- query: "\"machine learning\" AND Python"
```

---

## 📊 Límites del Plan Gratuito

| Aspecto | Límite |
|---------|--------|
| **Requests/día** | 100 |
| **Fuentes** | 80,000+ |
| **Antigüedad** | Hasta 1 mes |
| **Results/request** | Hasta 100 |
| **Costo** | $0 (gratis) |

**Para tu uso (2 ejecuciones/día):**
- Cada ejecución = ~3-5 requests
- Total diario = ~6-10 requests
- **Muy por debajo del límite de 100** ✅

---

## 🔄 Actualizar el Sistema

Ya está todo integrado! Solo necesitas:

1. ✅ Agregar tu News API key a `.env`
2. ✅ Ejecutar `python src/main.py collect`
3. ✅ ¡Listo! Tendrás noticias de ambas fuentes

---

## 💡 Tips

### **Filtrar por Fuentes Específicas**

Si quieres solo fuentes tech, puedes filtrar:

```python
# En news_api_collector.py
params = {
    'sources': 'techcrunch,hacker-news,wired,the-verge',
    # ... resto de params
}
```

### **Buscar en Títulos Solamente**

Para búsquedas más precisas:

```python
params = {
    'qInTitle': 'AI',  # Solo en títulos
    # ... resto
}
```

### **Monitorear tu Uso**

Ve a: https://newsapi.org/account

---

## ❓ Solución de Problemas

### **Error: "Missing API key"**

**Solución:**
1. Verifica que agregaste `NEWS_API_KEY` en `.env`
2. Sin espacios: `NEWS_API_KEY=abc123...`
3. Reinicia el script

### **Error: "Invalid API key"**

**Solución:**
1. La key es incorrecta
2. Copia nuevamente desde: https://newsapi.org/account
3. Pégala en `.env`

### **Error: "Rate limit exceeded"**

**Solución:**
Llegaste a las 100 requests del día. Espera hasta mañana o:
1. Reduce `max_results_per_query` en el código
2. Ejecuta menos veces por día

### **Error: "You have requested too many results"**

**Solución:**
El límite es 100 por request. Reduce `max_results_per_query` a 10-20.

---

## 🎯 Resultado Final

Con News API integrado tendrás:

**RSS Feeds:**
- TechCrunch
- Hacker News
- The Verge
- Ars Technica
- Wired

**+**

**News API:**
- 80,000+ fuentes
- Búsquedas personalizadas
- Noticias en español e inglés

= **Mucha más variedad de noticias tech** 🚀

---

## 📞 Recursos

**Website:** https://newsapi.org/  
**Documentación:** https://newsapi.org/docs  
**Dashboard:** https://newsapi.org/account  
**Fuentes disponibles:** https://newsapi.org/sources

---

**¿Listo?** Obtén tu API key gratis y tendrás acceso a miles de noticias tech 🎉

