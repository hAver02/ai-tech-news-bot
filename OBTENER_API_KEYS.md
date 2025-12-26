# 🔑 Cómo Obtener API Keys para Noticias en Tiempo Real

## 🎯 **RESUMEN EJECUTIVO:**

Para tener **noticias de últimas horas**, necesitas al menos **1 de estas 2 keys**:

1. **Tavily AI** (RECOMENDADO) - $14/mes después de 1000 gratis
2. **Serper API** (Alternativa) - 2500 gratis/mes

---

## 🥇 **TAVILY AI** (Mejor para tiempo real)

### ⏱️ Tiempo: 5 minutos

### 📋 Pasos:

1. **Abre:** https://tavily.com
2. **Sign Up:**
   - Click en "Get Started" o "Try for Free"
   - Usa Google/GitHub o email
3. **Dashboard:**
   - Ve a: https://app.tavily.com
   - Click en "API Keys" (menú izquierdo)
4. **Copia tu key:**
   - Formato: `tvly-xxxxxxxxxx`
5. **Agrégala al `.env`:**
   ```bash
   TAVILY_API_KEY=tvly-xxxxxxxxxx
   ```

### 💰 Costo:
- ✅ **1,000 búsquedas GRATIS/mes**
- Después: $14/mes (ilimitadas)
- O $0.001 por búsqueda (pay-as-you-go)

### 📊 Volumen estimado:
- 10 búsquedas cada 30 min = 480/día
- Con tier gratis: **2 días de uso**
- Con pago: **$14/mes** (ilimitado)

---

## 🥈 **SERPER API** (Google Search)

### ⏱️ Tiempo: 3 minutos

### 📋 Pasos:

1. **Abre:** https://serper.dev
2. **Sign Up:**
   - Click en "Get Started Free"
   - Email + contraseña
3. **Confirma email:**
   - Revisa tu inbox
   - Click en link de confirmación
4. **Dashboard:**
   - Automáticamente te muestra tu API Key
5. **Copia tu key**
6. **Agrégala al `.env`:**
   ```bash
   SERPER_API_KEY=xxxxxxxxxx
   ```

### 💰 Costo:
- ✅ **2,500 búsquedas GRATIS/mes**
- Después: $50 por 10,000 búsquedas ($0.005 c/u)

### 📊 Volumen estimado:
- 10 búsquedas cada 30 min = 480/día
- Con tier gratis: **5 días de uso**
- Con pago: $15-20/mes

---

## 🎁 **BONUS: Product Hunt** (Lanzamientos del día)

### ⏱️ Tiempo: 10 minutos (OAuth más complejo)

### 📋 Pasos:

1. **Abre:** https://api.producthunt.com/v2/oauth/applications
2. **Sign Up** en Product Hunt
3. **Create Application:**
   - Name: "python-twitter"
   - Redirect URI: http://localhost:8000/callback
4. **Obtén credenciales:**
   - Client ID
   - Client Secret
5. **OAuth Flow** (requiere código adicional)

### 💰 Costo:
- ✅ **100% GRATIS**

### 📌 Nota:
- Requiere implementar OAuth (más complejo)
- Lo dejamos como opcional

---

## 🚫 **NO NECESITAS (Ya están gratis):**

Estas fuentes **NO requieren API keys**:
- ✅ Algolia HN (búsqueda avanzada HN)
- ✅ GitHub Trending (repos del día)
- ✅ Hacker News oficial (ya lo tienes)
- ✅ Dev.to (ya lo tienes)

---

## 📝 **TU `.env` FINAL:**

```bash
# === APIs EXISTENTES ===
OPENAI_API_KEY=sk-xxxxx
NEWS_API_KEY=xxxxx
NEWSDATA_API_KEY=xxxxx
GUARDIAN_API_KEY=xxxxx

# === NUEVAS APIS TIEMPO REAL ===
# (Agrega las que consigas)

# Tavily AI (RECOMENDADO)
TAVILY_API_KEY=tvly-xxxxx

# Serper (ALTERNATIVA/COMPLEMENTO)
SERPER_API_KEY=xxxxx

# Product Hunt (OPCIONAL)
PRODUCTHUNT_API_KEY=xxxxx
```

---

## ✅ **DESPUÉS DE AGREGAR LAS KEYS:**

### **Test rápido:**

```bash
# 1. Activa entorno
source venv/bin/activate

# 2. Prueba Tavily (si la agregaste)
python src/collectors/tavily_collector.py

# 3. Prueba Serper (si la agregaste)
python src/collectors/serper_collector.py

# 4. Ejecuta recopilador continuo
python src/main.py watch
```

---

## 🎯 **MI RECOMENDACIÓN:**

### **Para empezar (Costo $0):**

1. Consigue **Serper** (2500 gratis/mes)
2. Prueba el sistema por 1 semana
3. Si necesitas más, agrega **Tavily**

### **Para producción (Costo $14-29/mes):**

1. **Tavily AI** ($14/mes) - búsqueda principal
2. **Serper** (gratis hasta 2500, luego pago) - complemento

---

## ❓ **¿Cuál conseguir primero?**

| Si buscas... | Consigue |
|--------------|----------|
| **Gratis máximo tiempo** | Serper (2500/mes gratis) |
| **Mejor calidad** | Tavily ($14/mes) |
| **Ambas** | Las 2 (mejor cobertura) |

---

## 🔥 **CUANDO TENGAS LAS KEYS:**

Avísame y ejecutamos:

```bash
python src/main.py watch
```

Y verás **noticias de últimas 4 horas** en tiempo real! 🚀
