# 🎓 Tutorial: Primeros Pasos con Python

Este archivo te guiará paso a paso para configurar y usar tu proyecto.

## 📚 Conceptos Básicos de Python

### 1. ¿Qué es un Entorno Virtual?

Un entorno virtual es como una "caja" aislada donde instalas las librerías de Python solo para este proyecto. Así no contaminas tu sistema.

### 2. ¿Qué es pip?

`pip` es el instalador de paquetes de Python. Es como una "tienda" donde descargas librerías.

### 3. ¿Qué son los módulos?

Los módulos son archivos `.py` que contienen código reutilizable. Puedes importarlos en otros archivos.

---

## 🚀 Paso 1: Verificar Python

Primero, verifica que tienes Python instalado:

```bash
python3 --version
```

Deberías ver algo como: `Python 3.8.x` o superior.

Si no tienes Python, descárgalo de [python.org](https://www.python.org/downloads/)

---

## 🔧 Paso 2: Crear Entorno Virtual

En la terminal, dentro de tu carpeta del proyecto, ejecuta:

```bash
python3 -m venv venv
```

Esto crea una carpeta `venv/` con tu entorno virtual.

---

## ✅ Paso 3: Activar el Entorno Virtual

### En Mac/Linux:
```bash
source venv/bin/activate
```

### En Windows:
```bash
venv\Scripts\activate
```

Cuando esté activado, verás `(venv)` al inicio de tu línea de comando.

---

## 📦 Paso 4: Instalar Dependencias

Con el entorno activado, instala las librerías necesarias:

```bash
pip install -r requirements.txt
```

Esto instalará:
- `feedparser` - Para leer RSS feeds
- `requests` - Para hacer peticiones HTTP
- `pyyaml` - Para leer archivos de configuración
- Y otras más...

---

## 🎯 Paso 5: Probar el Recolector RSS

¡Ya puedes probar tu primer código! Ejecuta:

```bash
python src/collectors/rss_collector.py
```

Esto:
1. Lee los RSS feeds de TechCrunch, Hacker News, etc.
2. Recopila las noticias más recientes
3. Las guarda en `data/news.json`

---

## 🤖 Paso 6: Generar Tweets

Ahora genera tweets desde las noticias:

```bash
python src/generators/tweet_generator.py
```

Esto:
1. Lee las noticias de `data/news.json`
2. Genera tweets usando templates
3. Los guarda en `data/tweets.json`

---

## 📝 Paso 7: Ver los Tweets Generados

Abre el archivo `data/tweets.json` para ver los tweets generados.

O usa el comando:

```bash
python src/main.py list
```

---

## 🔄 Flujo Completo

Para ejecutar todo el proceso completo:

```bash
python src/main.py all
```

Esto ejecutará:
1. Recolección de noticias
2. Generación de tweets
3. Listado de tweets

---

## 🎨 Personalización

### Agregar más fuentes RSS

Edita `config/sources.yaml` y agrega más feeds:

```yaml
rss_feeds:
  - name: "Tu Fuente"
    url: "https://ejemplo.com/feed/"
    category: "tech"
```

### Cambiar los templates de tweets

Edita `src/generators/tweet_generator.py` y modifica la lista `TEMPLATES`:

```python
TEMPLATES = [
    "🚀 Tu template aqui: {title}\n\n{link}",
    # ... más templates
]
```

---

## 🐛 Solución de Problemas

### Error: "No module named 'feedparser'"

Solución: Activaste el entorno virtual? Ejecuta:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "File not found: config/sources.yaml"

Solución: Asegúrate de ejecutar los comandos desde la carpeta raíz del proyecto.

### Los feeds no traen noticias

Solución: Algunas fuentes RSS pueden estar caídas. Prueba con otras o aumenta el `max_age_hours`.

---

## 📖 Próximos Pasos

1. ✅ **Agrega News API** - Para más variedad de noticias
2. ✅ **Integra Reddit** - Para contenido trending
3. ✅ **Usa OpenAI** - Para generar tweets más creativos
4. ✅ **Crea un dashboard** - Para revisar tweets antes de publicar
5. ✅ **Automatiza** - Usa cron jobs para ejecutar automáticamente

---

## 💡 Tips de Python para Principiantes

### Leer el código
- Empieza por `src/main.py` - Es el más simple
- Luego ve a `rss_collector.py` - Ahí está la magia
- Finalmente `tweet_generator.py` - Para entender los templates

### Experimenta
- Cambia los templates
- Agrega emojis
- Modifica los filtros
- ¡Rompe cosas y aprende!

### Depuración
- Usa `print()` para ver qué pasa
- Lee los errores - siempre dicen qué está mal
- Google es tu amigo

---

## 🤝 ¿Necesitas Ayuda?

- Lee los comentarios en el código (líneas con `#`)
- Cada función tiene una explicación de qué hace
- Experimenta y no tengas miedo de romper cosas

**¡Feliz aprendizaje! 🎉**

