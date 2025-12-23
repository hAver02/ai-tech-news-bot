# 🔑 Guía: APIs Gratuitas para Noticias

Guía rápida para obtener API keys de fuentes gratuitas y generosas.

---

## 📊 Comparativa Rápida

| API | Requests Gratis | Idiomas | Registro | Tiempo | Recomendación |
|-----|-----------------|---------|----------|--------|---------------|
| **The Guardian** | 5000/día ⭐⭐⭐⭐⭐ | Inglés | Instantáneo | 2 min | ⭐⭐⭐⭐⭐ |
| **NewsData.io** | 200/día ⭐⭐⭐⭐ | 50+ idiomas | Instantáneo | 2 min | ⭐⭐⭐⭐⭐ |
| **News API** | 100/día ⭐⭐⭐ | Múltiples | Instantáneo | 2 min | ⭐⭐⭐⭐ |
| **NY Times** | 4000/día ⭐⭐⭐⭐⭐ | Inglés | Instantáneo | 3 min | ⭐⭐⭐⭐ |
| **Currents API** | 600/día ⭐⭐⭐⭐ | Múltiples | Instantáneo | 2 min | ⭐⭐⭐⭐ |

---

## 🚀 Guías Rápidas

### 1. The Guardian API (5000 requests/día) ⭐⭐⭐⭐⭐

**Por qué es excelente:**
- ✅ 5000 requests por día (¡súper generoso!)
- ✅ Contenido de alta calidad
- ✅ API simple y bien documentada
- ✅ No requiere tarjeta de crédito

**Cómo obtener la API key:**

1. Ve a: **https://open-platform.theguardian.com/access/**

2. Click en **"Register for a developer key"**

3. Llena el formulario:
   - **First name**: Tu nombre
   - **Last name**: Tu apellido
   - **Email**: Tu email
   - **Company/organization**: `Personal Project` (o como quieras)
   - **Reason for access**: Pon algo como:
     ```
     Building a tech news aggregator bot for personal use.
     Will collect technology, science and business articles.
     ```

4. Acepta los términos y haz click en **"Register"**

5. Te llegará un email con tu API key instantáneamente

6. Agrega a tu `.env`:
   ```bash
   GUARDIAN_API_KEY=tu_api_key_aqui
   ```

**Probar:**
```bash
cd src/collectors
python guardian_collector.py
```

---

### 2. NewsData.io (200 requests/día) ⭐⭐⭐⭐⭐

**Por qué es excelente:**
- ✅ 200 requests por día
- ✅ 50+ idiomas incluido español
- ✅ Noticias de todo el mundo
- ✅ Fácil de usar

**Cómo obtener la API key:**

1. Ve a: **https://newsdata.io/register**

2. Llena el formulario de registro:
   - **Email**: Tu email
   - **Password**: Tu contraseña
   - **Full Name**: Tu nombre

3. Click en **"Sign Up"**

4. Verifica tu email (revisa spam si no llega)

5. Una vez dentro, tu API key aparecerá en el dashboard

6. Agrega a tu `.env`:
   ```bash
   NEWSDATA_API_KEY=tu_api_key_aqui
   ```

**Probar:**
```bash
cd src/collectors
python newsdata_collector.py
```

---

### 3. News API (100 requests/día) - Ya la tienes

**Ya tienes esta configurada**, pero si necesitas otra cuenta:

1. Ve a: **https://newsapi.org/register**
2. Llena el formulario
3. Tu API key aparece instantáneamente
4. Agrega a `.env`:
   ```bash
   NEWS_API_KEY=tu_api_key_aqui
   ```

---

### 4. New York Times API (4000 requests/día) ⭐⭐⭐⭐⭐

**Por qué es excelente:**
- ✅ 4000 requests por día
- ✅ Contenido premium
- ✅ Histórico de artículos
- ✅ Múltiples APIs disponibles

**Cómo obtener la API key:**

1. Ve a: **https://developer.nytimes.com/get-started**

2. Click en **"Sign Up"** o **"Log In"** si tienes cuenta del NYT

3. Llena el formulario de registro

4. Ve a tu dashboard: **https://developer.nytimes.com/my-apps**

5. Click en **"+ New App"**

6. Dale un nombre: `TechNewsBot`

7. Activa la API: **"Article Search API"**

8. Tu API key aparecerá

9. Agrega a tu `.env`:
   ```bash
   NYT_API_KEY=tu_api_key_aqui
   ```

**Nota:** El collector para NYT no está implementado aún, pero puedo crearlo si quieres.

---

### 5. Currents API (600 requests/día) ⭐⭐⭐⭐

**Por qué es excelente:**
- ✅ 600 requests por día
- ✅ Noticias actualizadas constantemente
- ✅ Múltiples idiomas
- ✅ Sin tarjeta de crédito

**Cómo obtener la API key:**

1. Ve a: **https://currentsapi.services/en/register**

2. Llena el formulario:
   - **Email**: Tu email
   - **Password**: Tu contraseña
   - **Full Name**: Tu nombre

3. Click en **"Sign Up"**

4. Verifica tu email

5. Tu API key estará en el dashboard

6. Agrega a tu `.env`:
   ```bash
   CURRENTS_API_KEY=tu_api_key_aqui
   ```

**Nota:** El collector no está implementado, pero puedo crearlo si quieres.

---

## 📝 Resumen de tu archivo .env

Tu archivo `.env` debería verse así:

```bash
# News APIs
NEWS_API_KEY=tu_news_api_key
GUARDIAN_API_KEY=tu_guardian_api_key
NEWSDATA_API_KEY=tu_newsdata_api_key

# Opcional: Más APIs
NYT_API_KEY=tu_nyt_api_key
CURRENTS_API_KEY=tu_currents_api_key

# OpenAI (para generar tweets)
OPENAI_API_KEY=tu_openai_key

# Reddit (opcional - ahora es complicado)
# REDDIT_CLIENT_ID=tu_client_id
# REDDIT_CLIENT_SECRET=tu_secret
# REDDIT_USER_AGENT=TechNewsBot/1.0
```

---

## 🎯 Recomendación de Prioridad

### ⭐ Nivel 1: Implementar AHORA (Lo más fácil)
1. **The Guardian** (5000/día - ¡súper generoso!)
2. **NewsData.io** (200/día - español incluido)

### ⭐⭐ Nivel 2: Implementar después
3. **NY Times** (4000/día - calidad premium)
4. **Currents API** (600/día)

---

## 🔒 Notas de Seguridad

- ❌ **NUNCA** subas tu archivo `.env` a GitHub
- ❌ **NUNCA** compartas tus API keys
- ✅ El `.env` ya está en `.gitignore` por seguridad
- ✅ Si alguien obtiene tu key, regenera una nueva en el dashboard

---

## ✅ Checklist

Marca lo que ya tienes configurado:

- [ ] The Guardian API key configurada
- [ ] NewsData.io API key configurada
- [ ] News API key configurada (ya la tienes)
- [ ] Collectors funcionando
- [ ] Integrado en main.py

---

## 🚀 Próximo Paso

Una vez que tengas las API keys, puedo:

1. **Integrar todos los collectors en `main.py`**
2. **Crear un sistema que use todas las fuentes automáticamente**
3. **Optimizar para que tengas la mayor cobertura posible**

¿Listo para registrarte en estas APIs? ¡Son gratis y toma 2 minutos cada una! 🎯
