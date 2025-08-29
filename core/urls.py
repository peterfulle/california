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
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/comment/', views.add_event_comment, name='add_event_comment'),
    path('event/<int:event_id>/attendance/', views.update_event_attendance, name='update_event_attendance'),
    path('event/<int:event_id>/comments/', views.get_event_comments, name='get_event_comments'),
    
    # Contacto
    path('contact/', views.contact_view, name='contact'),
    
    # Sistema de Información Privada
    path('startup/<int:startup_id>/request-access/', views.request_startup_access, name='request_startup_access'),
    path('startup/<int:startup_id>/private/<str:section>/', views.startup_private_section, name='startup_private_section'),
]