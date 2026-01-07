# 🚀 Configuración de WebSockets en Render.com

## ❌ Problema Actual
```
WebSocket connection to 'wss://california-jhkj.onrender.com/ws/chat/1/' failed
```

El sistema de mensajería no funciona porque:
1. **Django Channels requiere Redis** en producción con múltiples workers
2. **Gunicorn NO soporta WebSockets** - se necesita Daphne (servidor ASGI)

---

## ✅ Solución Completa

### **IMPORTANTE: Configurar Start Command PRIMERO**

Antes de cualquier cosa, ve a **Settings** → **Build & Deploy** → **Start Command** y cámbialo a:

```bash
python -m daphne -b 0.0.0.0 -p $PORT mydevsite.asgi:application
```

⚠️ **NO uses** `gunicorn` - no soporta WebSockets
⚠️ **NO uses** `daphne` directamente - puede dar error 127
✅ **USA** `python -m daphne` - funciona siempre

---

## Paso 1: Agregar Redis a Render

### **Paso 1: Crear Redis Instance en Render**

1. Ve a tu Dashboard de Render: https://dashboard.render.com/
2. Click en **"New +"** → **"Redis"**
3. Configuración:
   - **Name**: `california-redis`
   - **Region**: Mismo que tu Web Service (ej: Oregon)
   - **Plan**: **Free** (suficiente para desarrollo)
   - **Max Memory Policy**: `noeviction` (recomendado)
4. Click **"Create Redis"**

⏱️ *Espera 2-3 minutos mientras se crea la instancia*

---

### **Paso 2: Copiar la URL de Redis**

1. Entra a tu Redis instance recién creada
2. En la pestaña **"Info"**, busca:
   - **Internal Redis URL** (si tu web service está en la misma región)
   - **External Redis URL** (si está en diferente región)
3. Copia la URL completa, se ve así:
   ```
   redis://red-xxxxx:6379
   ```

---

### **Paso 3: Agregar Variable de Entorno en Web Service**

1. Ve a tu **Web Service** (`california-jhkj`)
2. Ve a **Environment** en el menú lateral
3. Click **"Add Environment Variable"**
4. Agrega:
   ```
   Key:   REDIS_URL
   Value: redis://red-xxxxx:6379  (pega la URL que copiaste)
   ```
5. Click **"Save Changes"**

🔄 *Esto reiniciará automáticamente tu servicio*

---

### **Paso 4: Verificar el Deploy**

1. Espera 3-5 minutos a que termine el deploy
2. Ve a los **Logs** de tu Web Service
3. Busca mensajes como:
   ```
   ✅ Daphne running
   ✅ WebSocket connection successful
   ```

---

### **Paso 5: Probar WebSockets**

1. Abre tu sitio: `https://california-jhkj.onrender.com`
2. Ve a **Mensajes** → Abre una conversación
3. Abre la **Consola del navegador** (F12 → Console)
4. Deberías ver:
   ```
   ✅ WebSocket conectado
   ✅ Sistema de notificaciones internas activo
   ```
5. Envía un mensaje de prueba

---

## 🔧 Troubleshooting

### ❌ Problema: "Redis connection refused"
**Solución:** Verifica que:
- La URL de Redis esté correcta en variables de entorno
- Redis instance esté en estado "Available"
- Ambos servicios estén en la **misma región** (para usar Internal URL)

### ❌ Problema: "WebSocket still failing"
**Solución:** 
1. Verifica logs: `https://dashboard.render.com/web/california-jhkj/logs`
2. Busca errores relacionados con `channels` o `daphne`
3. Asegúrate de que `requirements.txt` tiene:
   ```
   channels==4.3.1
   channels-redis==4.3.0
   daphne==4.2.1
   redis==6.1.0
   ```

### ❌ Problema: "Build succeed but WebSocket fails"
**Solución:** Verifica que el **Start Command** sea correcto:
```bash
daphne -b 0.0.0.0 -p $PORT mydevsite.asgi:application
```

---

## 📊 Configuración Actual del Proyecto

✅ **Ya configurado:**
- `mydevsite/settings.py` → Detecta automáticamente `REDIS_URL`
- `requirements.txt` → Incluye todas las dependencias necesarias
- `mydevsite/asgi.py` → Configurado para WebSockets
- `core/routing.py` → Rutas WebSocket definidas
- `core/consumers.py` → ChatConsumer implementado

⏳ **Falta configurar:**
- ❌ Redis instance en Render
- ❌ Variable de entorno `REDIS_URL`

---

## 🎯 Resumen de Comandos

### Verificar Redis localmente (opcional):
```bash
redis-cli ping
# Respuesta: PONG
```

### Logs en Render:
```bash
# Dashboard → Web Service → Logs
# Busca: "Daphne", "WebSocket", "Redis"
```

### Variables de entorno necesarias:
```env
REDIS_URL=redis://red-xxxxx:6379
SECRET_KEY=tu-secret-key
DEBUG=False
ALLOWED_HOSTS=california-jhkj.onrender.com
```

---

## 📚 Recursos

- [Render Redis Docs](https://render.com/docs/redis)
- [Django Channels Docs](https://channels.readthedocs.io/)
- [Channels Redis Backend](https://github.com/django/channels_redis)

---

## ✅ Checklist Final

- [ ] Redis instance creada en Render
- [ ] Variable `REDIS_URL` agregada al Web Service
- [ ] Deploy completado sin errores
- [ ] WebSocket se conecta correctamente
- [ ] Mensajes se envían y reciben en tiempo real
- [ ] Notificaciones internas funcionan

¡Listo! Después de estos pasos, tu sistema de mensajería debería funcionar perfectamente en producción. 🎉
