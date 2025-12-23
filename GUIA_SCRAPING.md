# 🕷️ Guía Completa: Web Scraping para Noticias Tech

Esta guía te muestra cómo scrapear diferentes fuentes de noticias tecnológicas sin necesidad de APIs.

---

## 🎯 Fuentes que Puedes Scrapear

### ⭐ Nivel 1: FÁCIL (Ideal para empezar)

#### 1. **Blogs Oficiales de Empresas Tech**

Estas empresas publican en sus blogs oficiales que son fáciles de scrapear:

| Empresa | Blog URL | Frecuencia | Calidad |
|---------|----------|------------|---------|
| **Google AI** | `https://blog.google/technology/ai/` | Semanal | ⭐⭐⭐⭐⭐ |
| **Microsoft** | `https://blogs.microsoft.com/` | Diaria | ⭐⭐⭐⭐⭐ |
| **Meta AI** | `https://ai.meta.com/blog/` | Semanal | ⭐⭐⭐⭐⭐ |
| **OpenAI** | `https://openai.com/news/` | Semanal | ⭐⭐⭐⭐⭐ |
| **DeepMind** | `https://deepmind.google/discover/blog/` | Mensual | ⭐⭐⭐⭐⭐ |
| **Anthropic** | `https://www.anthropic.com/news` | Mensual | ⭐⭐⭐⭐⭐ |
| **Tesla** | `https://www.tesla.com/blog` | Mensual | ⭐⭐⭐⭐ |
| **SpaceX** | `https://www.spacex.com/updates/` | Mensual | ⭐⭐⭐⭐ |
| **GitHub** | `https://github.blog/` | Diaria | ⭐⭐⭐⭐⭐ |
| **Stripe** | `https://stripe.com/blog` | Semanal | ⭐⭐⭐⭐ |
| **Shopify** | `https://www.shopify.com/blog` | Diaria | ⭐⭐⭐⭐ |
| **Notion** | `https://www.notion.so/blog` | Semanal | ⭐⭐⭐⭐ |
| **Linear** | `https://linear.app/blog` | Mensual | ⭐⭐⭐⭐ |
| **Vercel** | `https://vercel.com/blog` | Semanal | ⭐⭐⭐⭐⭐ |
| **Netflix Tech** | `https://netflixtechblog.com/` | Mensual | ⭐⭐⭐⭐⭐ |
| **Uber Engineering** | `https://www.uber.com/blog/engineering/` | Semanal | ⭐⭐⭐⭐⭐ |
| **Airbnb Tech** | `https://medium.com/airbnb-engineering` | Mensual | ⭐⭐⭐⭐⭐ |
| **Spotify Engineering** | `https://engineering.atspotify.com/` | Mensual | ⭐⭐⭐⭐ |
| **AWS News** | `https://aws.amazon.com/blogs/aws/` | Diaria | ⭐⭐⭐⭐⭐ |
| **Azure Updates** | `https://azure.microsoft.com/en-us/updates/` | Diaria | ⭐⭐⭐⭐⭐ |

#### 2. **Hacker News** (Súper fácil de scrapear)

```
https://news.ycombinator.com/
```

- ✅ HTML simple
- ✅ No requiere JavaScript
- ✅ API pública: https://github.com/HackerNews/API
- ✅ Sin restricciones

#### 3. **Product Hunt**

```
https://www.producthunt.com/
```

- ✅ Estructura HTML clara
- ✅ Productos tech diarios
- ✅ API disponible: https://api.producthunt.com/v2/docs

#### 4. **Indie Hackers**

```
https://www.indiehackers.com/
```

- ✅ Fácil de parsear
- ✅ Historias de startups
- ✅ HTML limpio

---

### ⭐⭐ Nivel 2: INTERMEDIO (Requiere algo de experiencia)

#### 5. **Twitter/X** (Complicado pero posible)

**Opciones:**

**A) Nitter (Frontend alternativo - FÁCIL)**
```
https://nitter.net/username
```
- ✅ Scraping fácil
- ✅ No requiere API
- ✅ Sin bloqueos
- ✅ Múltiples instancias disponibles

**Cuentas Tech para seguir:**
- `@elonmusk` - Tesla/SpaceX
- `@sama` - OpenAI
- `@satyanadella` - Microsoft
- `@sundarpichai` - Google
- `@getify` - JavaScript
- `@dan_abramov` - React
- `@paulg` - Y Combinator
- `@naval` - AngelList
- `@pmarca` - a16z
- `@balajis` - Crypto/Tech
- `@benedictevans` - Tech analyst
- `@cdixon` - a16z crypto
- `@dhh` - Ruby on Rails
- `@spolsky` - Stack Overflow

**B) Twitter API v2 (Requiere aprobación)**
- ⚠️ Complicado de conseguir acceso
- ⚠️ Plan gratis muy limitado
- ⚠️ No recomendado

#### 6. **Reddit** (Sin API oficial)

**Opciones:**

**A) Old Reddit (Fácil de scrapear)**
```
https://old.reddit.com/r/subreddit/.json
```
- ✅ JSON público
- ✅ No requiere autenticación
- ✅ Límites razonables

**Subreddits Tech relevantes:**
- `r/technology` - Tech general
- `r/programming` - Programación
- `r/Python` - Python específico
- `r/javascript` - JavaScript
- `r/webdev` - Web development
- `r/MachineLearning` - ML/AI
- `r/artificial` - AI news
- `r/datascience` - Data Science
- `r/devops` - DevOps
- `r/kubernetes` - Kubernetes
- `r/docker` - Docker
- `r/golang` - Go
- `r/rust` - Rust
- `r/reactjs` - React
- `r/nextjs` - Next.js
- `r/tailwindcss` - Tailwind
- `r/opensource` - Open Source
- `r/github` - GitHub
- `r/selfhosted` - Self-hosting
- `r/homelab` - Homelabs
- `r/sysadmin` - Sysadmin
- `r/netsec` - Security
- `r/hacking` - Ethical hacking
- `r/cryptography` - Crypto
- `r/blockchain` - Blockchain
- `r/cryptocurrency` - Crypto general
- `r/ethereum` - Ethereum
- `r/Bitcoin` - Bitcoin
- `r/startups` - Startups
- `r/entrepreneur` - Emprendimiento
- `r/SaaS` - SaaS products
- `r/indiehackers` - Indie devs
- `r/gamedev` - Game development
- `r/Unity3D` - Unity
- `r/unrealengine` - Unreal Engine

**B) Libreddit/Redlib (Frontend alternativo)**
```
https://libreddit.domain.glass/
```
- ✅ Fácil de scrapear
- ✅ Sin JavaScript

#### 7. **Medium** (Publicaciones tech)

```
https://medium.com/tag/technology/latest
```

**Publicaciones relevantes:**
- `Better Programming`
- `The Startup`
- `JavaScript in Plain English`
- `Python in Plain English`
- `Level Up Coding`
- `Towards Data Science`
- `Analytics Vidhya`
- `UX Collective`

#### 8. **Dev.to**

```
https://dev.to/api/articles
```
- ✅ API pública y gratuita
- ✅ Sin autenticación necesaria
- ✅ Documentación: https://developers.forem.com/api

---

### ⭐⭐⭐ Nivel 3: AVANZADO (Requiere herramientas especiales)

#### 9. **LinkedIn** (Complicado)

- ⚠️ Requiere login
- ⚠️ Anti-scraping agresivo
- ⚠️ Puede banear IPs
- 💡 Alternativa: Buscar RSS feeds de blogs personales

#### 10. **Discord/Slack** (Comunidades tech)

- Requiere bots/webhooks
- Comunidades de empresas tech
- Anuncios de productos

---

## 🛠️ Herramientas de Scraping

### Python Libraries (ya tienes instalado)

```python
# HTML parsing
BeautifulSoup4   # Ya instalado
lxml             # Ya instalado

# HTTP requests
requests         # Ya instalado

# JavaScript rendering (si se necesita)
playwright       # Para sitios con JS
selenium         # Alternativa a Playwright

# APIs alternativas
tweepy           # Twitter (si consigues API)
praw             # Reddit (si consigues API)
```

---

## 📝 Ejemplos de Código

### 1. Scraper para Blog de Empresa (Google AI)

```python
import requests
from bs4 import BeautifulSoup

def scrape_google_ai_blog():
    url = "https://blog.google/technology/ai/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    articles = []
    # Encontrar los artículos (inspecciona el HTML primero)
    for article in soup.find_all('article', class_='post'):
        title = article.find('h2').text.strip()
        link = article.find('a')['href']
        summary = article.find('p').text.strip()
        
        articles.append({
            'title': title,
            'link': link,
            'summary': summary,
            'source': 'Google AI Blog'
        })
    
    return articles
```

### 2. Scraper para Hacker News

```python
import requests

def scrape_hacker_news():
    # Usar la API oficial
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(url)
    story_ids = response.json()[:30]  # Top 30
    
    articles = []
    for story_id in story_ids:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story = requests.get(story_url).json()
        
        if story.get('type') == 'story':
            articles.append({
                'title': story.get('title'),
                'link': story.get('url'),
                'score': story.get('score'),
                'source': 'Hacker News'
            })
    
    return articles
```

### 3. Scraper para Reddit (sin API)

```python
import requests

def scrape_reddit_subreddit(subreddit='technology'):
    url = f"https://old.reddit.com/r/{subreddit}/.json"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    posts = []
    for post in data['data']['children']:
        post_data = post['data']
        posts.append({
            'title': post_data['title'],
            'link': post_data['url'],
            'score': post_data['score'],
            'comments': post_data['num_comments'],
            'source': f'Reddit - r/{subreddit}'
        })
    
    return posts
```

### 4. Scraper para Nitter (Twitter alternativo)

```python
import requests
from bs4 import BeautifulSoup

def scrape_nitter_user(username='elonmusk'):
    url = f"https://nitter.net/{username}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    tweets = []
    for tweet in soup.find_all('div', class_='timeline-item')[:10]:
        content = tweet.find('div', class_='tweet-content')
        if content:
            tweets.append({
                'text': content.text.strip(),
                'source': f'Twitter - @{username}',
                'author': username
            })
    
    return tweets
```

### 5. Scraper para Dev.to (con API)

```python
import requests

def scrape_dev_to(tag='python', per_page=20):
    url = f"https://dev.to/api/articles"
    params = {
        'tag': tag,
        'per_page': per_page
    }
    
    response = requests.get(url, params=params)
    articles = response.json()
    
    posts = []
    for article in articles:
        posts.append({
            'title': article['title'],
            'link': article['url'],
            'summary': article['description'],
            'tags': article['tag_list'],
            'source': 'Dev.to'
        })
    
    return posts
```

---

## 🎯 Empresas Tech para Seguir

### FAANG + Big Tech

- **Google**: Blog AI, Cloud, Developer, Chrome
- **Meta/Facebook**: AI Blog, Engineering Blog
- **Amazon/AWS**: AWS News, Amazon Science
- **Netflix**: Tech Blog
- **Apple**: Newsroom (limitado)
- **Microsoft**: Azure, Developer Blogs
- **Nvidia**: AI Blog
- **Intel**: Newsroom

### Startups & Scale-ups

- **OpenAI**: News, Research
- **Anthropic**: News, Research
- **Stripe**: Blog, Developer Updates
- **Vercel**: Blog, Changelog
- **Supabase**: Blog
- **Railway**: Blog
- **Fly.io**: Blog
- **Render**: Blog
- **PlanetScale**: Blog
- **Neon**: Blog

### Developer Tools

- **GitHub**: Blog, Changelog
- **GitLab**: Blog
- **Docker**: Blog
- **Kubernetes**: Blog
- **Terraform**: Blog
- **Cloudflare**: Blog
- **Datadog**: Blog
- **Sentry**: Blog

### Languages & Frameworks

- **Python**: Blog oficial
- **JavaScript**: News
- **Rust**: Blog
- **Go**: Blog
- **React**: Blog
- **Vue**: Blog
- **Svelte**: Blog
- **Next.js**: Blog

---

## ⚠️ Consideraciones Éticas y Legales

### ✅ BUENAS PRÁCTICAS

1. **Respetar robots.txt**
   ```python
   # Verificar antes de scrapear
   https://website.com/robots.txt
   ```

2. **Rate limiting**
   ```python
   import time
   time.sleep(1)  # 1 segundo entre requests
   ```

3. **User-Agent honesto**
   ```python
   headers = {
       'User-Agent': 'TechNewsBot/1.0 (contact@email.com)'
   }
   ```

4. **Cachear resultados**
   - No hacer requests innecesarios
   - Guardar datos localmente

### ❌ EVITAR

- ❌ Scrapear datos privados
- ❌ Hacer requests excesivos (DDoS)
- ❌ Ignorar Terms of Service
- ❌ Revender datos sin permiso

---

## 🚀 Recomendaciones Finales

### Empezar con:

1. **RSS Feeds** (33 ya configuradas) ← Ya tienes esto
2. **Hacker News API** (súper fácil)
3. **Dev.to API** (gratis, sin límites)
4. **Reddit JSON** (sin autenticación)
5. **Blogs de empresas** (Google, Microsoft, OpenAI)

### Después agregar:

6. **Nitter** para Twitter
7. **APIs pagadas** (Guardian, NewsData)
8. **Scraping avanzado** con Playwright

---

## 📚 Próximos Pasos

1. ¿Quieres que cree scrapers para blogs de empresas específicas?
2. ¿Implemento scraper de Hacker News?
3. ¿Creo scraper de Reddit sin API?
4. ¿Implemento Nitter para seguir cuentas de Twitter?
5. ¿Dev.to API integration?

**¿Cuál te interesa más?** 🎯
