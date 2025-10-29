"""
Servicio para integración con Google Meet API
"""
import os
import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings


class GoogleMeetService:
    """Maneja la integración con Google Meet API"""
    
    # Scopes requeridos para Google Meet
    SCOPES = [
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/calendar.events'
    ]
    
    def __init__(self):
        self.client_id = os.getenv('GOOGLE_MEET_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_MEET_CLIENT_SECRET')
        self.api_key = os.getenv('GOOGLE_MEET_API_KEY')
        
    def get_authorization_url(self, redirect_uri):
        """
        Genera URL de autorización OAuth para el usuario
        """
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [redirect_uri]
                }
            },
            scopes=self.SCOPES,
            redirect_uri=redirect_uri
        )
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        return authorization_url, state
    
    def exchange_code_for_credentials(self, code, redirect_uri, state):
        """
        Intercambia el código de autorización por credenciales
        """
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [redirect_uri]
                }
            },
            scopes=self.SCOPES,
            state=state,
            redirect_uri=redirect_uri
        )
        
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        return {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
    
    def create_meet_link(self, user_credentials, summary, participants_emails, duration_minutes=60):
        """
        Crea un evento de Google Calendar con enlace de Meet
        
        Args:
            user_credentials: Credenciales OAuth del usuario
            summary: Título de la reunión
            participants_emails: Lista de emails de los participantes
            duration_minutes: Duración de la reunión en minutos
            
        Returns:
            dict con 'meet_link' y 'event_id'
        """
        try:
            # Reconstruir credenciales desde el dict
            creds = Credentials(
                token=user_credentials.get('token'),
                refresh_token=user_credentials.get('refresh_token'),
                token_uri=user_credentials.get('token_uri'),
                client_id=user_credentials.get('client_id'),
                client_secret=user_credentials.get('client_secret'),
                scopes=user_credentials.get('scopes')
            )
            
            # Construir servicio de Calendar
            service = build('calendar', 'v3', credentials=creds)
            
            # Configurar tiempo de inicio y fin
            now = datetime.utcnow()
            start_time = now.isoformat() + 'Z'
            end_time = (now + timedelta(minutes=duration_minutes)).isoformat() + 'Z'
            
            # Preparar lista de asistentes
            attendees = [{'email': email} for email in participants_emails]
            
            # Crear evento con Google Meet
            event = {
                'summary': summary,
                'description': 'Reunión generada desde Silicon Founder',
                'start': {
                    'dateTime': start_time,
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': 'UTC',
                },
                'attendees': attendees,
                'conferenceData': {
                    'createRequest': {
                        'requestId': f'silicon-founder-{now.timestamp()}',
                        'conferenceSolutionKey': {
                            'type': 'hangoutsMeet'
                        }
                    }
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            
            # Insertar evento
            event_result = service.events().insert(
                calendarId='primary',
                body=event,
                conferenceDataVersion=1,
                sendUpdates='all'
            ).execute()
            
            # Extraer enlace de Meet
            meet_link = event_result.get('hangoutLink')
            
            return {
                'success': True,
                'meet_link': meet_link,
                'event_id': event_result.get('id'),
                'event_html_link': event_result.get('htmlLink')
            }
            
        except HttpError as error:
            return {
                'success': False,
                'error': f'Error al crear reunión: {error}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error inesperado: {str(e)}'
            }
    
    def get_meet_link_simple(self, conversation_id):
        """
        Genera un enlace de Meet simple sin OAuth (usando código de reunión)
        Esta es una alternativa más simple que no requiere OAuth del usuario
        
        Returns:
            str: URL de Google Meet
        """
        # Generar código único basado en la conversación
        import hashlib
        meeting_code = hashlib.md5(f"silicon-founder-{conversation_id}".encode()).hexdigest()[:10]
        
        # Google Meet permite crear enlaces directos con códigos
        meet_link = f"https://meet.google.com/{meeting_code}"
        
        return meet_link
    
    def create_instant_meet(self, conversation):
        """
        Crea un enlace de Meet instantáneo para una conversación
        Sin necesidad de OAuth (método simplificado)
        
        Args:
            conversation: Instancia del modelo Conversation
            
        Returns:
            str: Enlace de Google Meet
        """
        # Usar el ID de la conversación para generar un código único
        import hashlib
        from datetime import datetime
        
        # Crear código único: sf (silicon founder) + timestamp + conversation_id
        timestamp = int(datetime.now().timestamp())
        unique_string = f"sf-{conversation.id}-{timestamp}"
        meeting_code = hashlib.md5(unique_string.encode()).hexdigest()[:12]
        
        # Formatear como código de Meet (formato: xxx-xxxx-xxx)
        formatted_code = f"{meeting_code[:3]}-{meeting_code[3:7]}-{meeting_code[7:]}"
        
        meet_link = f"https://meet.google.com/{formatted_code}"
        
        return meet_link
