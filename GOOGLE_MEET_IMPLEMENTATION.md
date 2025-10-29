# 🎥 Integración de Google Meet en Silicon Founder

## 📋 Resumen de Implementación

Este documento describe la integración completa de Google Meet en el sistema de mensajería de Silicon Founder, permitiendo a los usuarios realizar videollamadas instantáneas desde sus conversaciones.

---

## ✅ Lo que ya está implementado

### 1. **Backend Completo**

- ✅ Modelo `Conversation` actualizado con campos de Meet:
  - `meet_enabled`: Habilitar/deshabilitar videollamadas
  - `meet_link`: URL de la videollamada
  - `meet_created_at`: Timestamp de creación
  - `meet_created_by`: Usuario que creó la reunión

- ✅ Servicio `GoogleMeetService` (`core/google_meet_service.py`):
  - `create_instant_meet()`: Genera enlaces únicos de Meet
  - `get_authorization_url()`: OAuth flow (opcional, avanzado)
  - `create_meet_link()`: Integración completa con Calendar API

- ✅ Vistas implementadas (`core/views.py`):
  - `toggle_meet_in_conversation`: ON/OFF videollamadas
  - `create_meet_link`: Crear enlace de Meet  
  - `join_meet`: Redirigir a Google Meet
  - `end_meet`: Finalizar reunión

- ✅ URLs configuradas (`core/urls.py`):
  ```python
  /messages/<id>/meet/toggle/  # Habilitar/deshabilitar
  /messages/<id>/meet/create/  # Crear enlace
  /messages/<id>/meet/join/    # Unirse a reunión
  /messages/<id>/meet/end/     # Finalizar
  ```

- ✅ Dependencias agregadas (`requirements.txt`):
  ```
  google-auth==2.42.0
  google-auth-oauthlib==1.2.1
  google-auth-httplib2==0.2.0
  google-api-python-client==2.185.0
  ```

### 2. **Migración de Base de Datos**

- ✅ Archivo creado: `core/migrations/0002_add_google_meet_to_conversation.py`
- ⏳ **Pendiente**: Ejecutar en producción con `python manage.py migrate`

---

## 🚀 Próximos Pasos (Frontend)

### Opción 1: Implementación Simple (Recomendado para MVP)

Agregar al template `core/templates/core/conversation_detail.html` en la sección del header:

```html
<!-- Después de "Ver perfil", agregar botón de videollamada -->
<div class="flex items-center gap-3">
    <!-- Botón de Google Meet -->
    <div x-data="{ meetEnabled: {{ conversation.meet_enabled|yesno:'true,false' }} }">
        <!-- Toggle para habilitar Meet -->
        <button @click="toggleMeet()" 
                class="px-4 py-2 rounded-xl transition-all text-sm font-medium"
                :class="meetEnabled ? 'bg-green-100 text-green-700 hover:bg-green-200' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'">
            <i class="fas fa-video mr-2"></i>
            <span x-text="meetEnabled ? 'Meet ON' : 'Meet OFF'"></span>
        </button>
        
        <!-- Botón para iniciar/unirse a videollamada -->
        <div x-show="meetEnabled" class="mt-2">
            {% if conversation.meet_link %}
                <a href="{% url 'core:join_meet' conversation.id %}" 
                   target="_blank"
                   class="block px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-center">
                    <i class="fas fa-video mr-2"></i> Unirse a videollamada
                </a>
                <button onclick="endMeet()" 
                        class="mt-2 w-full px-4 py-2 bg-red-100 text-red-700 hover:bg-red-200 rounded-xl text-sm">
                    <i class="fas fa-phone-slash mr-2"></i> Finalizar reunión
                </button>
            {% else %}
                <button onclick="createMeet()" 
                        class="block w-full px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-xl">
                    <i class="fas fa-plus-circle mr-2"></i> Iniciar videollamada
                </button>
            {% endif %}
        </div>
    </div>
    
    <a href="{% url 'core:investor_detail' other_user.investorprofile.id %}" 
       class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl">
        <i class="fas fa-external-link-alt mr-2"></i> Ver perfil
    </a>
</div>
```

### JavaScript para manejar acciones:

```html
<script>
// Toggle Meet ON/OFF
function toggleMeet() {
    fetch(`/messages/{{ conversation.id }}/meet/toggle/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            location.reload(); // Recargar para actualizar UI
        }
    });
}

// Crear enlace de Meet
function createMeet() {
    fetch(`/messages/{{ conversation.id }}/meet/create/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // Abrir en nueva pestaña
            window.open(data.meet_link, '_blank');
            location.reload();
        } else {
            alert(data.error);
        }
    });
}

// Finalizar Meet
function endMeet() {
    if (confirm('¿Seguro que deseas finalizar la videollamada?')) {
        fetch(`/messages/{{ conversation.id }}/meet/end/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json'
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        });
    }
}
</script>
```

### Opción 2: Implementación Avanzada con Modal

Crear un componente modal más elaborado con Alpine.js o Vue.js que muestre:
- Preview del enlace de Meet
- Opciones de configuración (duración, compartir pantalla, etc.)
- Historial de reuniones
- Embed de Google Meet dentro del sitio (requiere iframe)

---

## 🔐 Configuración de Variables de Entorno

Agregar en Render.com → Environment Variables:

```bash
# Google Meet OAuth Credentials
GOOGLE_MEET_CLIENT_ID=766447406081-lcb9li4g7875fl304dr8ai1k1mtdng5i.apps.googleusercontent.com
GOOGLE_MEET_CLIENT_SECRET=[TU_CLIENT_SECRET_AQUI]
GOOGLE_MEET_API_KEY=AIzaSyB2s5SzWLePYEt1o2eKYEvAWPxasqrEOWU
```

⚠️ **IMPORTANTE**: Nunca subir las credenciales al repositorio Git. Siempre usar variables de entorno.

---

## 📊 Cómo Funciona

### Flujo Simple (Implementado):

1. **Usuario A** habilita videollamadas en su conversación con **Usuario B**
2. **Usuario A** presiona "Iniciar videollamada"
3. Backend genera un enlace único de Meet: `https://meet.google.com/abc-defg-hij`
4. Se guarda en `conversation.meet_link`
5. Se crea una notificación para **Usuario B**
6. **Usuario B** recibe notificación y puede unirse con "Unirse a videollamada"
7. Ambos son redirigidos a Google Meet en nueva pestaña
8. Cuando terminan, cualquiera puede presionar "Finalizar reunión"

### Flujo Avanzado (Opcional - OAuth):

1. Usuario autoriza con su cuenta de Google (OAuth 2.0)
2. Se crea evento en Google Calendar con Meet integrado
3. Se envían invitaciones automáticas por email
4. La reunión queda agendada en los calendarios de ambos usuarios

---

## 🎨 Mejoras de UX Sugeridas

### 1. **Indicador Visual de Reunión Activa**

```html
{% if conversation.meet_link %}
<div class="bg-green-100 border border-green-300 rounded-xl p-4 mb-4">
    <div class="flex items-center gap-3">
        <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
        <div class="flex-1">
            <p class="font-bold text-green-900">Videollamada activa</p>
            <p class="text-sm text-green-700">
                Iniciada por {{ conversation.meet_created_by.get_full_name }}
                hace {{ conversation.meet_created_at|timesince }}
            </p>
        </div>
        <a href="{% url 'core:join_meet' conversation.id %}" 
           target="_blank"
           class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg">
            Unirse ahora
        </a>
    </div>
</div>
{% endif %}
```

### 2. **Notificación en Tiempo Real (WebSocket)**

Modificar `core/consumers.py` para enviar eventos de Meet:

```python
# Cuando se crea una reunión
await self.channel_layer.group_send(
    self.conversation_group_name,
    {
        'type': 'meet_started',
        'meet_link': conversation.meet_link,
        'started_by': user.get_full_name()
    }
)
```

### 3. **Badge en la Lista de Conversaciones**

En `messages_inbox.html`, mostrar icono de Meet activo:

```html
{% if conv_data.conversation.meet_link %}
<span class="bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs">
    <i class="fas fa-video mr-1"></i> En llamada
</span>
{% endif %}
```

---

## 🔧 Solución de Problemas

### Error: "No module named 'google'"

```bash
# En Render, las dependencias se instalan automáticamente
# Si desarrollas local, instala:
pip install google-auth google-auth-oauthlib google-api-python-client
```

### Error: "Meet link not working"

- Verifica que las credenciales OAuth estén configuradas en Render
- Revisa que el dominio esté autorizado en Google Cloud Console
- Los enlaces de Meet son válidos pero pueden requerir cuenta de Google

### Mejora: Persistir enlaces de Meet

Los enlaces generados con `create_instant_meet()` son estáticos. Para crear reuniones reales de Google Calendar con Meet integrado, usa el método `create_meet_link()` con OAuth completo.

---

## 📚 Documentación de Referencia

- [Google Meet API](https://developers.google.com/workspace/meet/api/guides/overview?hl=es_419)
- [Google Calendar API](https://developers.google.com/calendar/api/guides/overview)
- [OAuth 2.0 for Web Apps](https://developers.google.com/identity/protocols/oauth2/web-server)

---

## ✨ Características Futuras

- [ ] Grabar reuniones y guardar en el sistema
- [ ] Transcripción automática con Speech-to-Text API
- [ ] Calendario de reuniones agendadas
- [ ] Integración con Google Drive para compartir archivos
- [ ] Estadísticas de tiempo en llamada
- [ ] Recordatorios automáticos 10 minutos antes

---

## 🚀 Deploy a Producción

```bash
# 1. Commit de cambios
git add -A
git commit -m "feat: Integración de Google Meet en mensajería"

# 2. Push a GitHub (trigger auto-deploy en Render)
git push origin main

# 3. En Render, esperar deploy y ejecutar migraciones
# Render lo hace automáticamente con build.sh
```

### Verificar en Producción:

1. Ir a https://california-jhkj.onrender.com/messages/
2. Abrir una conversación
3. Buscar el botón "Meet ON/OFF"
4. Habilitar y crear videollamada
5. El enlace debería abrir Google Meet en nueva pestaña

---

**¿Listo para implementar? Puedes elegir la Opción 1 (Simple) para MVP o la Opción 2 (Avanzada) para experiencia premium.**
