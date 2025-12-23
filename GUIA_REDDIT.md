# 🔑 Guía: Cómo Obtener Credenciales de Reddit API

Esta guía te mostrará paso a paso cómo obtener tus credenciales de Reddit para usar el **Reddit Collector**.

## ¿Por qué Reddit?

Reddit es una excelente fuente de noticias tecnológicas porque:
- ✅ **Gratis y sin límites estrictos** para uso básico
- ✅ **Comunidad activa** que filtra contenido de calidad (upvotes/downvotes)
- ✅ **Noticias en tiempo real** - a veces antes que medios tradicionales
- ✅ **Discusiones valiosas** en los comentarios

## 📋 Requisitos

- Una cuenta de Reddit (si no tienes, créala en [reddit.com](https://www.reddit.com))
- 5 minutos de tu tiempo

---

## 🚀 Paso a Paso: Crear una Aplicación en Reddit

### **Paso 1: Iniciar Sesión**
1. Ve a [reddit.com](https://www.reddit.com)
2. Inicia sesión con tu cuenta

### **Paso 2: Ir a Preferencias de Apps**
1. Ve directamente a: **https://www.reddit.com/prefs/apps**
   - O navega: Click en tu perfil → Settings → Safety & Privacy → Manage third-party app authorization
2. Baja hasta el final de la página
3. Click en el botón **"create another app..."** o **"are you a developer? create an app..."**

### **Paso 3: Completar el Formulario**

Llena los campos así:

| Campo | Qué poner |
|-------|-----------|
| **name** | `TechNewsBot` (o cualquier nombre que quieras) |
| **App type** | ⚠️ **IMPORTANTE**: Selecciona **"script"** (no web app) |
| **description** | `Bot para recopilar noticias tecnológicas` (opcional) |
| **about url** | Déjalo vacío (opcional) |
| **redirect uri** | `http://localhost:8080` (requerido, pero no lo usaremos) |

**⚠️ MUY IMPORTANTE:** Selecciona el tipo **"script"** - este es el correcto para bots y scripts

### **Paso 4: Crear la App**
1. Click en **"create app"** al final del formulario
2. ¡Listo! Tu app está creada

### **Paso 5: Copiar las Credenciales**

Ahora verás tu app creada con esta información:

```
TechNewsBot                          [edit] [delete]
personal use script
--------------------
[una cadena de caracteres aquí]     ← Este es tu CLIENT_ID
--------------------
secret: [otra cadena de caracteres]  ← Este es tu CLIENT_SECRET
```

**🔑 Identifica tus credenciales:**

1. **CLIENT_ID**: Es la cadena de ~14 caracteres debajo de "personal use script"
   - Ejemplo: `a1b2c3d4e5f6g7`

2. **CLIENT_SECRET**: Es la cadena más larga al lado de "secret:"
   - Ejemplo: `X1Y2Z3A4B5C6D7E8F9G0H1I2J3K4L5`

---

## 📝 Paso 6: Agregar las Credenciales a tu Proyecto

### Opción A: Usando archivo `.env` (Recomendado)

1. Abre tu archivo `.env` (o crea uno si no existe)

2. Agrega estas líneas:

```bash
# Reddit API Credentials
REDDIT_CLIENT_ID=a1b2c3d4e5f6g7
REDDIT_CLIENT_SECRET=X1Y2Z3A4B5C6D7E8F9G0H1I2J3K4L5
REDDIT_USER_AGENT=TechNewsBot/1.0
```

3. **Reemplaza** los valores de ejemplo con tus credenciales reales

4. Guarda el archivo

### Opción B: Variables de entorno (Terminal)

```bash
export REDDIT_CLIENT_ID="a1b2c3d4e5f6g7"
export REDDIT_CLIENT_SECRET="X1Y2Z3A4B5C6D7E8F9G0H1I2J3K4L5"
export REDDIT_USER_AGENT="TechNewsBot/1.0"
```

---

## ✅ Paso 7: Verificar que Funciona

Prueba tu configuración con este comando:

```bash
cd src/collectors
python reddit_collector.py
```

Si todo está bien, verás:
```
📡 Recopilando desde Reddit (4 subreddits)...
  ✅ r/technology: 10 posts
  ✅ r/programming: 10 posts
  ✅ r/Python: 5 posts
  ✅ r/artificial: 5 posts
```

---

## 🔧 Solución de Problemas

### ❌ Error: "⚠️ No se encontraron credenciales de Reddit"
- **Causa**: No configuraste el archivo `.env`
- **Solución**: Revisa el Paso 6

### ❌ Error: "401 Unauthorized"
- **Causa**: Credenciales incorrectas
- **Solución**: 
  1. Verifica que copiaste bien el CLIENT_ID y CLIENT_SECRET
  2. Asegúrate de que no hay espacios extras
  3. Verifica que seleccionaste "script" como tipo de app

### ❌ Error: "praw not found" o "No module named 'praw'"
- **Causa**: No instalaste la librería de Reddit
- **Solución**: 
  ```bash
  pip install praw
  ```

### ❌ No se recopilan posts
- **Causa posible 1**: Los posts no cumplen el `min_score` (score mínimo)
- **Solución**: Baja el `min_score` en el código:
  ```python
  posts = collector.collect(time_filter='day', min_score=10)  # Bajado de 50 a 10
  ```
  
- **Causa posible 2**: No hay posts recientes en ese subreddit
- **Solución**: Prueba con otros subreddits más activos

---

## 🎯 Configuración Avanzada

### Cambiar Subreddits

Edita `config/sources.yaml`:

```yaml
reddit_sources:
  - name: "r/MachineLearning"
    subreddit: "MachineLearning"
    limit: 15
    
  - name: "r/javascript"
    subreddit: "javascript"
    limit: 10
```

### Ajustar Filtros

En tu código:

```python
collector = RedditCollector()

# Recopilar posts de la última semana con mínimo 100 upvotes
posts = collector.collect(
    time_filter='week',  # 'hour', 'day', 'week', 'month', 'year'
    min_score=100        # Mínimo de upvotes
)
```

---

## 📚 Recursos Adicionales

- **Reddit API Docs**: https://www.reddit.com/dev/api/
- **PRAW Documentation**: https://praw.readthedocs.io/
- **Crear Reddit App**: https://www.reddit.com/prefs/apps
- **Reddit API Rules**: https://github.com/reddit-archive/reddit/wiki/API

---

## 🔒 Seguridad

⚠️ **NUNCA compartas tus credenciales:**
- ❌ NO las subas a GitHub
- ❌ NO las compartas en screenshots
- ❌ NO las incluyas en el código directamente

✅ **Buenas prácticas:**
- ✅ Usa archivo `.env` (ya está en `.gitignore`)
- ✅ Si alguien accede a tus credenciales, regenera la app
- ✅ Usa un user_agent descriptivo y único

---

## 🎉 ¡Listo!

Ahora tienes acceso a Reddit API y puedes recopilar noticias de los mejores subreddits tech.

**Siguiente paso**: Integra el Reddit Collector en tu flujo principal (`main.py`) para usarlo junto con RSS y News API.

¿Necesitas ayuda? Abre un issue o consulta la documentación de PRAW.


