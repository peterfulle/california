from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Dashboard y perfiles
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Startups
    path('startup/create/', views.create_startup, name='create_startup'),
    path('startup/<int:startup_id>/', views.startup_profile, name='startup_profile'),
    path('startups/', views.startup_directory, name='startup_directory'),
    
    # Investors
    path('investor/create/', views.investor_create, name='investor_create'),
    path('investors/', views.investor_directory, name='investor_directory'),
    path('investor/<int:investor_id>/', views.investor_detail, name='investor_detail'),
    
    # Eventos
    path('events/', views.events_list, name='events_list'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('events/<int:event_id>/toggle-attendance/', views.toggle_event_attendance, name='toggle_event_attendance'),
    path('events/<int:event_id>/comment/', views.add_event_comment, name='add_event_comment'),
    path('events/comment/<int:comment_id>/delete/', views.delete_event_comment, name='delete_event_comment'),
    
    # Contacto
    path('contact/', views.contact_view, name='contact'),
    
    # Sistema de Información Privada
    path('startup/<int:startup_id>/request-access/', views.request_startup_access, name='request_startup_access'),
    path('startup/<int:startup_id>/private/<str:section>/', views.startup_private_section, name='startup_private_section'),
    
    # Pitch Deck Generator
    path('startup/<int:startup_id>/pitch-deck/', views.pitch_deck_generator, name='pitch_deck_generator'),
    path('startup/<int:startup_id>/pitch-deck/generate-slide/', views.generate_pitch_deck_slide, name='generate_pitch_deck_slide'),
    
    # Chatbot IA
    path('chat/', views.chat_interface, name='chat_interface'),
    path('chat/send/', views.send_message, name='send_message'),
    path('chat/send-stream/', views.send_message_stream, name='send_message_stream'),
    path('chat/conversation/<int:conversation_id>/', views.get_conversation, name='get_conversation'),
    path('chat/conversations/', views.get_conversations, name='get_conversations'),
    path('chat/new/', views.new_conversation, name='new_conversation'),
    path('chat/delete/<int:conversation_id>/', views.delete_conversation, name='delete_conversation'),
    
    # Sistema de Conexiones
    path('connections/request/<int:user_id>/', views.send_connection_request, name='send_connection_request'),
    path('connections/requests/', views.connection_requests_list, name='connection_requests'),
    path('connections/accept/<int:request_id>/', views.accept_connection_request, name='accept_connection'),
    path('connections/reject/<int:request_id>/', views.reject_connection_request, name='reject_connection'),
    path('connections/cancel/<int:request_id>/', views.cancel_connection_request, name='cancel_connection'),
    path('connections/', views.my_connections, name='my_connections'),
    
    # Sistema de Mensajería
    path('messages/', views.messages_inbox, name='messages_inbox'),
    path('messages/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    
    # Sistema de Notificaciones
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
]