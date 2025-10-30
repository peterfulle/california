"""
WebSocket Consumers para chat en tiempo real
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Conversation, Message, Notification

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Consumer para chat en tiempo real
    Maneja:
    - Envío y recepción de mensajes
    - Indicador de "está escribiendo"
    - Notificaciones de lectura
    """
    
    async def connect(self):
        """Cuando un usuario se conecta al WebSocket"""
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        self.user = self.scope['user']
        
        # Verificar que el usuario esté autenticado
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Unirse al grupo de la conversación
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Notificar que el usuario se conectó
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'user_id': self.user.id,
                'status': 'online',
                'username': self.user.get_full_name()
            }
        )
    
    async def disconnect(self, close_code):
        """Cuando un usuario se desconecta"""
        # Verificar que el usuario esté autenticado antes de notificar
        if self.user.is_authenticated:
            # Notificar que el usuario se desconectó
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_status',
                    'user_id': self.user.id,
                    'status': 'offline',
                    'username': self.user.get_full_name()
                }
            )
        
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Recibir mensaje del WebSocket"""
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'chat_message':
            # Mensaje de chat
            content = data['message']
            
            # Guardar mensaje en la base de datos
            message = await self.save_message(content)
            
            # Obtener avatar URL de forma asíncrona
            avatar_url = await self.get_user_avatar()
            
            # Enviar mensaje a todos en el grupo
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': content,
                    'message_id': message.id,
                    'sender_id': self.user.id,
                    'sender_name': self.user.get_full_name(),
                    'timestamp': message.created_at.strftime('%H:%M'),
                    'avatar_url': avatar_url,
                }
            )
            
        elif message_type == 'typing':
            # Indicador de "está escribiendo"
            is_typing = data.get('is_typing', False)
            
            # Enviar a todos excepto al remitente
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'user_id': self.user.id,
                    'username': self.user.get_full_name(),
                    'is_typing': is_typing,
                }
            )
        
        elif message_type == 'mark_read':
            # Marcar mensajes como leídos
            await self.mark_messages_read()
    
    async def chat_message(self, event):
        """Enviar mensaje de chat al WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'message_id': event['message_id'],
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name'],
            'timestamp': event['timestamp'],
            'avatar_url': event.get('avatar_url'),
        }))
    
    async def typing_indicator(self, event):
        """Enviar indicador de escritura al WebSocket"""
        # No enviar el indicador al usuario que está escribiendo
        if event['user_id'] != self.user.id:
            await self.send(text_data=json.dumps({
                'type': 'typing',
                'user_id': event['user_id'],
                'username': event['username'],
                'is_typing': event['is_typing'],
            }))
    
    async def user_status(self, event):
        """Enviar estado del usuario al WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'user_status',
            'user_id': event['user_id'],
            'username': event['username'],
            'status': event['status'],
        }))
    
    async def meet_started(self, event):
        """Enviar notificación de videollamada iniciada"""
        await self.send(text_data=json.dumps({
            'type': 'meet_started',
            'meet_link': event['meet_link'],
            'creator_id': event['creator_id'],
            'creator_name': event['creator_name'],
            'conversation_id': event['conversation_id'],
        }))
    
    async def meet_request_sent(self, event):
        """Enviar notificación de solicitud de videollamada enviada"""
        await self.send(text_data=json.dumps({
            'type': 'meet_request_sent',
            'request_id': event['request_id'],
            'requester_id': event['requester_id'],
            'requester_name': event['requester_name'],
            'receiver_id': event['receiver_id'],
            'conversation_id': event['conversation_id'],
        }))
    
    async def meet_request_accepted(self, event):
        """Enviar notificación de solicitud de videollamada aceptada"""
        await self.send(text_data=json.dumps({
            'type': 'meet_request_accepted',
            'request_id': event['request_id'],
            'meet_link': event['meet_link'],
            'acceptor_id': event['acceptor_id'],
            'acceptor_name': event['acceptor_name'],
            'requester_id': event['requester_id'],
            'conversation_id': event['conversation_id'],
        }))
    
    async def meet_request_rejected(self, event):
        """Enviar notificación de solicitud de videollamada rechazada"""
        await self.send(text_data=json.dumps({
            'type': 'meet_request_rejected',
            'request_id': event['request_id'],
            'rejecter_id': event['rejecter_id'],
            'rejecter_name': event['rejecter_name'],
            'requester_id': event['requester_id'],
            'conversation_id': event['conversation_id'],
        }))
    
    @database_sync_to_async
    def save_message(self, content):
        """Guardar mensaje en la base de datos y crear notificación"""
        conversation = Conversation.objects.get(id=self.conversation_id)
        message = Message.objects.create(
            conversation=conversation,
            sender=self.user,
            content=content
        )
        
        # Crear notificación para el otro participante
        recipient = conversation.get_other_participant(self.user)
        if recipient:
            # Limitar preview a 100 caracteres
            preview = content if len(content) <= 100 else content[:97] + '...'
            Notification.objects.create(
                user=recipient,
                message=message,
                conversation=conversation,
                content=f"{self.user.get_full_name()}: {preview}"
            )
        
        return message
    
    @database_sync_to_async
    def mark_messages_read(self):
        """Marcar mensajes como leídos"""
        conversation = Conversation.objects.get(id=self.conversation_id)
        Message.objects.filter(
            conversation=conversation,
            is_read=False
        ).exclude(
            sender=self.user
        ).update(is_read=True)
    
    @database_sync_to_async
    def get_user_avatar(self):
        """Obtener URL del avatar del usuario de forma asíncrona"""
        try:
            if self.user.profile and self.user.profile.profile_image:
                return self.user.profile.profile_image.url
        except:
            pass
        return None
