"""
Servicio de IA para el chatbot usando Google Gemini
"""
import os
import json
import google.generativeai as genai
from google.generativeai.types import content_types
from django.conf import settings
from .models import UserProfile, Startup, InvestorProfile
from decimal import Decimal

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


# ============================================
# FUNCIONES PARA EDITAR LA STARTUP (Function Calling)
# ============================================

def update_startup_field(user, field_name, field_value):
    """
    Actualiza un campo específico de la startup del usuario.
    Solo el fundador puede editar su propia startup.
    
    Args:
        user: Usuario de Django
        field_name: Nombre del campo a actualizar
        field_value: Nuevo valor para el campo
    
    Returns:
        dict: Resultado de la operación
    """
    try:
        profile = user.profile
        if profile.user_type != 'founder':
            return {
                'success': False,
                'message': 'Solo los founders pueden editar startups'
            }
        
        startup = Startup.objects.filter(founder=profile).first()
        if not startup:
            return {
                'success': False,
                'message': 'No se encontró una startup para este usuario'
            }
        
        # Mapeo de campos permitidos
        allowed_fields = {
            'employees_count': int,
            'tagline': str,
            'description': str,
            'sub_industry': str,
            'website': str,
            'pitch_deck_url': str,
            'demo_url': str,
            'problem_statement': str,
            'solution_description': str,
            'market_size': str,
            'business_model': str,
            'competitive_advantage': str,
            'monthly_revenue': Decimal,
            'annual_revenue': Decimal,
            'monthly_users': int,
            'seeking_amount': Decimal,
            'is_fundraising': bool,
        }
        
        if field_name not in allowed_fields:
            return {
                'success': False,
                'message': f'Campo "{field_name}" no permitido para edición'
            }
        
        # Convertir el valor al tipo correcto
        field_type = allowed_fields[field_name]
        try:
            if field_type == bool:
                converted_value = str(field_value).lower() in ['true', 'si', 'sí', 'yes', '1', 'verdadero']
            elif field_type == Decimal:
                converted_value = Decimal(str(field_value))
            else:
                converted_value = field_type(field_value)
        except (ValueError, TypeError) as e:
            return {
                'success': False,
                'message': f'Valor inválido para el campo {field_name}: {str(e)}'
            }
        
        # Actualizar el campo
        setattr(startup, field_name, converted_value)
        startup.save()
        
        # Obtener el nombre legible del campo
        field_labels = {
            'employees_count': 'Número de empleados',
            'tagline': 'Tagline',
            'description': 'Descripción',
            'sub_industry': 'Sub-industria',
            'website': 'Sitio web',
            'monthly_revenue': 'Revenue mensual',
            'annual_revenue': 'Revenue anual',
            'monthly_users': 'Usuarios mensuales',
            'seeking_amount': 'Monto buscado',
            'is_fundraising': 'Estado de fundraising',
        }
        
        field_label = field_labels.get(field_name, field_name)
        
        return {
            'success': True,
            'message': f'✅ {field_label} actualizado correctamente a: {converted_value}',
            'field_name': field_name,
            'new_value': str(converted_value)
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Error al actualizar: {str(e)}'
        }


# Definir las herramientas (tools) para Function Calling
update_startup_tool = {
    'function_declarations': [{
        'name': 'update_startup_field',
        'description': 'Actualiza un campo específico de la startup del usuario. Úsalo cuando el usuario pida modificar, cambiar, actualizar o editar información de su startup.',
        'parameters': {
            'type': 'object',
            'properties': {
                'field_name': {
                    'type': 'string',
                    'description': 'Nombre del campo a actualizar. Opciones: employees_count, tagline, description, sub_industry, website, pitch_deck_url, demo_url, problem_statement, solution_description, market_size, business_model, competitive_advantage, monthly_revenue, annual_revenue, monthly_users, seeking_amount, is_fundraising'
                },
                'field_value': {
                    'type': 'string',
                    'description': 'Nuevo valor para el campo'
                },
            },
            'required': ['field_name', 'field_value']
        }
    }]
}


def get_user_context(user):
    """Obtiene el contexto del usuario para personalizar las respuestas"""
    try:
        profile = user.profile
        context = {
            'user_type': profile.user_type,
            'name': user.get_full_name() or user.username,
            'email': user.email,
        }
        
        # Si es founder, obtener info COMPLETA de su startup
        if profile.user_type == 'founder':
            try:
                startup = Startup.objects.filter(founder=profile).first()
                if startup:
                    context['has_startup'] = True
                    context['startup'] = {
                        'name': startup.company_name,
                        'tagline': startup.tagline,
                        'description': startup.description,
                        'stage': startup.stage,
                        'revenue_stage': startup.revenue_stage,
                        'industry': startup.industry.name if startup.industry else None,
                        'sub_industry': startup.sub_industry,
                        'seeking_amount': startup.seeking_amount,
                        'is_fundraising': startup.is_fundraising,
                        'website': startup.website,
                        'founded_date': str(startup.founded_date) if startup.founded_date else None,
                        'employees_count': startup.employees_count,
                        'business_model': startup.business_model,
                        'problem_statement': startup.problem_statement,
                        'solution_description': startup.solution_description,
                        'market_size': startup.market_size,
                        'competitive_advantage': startup.competitive_advantage,
                        'monthly_revenue': float(startup.monthly_revenue) if startup.monthly_revenue else None,
                        'annual_revenue': float(startup.annual_revenue) if startup.annual_revenue else None,
                        'monthly_users': startup.monthly_users,
                        'total_funding_raised': float(startup.total_funding_raised) if startup.total_funding_raised else 0,
                    }
                else:
                    context['has_startup'] = False
            except Exception as e:
                print(f"Error al obtener startup: {e}")
                context['has_startup'] = False
        
        # Si es investor, obtener su perfil
        elif profile.user_type == 'investor':
            try:
                investor = InvestorProfile.objects.filter(user=user).first()
                if investor:
                    context['has_investor_profile'] = True
                    context['investor'] = {
                        'firm_name': investor.firm_name,
                        'investment_range_min': investor.investment_range_min,
                        'investment_range_max': investor.investment_range_max,
                        'investment_stage': investor.investment_stage,
                        'bio': investor.bio,
                        'investment_thesis': getattr(investor, 'investment_thesis', None),
                    }
                else:
                    context['has_investor_profile'] = False
            except Exception as e:
                print(f"Error al obtener investor profile: {e}")
                context['has_investor_profile'] = False
        
        return context
    except Exception as e:
        print(f"Error en get_user_context: {e}")
        return {'user_type': 'community', 'name': user.username, 'has_startup': False}


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
        has_startup = user_context.get('has_startup', False)
        
        if has_startup:
            startup_info = user_context.get('startup', {})
            
            # Helper para formatear montos de forma segura
            def format_money(value):
                if value is None or value == 0:
                    return "$0"
                return f"${value:,.0f}"
            
            seeking_amount = format_money(startup_info.get('seeking_amount'))
            total_funding = format_money(startup_info.get('total_funding_raised'))
            monthly_rev = format_money(startup_info.get('monthly_revenue'))
            annual_rev = format_money(startup_info.get('annual_revenue'))
            
            base_prompt += f"""
✅ STARTUP REGISTRADA EN LA BASE DE DATOS:

Información completa de la startup de {name}:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 DATOS BÁSICOS:
- Nombre: {startup_info.get('name', 'N/A')}
- Tagline: {startup_info.get('tagline', 'N/A')}
- Descripción: {startup_info.get('description', 'N/A')}
- Industria: {startup_info.get('industry', 'N/A')}
- Sub-industria: {startup_info.get('sub_industry') or 'N/A'}
- Sitio web: {startup_info.get('website') or 'N/A'}
- Fecha de fundación: {startup_info.get('founded_date', 'N/A')}
- Empleados: {startup_info.get('employees_count') or 'N/A'}

💰 FINANCIAMIENTO:
- Etapa: {startup_info.get('stage', 'N/A')}
- Etapa de Revenue: {startup_info.get('revenue_stage') or 'N/A'}
- Buscando: {seeking_amount} USD
- Funding recaudado: {total_funding} USD
- En fundraising activo: {'✅ SÍ' if startup_info.get('is_fundraising') else '❌ NO'}

📊 MODELO DE NEGOCIO:
- Problema: {startup_info.get('problem_statement') or 'N/A'}
- Solución: {startup_info.get('solution_description') or 'N/A'}
- Tamaño del mercado: {startup_info.get('market_size') or 'N/A'}
- Modelo de negocio: {startup_info.get('business_model') or 'N/A'}
- Ventaja competitiva: {startup_info.get('competitive_advantage') or 'N/A'}

📈 MÉTRICAS:
- Revenue mensual: {monthly_rev} USD
- Revenue anual: {annual_rev} USD
- Usuarios mensuales: {startup_info.get('monthly_users') or 'N/A'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INSTRUCCIONES IMPORTANTES:
1. 🎯 **USA ESTA INFORMACIÓN AUTOMÁTICAMENTE**: Cuando el usuario pregunte sobre match con inversores, análisis, pitch deck o cualquier tema relacionado con su startup, UTILIZA DIRECTAMENTE estos datos sin pedirlos de nuevo.

2. 📝 **NO PIDAS INFORMACIÓN QUE YA TIENES**: Si la información está disponible arriba (descripción, industria, etapa, etc.), úsala directamente en tus respuestas.

3. ✏️ **PUEDES EDITAR LA STARTUP**: Cuando el usuario pida modificar, cambiar, actualizar o editar cualquier información de su startup (empleados, descripción, website, revenue, etc.), USA LA FUNCIÓN update_startup_field automáticamente. NO le pidas que vaya al formulario de edición.
   
   Ejemplos de solicitudes de edición:
   - "cambia el número de empleados a 10"
   - "actualiza el revenue mensual a 50000"
   - "modifica la descripción a [nueva descripción]"
   - "edita el website a https://mistartp.com"

4. 🤝 **PARA AI MATCH**: Cuando el usuario pida "match con inversores", analiza automáticamente su perfil con estos datos y sugiere tipos de inversores compatibles basándote en:
   - Industria y sector
   - Etapa de financiamiento
   - Monto buscado
   - Modelo de negocio y tracción

5. 💡 **SÉ PROACTIVO**: Ofrece análisis específicos basados en estos datos reales, no generalidades.

Enfócate en ayudar con:
- Estrategias de fundraising y pitch (usando sus datos reales)
- Match inteligente con inversores (basado en su perfil)
- Desarrollo de producto y mercado
- Modelo de negocio y métricas clave
- Networking estratégico
- Growth hacking específico para su industria
"""
        else:
            base_prompt += f"""
⚠️ STARTUP NO REGISTRADA

{name} es un founder pero AÚN NO ha creado su perfil de startup en la plataforma.

MENSAJE PRIORITARIO PARA EL USUARIO:
Para aprovechar al máximo el AI Match y las recomendaciones personalizadas, necesitas primero registrar tu startup en la plataforma.

👉 Haz clic en "Nueva Startup" en el menú lateral izquierdo para crear tu perfil.

Una vez que registres tu startup con todos los detalles (descripción, industria, etapa, monto buscado, tracción, etc.), podré ayudarte con:
- Match automático con inversores compatibles
- Análisis personalizado de tu startup
- Recomendaciones específicas de fundraising
- Estrategias adaptadas a tu industria y etapa

Mientras tanto, puedo ayudarte con:
- Validación de ideas de negocio
- Guía para crear un pitch deck efectivo
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
    Genera una respuesta usando Google Gemini con Function Calling
    
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
        
        # Crear el modelo CON tools (Function Calling)
        model = genai.GenerativeModel(
            'models/gemini-2.5-flash',
            tools=[update_startup_tool]
        )
        
        # Primera llamada al modelo
        response = model.generate_content(full_prompt)
        
        # Verificar si el modelo quiere llamar a una función
        function_call = None
        try:
            if hasattr(response.candidates[0].content.parts[0], 'function_call'):
                function_call = response.candidates[0].content.parts[0].function_call
        except (IndexError, AttributeError):
            pass
        
        if function_call:
            # Ejecutar la función solicitada
            if function_call.name == 'update_startup_field':
                args = dict(function_call.args)
                result = update_startup_field(
                    user,
                    args.get('field_name'),
                    args.get('field_value')
                )
                
                # Crear respuesta con el resultado de la función
                function_response_part = genai.protos.Part(
                    function_response=genai.protos.FunctionResponse(
                        name='update_startup_field',
                        response={'result': result}
                    )
                )
                
                # Segunda llamada al modelo con el resultado de la función
                response = model.generate_content([
                    full_prompt,
                    response.candidates[0].content,
                    function_response_part
                ])
                
                return response.text
        
        # Si no hay function call, retornar respuesta normal
        return response.text
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error en AI service: {error_msg}")
        
        # Intentar con modelo sin tools
        try:
            print("Intentando con modelo sin function calling...")
            model = genai.GenerativeModel('models/gemini-2.5-flash')
            
            full_prompt = system_prompt + "\n\n"
            if conversation_history:
                full_prompt += "Historial:\n"
                for msg in conversation_history[-5:]:
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


# ============================================
# GENERADOR DE PITCH DECK CON IA
# ============================================

def generate_pitch_deck_slide_content(startup, slide_type, custom_instructions=''):
    """
    Genera el contenido de un slide específico del pitch deck usando IA
    Formato estilo Sequoia Capital
    
    Args:
        startup: Objeto Startup
        slide_type: Tipo de slide (company_purpose, problem, solution, etc.)
        custom_instructions: Instrucciones adicionales del usuario
    
    Returns:
        dict: Contenido estructurado del slide
    """
    try:
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # Construir información de la startup
        startup_info = f"""
INFORMACIÓN DE LA STARTUP:
Nombre: {startup.company_name}
Tagline: {startup.tagline}
Descripción: {startup.description}
Industria: {startup.industry.name if startup.industry else 'N/A'}
Etapa: {startup.get_stage_display()}
Problema: {startup.problem_statement or 'N/A'}
Solución: {startup.solution_description or 'N/A'}
Modelo de negocio: {startup.business_model or 'N/A'}
Tamaño del mercado: {startup.market_size or 'N/A'}
Ventaja competitiva: {startup.competitive_advantage or 'N/A'}
Empleados: {startup.employees_count or 'N/A'}
Revenue mensual: ${startup.monthly_revenue or 0}
Revenue anual: ${startup.annual_revenue or 0}
Usuarios mensuales: {startup.monthly_users or 'N/A'}
Funding buscado: ${startup.seeking_amount or 0}
"""
        
        # Prompts específicos por tipo de slide (Sequoia Capital format)
        slide_prompts = {
            'company_purpose': f"""
Genera el contenido para el slide "COMPANY PURPOSE" (Propósito de la Compañía).
Formato Sequoia Capital - Debe ser conciso y poderoso.

Estructura del slide:
1. **Headline**: Una frase impactante que capture la esencia de la startup (máximo 10 palabras)
2. **Subheadline**: Una línea que expanda el propósito (máximo 15 palabras)
3. **Key Points**: 2-3 puntos bullet que expliquen qué hace la startup y por qué importa

{startup_info}

{f'Instrucciones adicionales: {custom_instructions}' if custom_instructions else ''}

Responde en formato JSON:
{{
    "headline": "...",
    "subheadline": "...",
    "bullets": ["...", "...", "..."]
}}
""",
            
            'problem': f"""
Genera el contenido para el slide "PROBLEM" (Problema).
Formato Sequoia Capital - El problema debe ser claro y urgente.

Estructura del slide:
1. **Title**: Título del problema (5-8 palabras)
2. **Problem Statement**: Descripción clara del problema principal (2-3 líneas)
3. **Pain Points**: 3-4 puntos específicos del dolor que enfrentan los clientes
4. **Market Impact**: Una estadística o dato que muestre la magnitud del problema

{startup_info}

{f'Instrucciones adicionales: {custom_instructions}' if custom_instructions else ''}

Responde en formato JSON:
{{
    "title": "...",
    "problem_statement": "...",
    "pain_points": ["...", "...", "..."],
    "market_impact": "..."
}}
""",
            
            'solution': f"""
Genera el contenido para el slide "SOLUTION" (Solución).
Formato Sequoia Capital - La solución debe ser clara y diferenciadora.

Estructura del slide:
1. **Title**: Título de la solución (5-8 palabras)
2. **Solution Overview**: Descripción de cómo resuelven el problema (2-3 líneas)
3. **Key Features**: 3-4 características clave de la solución
4. **Differentiator**: Por qué es mejor que las alternativas (1-2 líneas)

{startup_info}

{f'Instrucciones adicionales: {custom_instructions}' if custom_instructions else ''}

Responde en formato JSON:
{{
    "title": "...",
    "solution_overview": "...",
    "key_features": ["...", "...", "..."],
    "differentiator": "..."
}}
""",
            
            'market_opportunity': f"""
Genera el contenido para el slide "MARKET OPPORTUNITY" (Oportunidad de Mercado).
Formato Sequoia Capital - Debe mostrar el tamaño y potencial del mercado.

Estructura del slide:
1. **Title**: "Market Opportunity" o título personalizado
2. **TAM (Total Addressable Market)**: Tamaño total del mercado
3. **SAM (Serviceable Addressable Market)**: Mercado al que pueden llegar
4. **SOM (Serviceable Obtainable Market)**: Mercado que pueden capturar realistamente
5. **Growth Rate**: Tasa de crecimiento del mercado

{startup_info}

{f'Instrucciones adicionales: {custom_instructions}' if custom_instructions else ''}

Responde en formato JSON:
{{
    "title": "...",
    "tam": "...",
    "sam": "...",
    "som": "...",
    "growth_rate": "...",
    "insight": "..."
}}
""",
            
            'product': f"""
Genera el contenido para el slide "PRODUCT" (Producto).
Formato Sequoia Capital - Muestra el producto de forma visual y clara.

Estructura del slide:
1. **Title**: Título del producto
2. **Product Description**: Descripción breve del producto (2-3 líneas)
3. **Key Capabilities**: 4-5 capacidades principales
4. **Technology**: Stack tecnológico o innovación técnica (opcional)
5. **Demo Note**: Nota sobre demo o próximos pasos

{startup_info}

{f'Instrucciones adicionales: {custom_instructions}' if custom_instructions else ''}

Responde en formato JSON:
{{
    "title": "...",
    "product_description": "...",
    "key_capabilities": ["...", "...", "...", "..."],
    "technology": "...",
    "demo_note": "..."
}}
""",
            
            'business_model': f"""
Genera el contenido para el slide "BUSINESS MODEL" (Modelo de Negocio).
Formato Sequoia Capital - Debe mostrar claramente cómo generan dinero.

Estructura del slide:
1. **Title**: "Business Model"
2. **Revenue Streams**: Cómo generan ingresos
3. **Pricing Strategy**: Estrategia de precios
4. **Unit Economics**: Métricas clave (CAC, LTV, margins)
5. **Scalability**: Por qué el modelo escala

{startup_info}

{f'Instrucciones adicionales: {custom_instructions}' if custom_instructions else ''}

Responde en formato JSON:
{{
    "title": "...",
    "revenue_streams": ["...", "..."],
    "pricing_strategy": "...",
    "unit_economics": {{"cac": "...", "ltv": "...", "margin": "..."}},
    "scalability": "..."
}}
""",
            
            'traction': f"""
Genera el contenido para el slide "TRACTION" (Tracción).
Formato Sequoia Capital - Métricas y logros concretos.

Estructura del slide:
1. **Title**: "Traction & Metrics"
2. **Key Metrics**: 4-6 métricas clave con números
3. **Growth Rate**: Tasa de crecimiento
4. **Milestones**: Hitos importantes alcanzados
5. **Social Proof**: Testimonios, premios, reconocimientos

{startup_info}

{f'Instrucciones adicionales: {custom_instructions}' if custom_instructions else ''}

Responde en formato JSON:
{{
    "title": "...",
    "key_metrics": [{{"label": "...", "value": "..."}}, ...],
    "growth_rate": "...",
    "milestones": ["...", "...", "..."],
    "social_proof": ["...", "..."]
}}
""",
            
            'competition': f"""
Genera el contenido para el slide "COMPETITION" (Competencia).
Formato Sequoia Capital - Matriz comparativa clara.

Estructura del slide:
1. **Title**: "Competitive Landscape"
2. **Competitors**: Lista de 3-5 competidores principales
3. **Comparison Matrix**: Comparación en 3-4 dimensiones clave
4. **Our Advantage**: Por qué somos diferentes y mejores

{startup_info}

{f'Instrucciones adicionales: {custom_instructions}' if custom_instructions else ''}

Responde en formato JSON:
{{
    "title": "...",
    "competitors": ["...", "...", "..."],
    "comparison_dimensions": ["...", "...", "..."],
    "our_advantage": "..."
}}
""",
            
            'team': f"""
Genera el contenido para el slide "TEAM" (Equipo).
Formato Sequoia Capital - Destaca experiencia y credibilidad.

Estructura del slide:
1. **Title**: "Team"
2. **Founders**: Información de fundadores (nombre, rol, background relevante)
3. **Key Team Members**: Miembros clave del equipo (si aplica)
4. **Advisors**: Asesores o board members importantes
5. **Team Strength**: Por qué este equipo puede ejecutar la visión

{startup_info}

{f'Instrucciones adicionales: {custom_instructions}' if custom_instructions else ''}

Responde en formato JSON:
{{
    "title": "...",
    "founders": [{{"name": "...", "role": "...", "background": "..."}}, ...],
    "key_members": ["...", "..."],
    "advisors": ["...", "..."],
    "team_strength": "..."
}}
""",
            
            'financials': f"""
Genera el contenido para el slide "FINANCIALS" (Financiero).
Formato Sequoia Capital - Proyecciones realistas y métricas actuales.

Estructura del slide:
1. **Title**: "Financial Projections"
2. **Current State**: Estado financiero actual (revenue, burn rate)
3. **3-Year Projection**: Proyección de revenue a 3 años
4. **Key Assumptions**: Supuestos principales de las proyecciones
5. **Break-even**: Cuándo alcanzarán el break-even

{startup_info}

{f'Instrucciones adicionales: {custom_instructions}' if custom_instructions else ''}

Responde en formato JSON:
{{
    "title": "...",
    "current_state": {{"revenue": "...", "burn_rate": "...", "runway": "..."}},
    "projections": [{{"year": "2025", "revenue": "..."}}, ...],
    "key_assumptions": ["...", "...", "..."],
    "break_even": "..."
}}
""",
            
            'ask': f"""
Genera el contenido para el slide "THE ASK" (La Petición).
Formato Sequoia Capital - Claro y directo sobre lo que necesitan.

Estructura del slide:
1. **Title**: "The Ask"
2. **Amount**: Cantidad que están buscando
3. **Use of Funds**: Cómo usarán el dinero (breakdown por categoría)
4. **Milestones**: Qué lograrán con esta inversión
5. **Timeline**: Timeline para alcanzar los hitos

{startup_info}

{f'Instrucciones adicionales: {custom_instructions}' if custom_instructions else ''}

Responde en formato JSON:
{{
    "title": "...",
    "amount": "...",
    "use_of_funds": [{{"category": "...", "percentage": "...", "description": "..."}}, ...],
    "milestones": ["...", "...", "..."],
    "timeline": "..."
}}
"""
        }
        
        # Obtener el prompt para el tipo de slide
        prompt = slide_prompts.get(slide_type, f"Genera contenido para el slide de tipo: {slide_type}")
        
        # Generar respuesta
        response = model.generate_content(prompt)
        
        # Parsear JSON response
        import json
        import re
        
        # Extraer JSON del response (puede venir con markdown)
        text = response.text.strip()
        # Remover markdown code blocks si existen
        json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        if json_match:
            text = json_match.group(1)
        elif text.startswith('```') and text.endswith('```'):
            text = text[3:-3].strip()
            if text.startswith('json'):
                text = text[4:].strip()
        
        content = json.loads(text)
        
        return {
            'success': True,
            'slide_type': slide_type,
            'content': content
        }
        
    except Exception as e:
        print(f"Error generando slide: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'slide_type': slide_type
        }
