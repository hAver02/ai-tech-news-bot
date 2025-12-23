# 🔑 Guía: Cómo Obtener y Configurar tu OpenAI API Key

Esta guía te enseña paso a paso cómo obtener tu API key de OpenAI y configurarla en el proyecto.

---

## 📋 Pasos para Obtener tu API Key

### **1. Crear Cuenta en OpenAI**

1. Ve a: https://platform.openai.com/signup
2. Registrate con email o Google
3. Verifica tu email

### **2. Agregar Método de Pago**

OpenAI requiere una tarjeta de crédito para usar la API:

1. Ve a: https://platform.openai.com/account/billing/overview
2. Click en "Add payment method"
3. Agrega tu tarjeta de crédito
4. (Opcional) Configura límites de gasto mensuales para evitar sorpresas

**Costo estimado:** ~$1-3 por mes para tu uso (2 ejecuciones/día)

### **3. Crear API Key**

1. Ve a: https://platform.openai.com/api-keys
2. Click en "Create new secret key"
3. Dale un nombre: "TechNews Bot" (o el que quieras)
4. **¡IMPORTANTE!** Copia la key inmediatamente (empieza con `sk-...`)
5. No la compartas con nadie

**La key se ve así:**
```
sk-proj-aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890...
```

---

## ⚙️ Configurar en tu Proyecto

### **Método 1: Usando el archivo .env (RECOMENDADO)**

1. **Crear archivo `.env`** en la raíz del proyecto:

```bash
cd /Users/lucianopaz/Desktop/hAver/python-twitter
cp env.example .env
```

2. **Editar el archivo `.env`** y pegar tu API key:

```bash
# Abre con cualquier editor
nano .env
# o
code .env
```

3. **Pegar tu API key:**

```env
# OpenAI API (REQUERIDO)
OPENAI_API_KEY=sk-proj-TU_KEY_AQUI_COMPLETA

# Modelo a usar
OPENAI_MODEL=gpt-3.5-turbo
```

4. **Guardar y cerrar**

✅ **¡Listo!** El proyecto cargará automáticamente la key desde `.env`

---

### **Método 2: Variable de Entorno (Temporal)**

Si solo quieres probar rápido:

```bash
export OPENAI_API_KEY="sk-proj-TU_KEY_AQUI"
python src/llm/openai_provider.py
```

⚠️ **Nota:** Esto solo funciona en la sesión actual de terminal.

---

## 🔒 Seguridad: ¡MUY IMPORTANTE!

### ❌ **NUNCA hagas esto:**

```python
# ❌ MAL - Key hardcodeada en el código
api_key = "sk-proj-abc123..."
```

```bash
# ❌ MAL - Subir .env a GitHub
git add .env
git commit -m "Added config"
```

### ✅ **SÍ haz esto:**

```python
# ✅ BIEN - Cargar desde variable de entorno
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

```bash
# ✅ BIEN - .env está en .gitignore
cat .gitignore | grep ".env"
```

---

## 🧪 Probar que Funciona

### **Test 1: Verificar que se carga la key**

```bash
cd /Users/lucianopaz/Desktop/hAver/python-twitter
source venv/bin/activate
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✅ API Key cargada' if os.getenv('OPENAI_API_KEY') else '❌ No se encontró API Key')"
```

### **Test 2: Probar el provider**

```bash
python src/llm/openai_provider.py
```

Deberías ver:
```
🧠 Calificando noticia con GPT...
   Score: 95/100
   Razón: ...

📝 Generando 3 versiones de tweets...
...
```

### **Test 3: Generar tweets con IA**

```bash
python src/generators/ai_tweet_generator.py
```

---

## 💰 Monitorear Costos

### **1. Ver uso en tiempo real:**
https://platform.openai.com/usage

### **2. Configurar límites de gasto:**
https://platform.openai.com/account/limits

### **3. Estimación de costos para tu proyecto:**

| Modelo | Costo por ejecución | Costo mensual (2x/día) |
|--------|---------------------|------------------------|
| **gpt-3.5-turbo** | ~$0.02 | ~$1.20 | ⭐ Recomendado
| **gpt-4o-mini** | ~$0.30 | ~$9.00 | Más inteligente
| **gpt-4o** | ~$2.00 | ~$60.00 | Premium

**Recomendación:** Empieza con `gpt-3.5-turbo` (barato y bueno)

---

## 🔧 Cambiar de Modelo

Si quieres usar un modelo diferente, edita `.env`:

```env
# Opciones:
OPENAI_MODEL=gpt-3.5-turbo      # Barato (~$0.02/ejecución)
# OPENAI_MODEL=gpt-4o-mini      # Balance calidad/precio
# OPENAI_MODEL=gpt-4o           # Mejor calidad pero caro
# OPENAI_MODEL=gpt-4-turbo      # Anterior generación
```

---

## ❓ Solución de Problemas

### **Error: "No se encontró OPENAI_API_KEY"**

**Solución:**
1. Verifica que existe el archivo `.env` en la raíz del proyecto
2. Verifica que la key está bien escrita (empieza con `sk-`)
3. No hay espacios extras: `OPENAI_API_KEY=sk-...` (sin espacios alrededor del `=`)

### **Error: "Invalid API Key"**

**Solución:**
1. La key es incorrecta o expiró
2. Crea una nueva key en: https://platform.openai.com/api-keys
3. Reemplázala en `.env`

### **Error: "You exceeded your current quota"**

**Solución:**
1. Agregaste método de pago en OpenAI?
2. O llegaste a tu límite de gasto mensual
3. Ve a: https://platform.openai.com/account/billing/overview

### **Error: Rate limit exceeded**

**Solución:**
Estás haciendo demasiadas requests. Espera 1 minuto y vuelve a intentar.

---

## 🎓 Tips Pro

1. **Usar variables de entorno diferentes por ambiente:**
   ```env
   # .env.development
   OPENAI_MODEL=gpt-3.5-turbo
   
   # .env.production
   OPENAI_MODEL=gpt-4o-mini
   ```

2. **Rotar API keys periódicamente** (cada 3-6 meses por seguridad)

3. **Configurar alertas de gasto** en OpenAI dashboard

4. **Revisar usage logs** para optimizar prompts y reducir costos

---

## 📞 Soporte

**OpenAI Help Center:** https://help.openai.com/
**Pricing:** https://openai.com/pricing
**Status:** https://status.openai.com/

---

**¿Listo?** Continúa con el `README.md` para ejecutar el proyecto completo 🚀

