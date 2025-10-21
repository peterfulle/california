"""
Servicio de IA para el chatbot usando Google Gemini
"""
import os
import google.generativeai as genai
from django.conf import settings
from .models import UserProfile, Startup, InvestorProfile

# Configurar la API de Gemini
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

# Listar modelos disponibles (para debugging)
try:
    available_models = []
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            available_models.append(model.name)
    print(f"Modelos disponibles: {available_models}")
except Exception as e:
    print(f"Error al listar modelos: {e}")

def get_user_context(user):
    """Obtiene el contexto del usuario para personalizar las respuestas"""
    try:
        profile = user.profile
        context = {
            'user_type': profile.user_type,
            'name': user.get_full_name() or user.username,
        }
        
        # Si es founder, obtener info de su startup
        if profile.user_type == 'founder':
            try:
                startup = Startup.objects.filter(founder=user).first()
                if startup:
                    context['startup'] = {
                        'name': startup.company_name,
                        'stage': startup.stage,
                        'industry': startup.industry.name if startup.industry else None,
                        'seeking_amount': startup.seeking_amount,
                        'is_fundraising': startup.is_fundraising,
                    }
            except:
                pass
        
        # Si es investor, obtener su perfil
        elif profile.user_type == 'investor':
            try:
                investor = InvestorProfile.objects.filter(user=user).first()
                if investor:
                    context['investor'] = {
                        'firm_name': investor.firm_name,
                        'investment_range_min': investor.investment_range_min,
                        'investment_range_max': investor.investment_range_max,
                        'investment_stage': investor.investment_stage,
                    }
            except:
                pass
        
        return context
    except:
        return {'user_type': 'community', 'name': user.username}


def get_system_prompt(user_context):
    """Genera el prompt del sistema basado en el tipo de usuario"""
    
    user_type = user_context.get('user_type', 'community')
    name = user_context.get('name', 'Usuario')
    
    base_prompt = f"""Eres un asistente de IA especializado en el ecosistema de startups, inversiones y emprendimiento. 
Tu nombre es "Startup Advisor AI" y estás aquí para ayudar a {name}.

Usuario actual: {name}
Tipo de usuario: {user_type}

"""
    
    if user_type == 'founder':
        startup_info = user_context.get('startup', {})
        if startup_info:
            base_prompt += f"""
Este usuario es fundador de una startup:
- Nombre: {startup_info.get('name', 'N/A')}
- Etapa: {startup_info.get('stage', 'N/A')}
- Industria: {startup_info.get('industry', 'N/A')}
- Buscando: ${startup_info.get('seeking_amount', 0):,} USD
- En fundraising: {'Sí' if startup_info.get('is_fundraising') else 'No'}

Enfócate en ayudar con:
- Estrategias de fundraising y pitch
- Desarrollo de producto y mercado
- Modelo de negocio y métricas clave
- Aspectos legales para startups
- Networking con inversores
- Growth hacking y marketing
"""
        else:
            base_prompt += """
Este usuario es un founder. Ayúdalo con:
- Validación de ideas de negocio
- Creación de pitch deck
- Búsqueda de inversores
- Aspectos legales y constitución de empresas
- Estrategias de go-to-market
- Construcción de equipo
"""
    
    elif user_type == 'investor':
        investor_info = user_context.get('investor', {})
        if investor_info:
            base_prompt += f"""
Este usuario es un inversor:
- Firma: {investor_info.get('firm_name', 'N/A')}
- Rango de inversión: ${investor_info.get('investment_range_min', 0):,} - ${investor_info.get('investment_range_max', 0):,} USD
- Etapa preferida: {investor_info.get('investment_stage', 'N/A')}

Enfócate en ayudar con:
- Análisis de startups y due diligence
- Valoración de empresas
- Estructuración de deals
- Construcción de portafolio
- Tendencias del mercado
- Deal flow y sourcing
"""
        else:
            base_prompt += """
Este usuario es un inversor. Ayúdalo con:
- Evaluación de startups
- Due diligence y métricas clave
- Estrategias de inversión
- Construcción de portafolio
- Networking con founders
- Términos de inversión (SAFE, equity, convertible notes)
"""
    
    elif user_type == 'advisor':
        base_prompt += """
Este usuario es un advisor/mentor. Ayúdalo con:
- Mejores prácticas de mentoría
- Estrategias de asesoramiento
- Tendencias del ecosistema
- Conexiones efectivas entre startups e inversores
- Desarrollo de programas de aceleración
"""
    
    else:
        base_prompt += """
Este usuario es parte de la comunidad. Ayúdalo con:
- Información general sobre startups e inversión
- Cómo empezar en el ecosistema
- Oportunidades de networking
- Eventos y recursos educativos
"""
    
    base_prompt += """

IMPORTANTE:
- Siempre responde en español de forma clara y profesional
- Sé conciso pero informativo
- Usa ejemplos prácticos cuando sea relevante
- Si no sabes algo, admítelo y sugiere recursos
- Enfócate en dar consejos accionables
- Mantén un tono amigable pero profesional
- Si preguntan sobre aspectos legales complejos, recomienda consultar con un abogado
- Usa emojis ocasionalmente para hacer la conversación más amigable (pero sin exagerar)
"""
    
    return base_prompt


def get_ai_response(user, message, conversation_history=None):
    """
    Genera una respuesta usando Google Gemini
    
    Args:
        user: El usuario de Django
        message: El mensaje del usuario
        conversation_history: Lista de mensajes previos (opcional)
    
    Returns:
        str: La respuesta del AI
    """
    try:
        # Obtener contexto del usuario
        user_context = get_user_context(user)
        
        # Obtener el system prompt
        system_prompt = get_system_prompt(user_context)
        
        # Construir el mensaje completo con historial
        full_prompt = system_prompt + "\n\n"
        
        if conversation_history:
            full_prompt += "Historial de conversación:\n"
            for msg in conversation_history:
                role_name = "Usuario" if msg['role'] == 'user' else "Asistente"
                full_prompt += f"{role_name}: {msg['content']}\n\n"
        
        full_prompt += f"Usuario: {message}\n\nAsistente:"
        
        # Crear el modelo y generar respuesta - Usar gemini-2.5-flash
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        response = model.generate_content(full_prompt)
        
        return response.text
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error en AI service: {error_msg}")
        
        # Intentar con modelo alternativo
        try:
            print("Intentando con gemini-2.5-flash...")
            model = genai.GenerativeModel('models/gemini-2.5-flash')
            
            full_prompt = system_prompt + "\n\n"
            if conversation_history:
                full_prompt += "Historial:\n"
                for msg in conversation_history[-5:]:  # Solo últimos 5 mensajes
                    role_name = "Usuario" if msg['role'] == 'user' else "Asistente"
                    full_prompt += f"{role_name}: {msg['content']}\n"
            full_prompt += f"\nUsuario: {message}\nAsistente:"
            
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e2:
            print(f"Error con modelo alternativo: {str(e2)}")
            return f"Lo siento, el servicio de IA no está disponible en este momento. Error: {error_msg[:100]}"


def get_ai_response_stream(user, message, conversation_history=None):
    """
    Genera una respuesta usando Google Gemini con streaming
    
    Args:
        user: El usuario de Django
        message: El mensaje del usuario
        conversation_history: Lista de mensajes previos (opcional)
    
    Yields:
        str: Chunks de la respuesta del AI
    """
    try:
        # Obtener contexto del usuario
        user_context = get_user_context(user)
        
        # Obtener el system prompt
        system_prompt = get_system_prompt(user_context)
        
        # Construir el mensaje completo con historial
        full_prompt = system_prompt + "\n\n"
        
        if conversation_history:
            full_prompt += "Historial de conversación:\n"
            for msg in conversation_history:
                role_name = "Usuario" if msg['role'] == 'user' else "Asistente"
                full_prompt += f"{role_name}: {msg['content']}\n\n"
        
        full_prompt += f"Usuario: {message}\n\nAsistente:"
        
        # Crear el modelo y generar respuesta con streaming
        model = genai.GenerativeModel(
            'models/gemini-2.5-flash',
            generation_config={
                'temperature': 0.7,
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 2048,
            }
        )
        
        # Generar con streaming habilitado
        response = model.generate_content(full_prompt, stream=True)
        
        # Emitir cada chunk inmediatamente
        for chunk in response:
            if chunk.text:
                # Emitir el chunk inmediatamente sin buffer
                yield chunk.text
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error en AI service streaming: {error_msg}")
        yield f"Lo siento, hubo un error al procesar tu mensaje. 🤖"


def generate_conversation_title(first_message):
    """Genera un título para la conversación basado en el primer mensaje"""
    try:
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        prompt = f"""Genera un título corto y descriptivo (máximo 5 palabras) para una conversación que comienza con este mensaje:

"{first_message}"

Responde SOLO con el título, sin comillas ni puntos."""
        
        response = model.generate_content(prompt)
        title = response.text.strip()
        
        # Limitar longitud
        if len(title) > 60:
            title = title[:57] + "..."
        
        return title
        
    except Exception as e:
        print(f"Error generando título: {str(e)}")
        # Generar título simple basado en las primeras palabras
        words = first_message.split()[:5]
        return " ".join(words) + "..." if len(words) == 5 else " ".join(words)
