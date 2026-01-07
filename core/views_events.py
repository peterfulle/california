from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Event
import json

@login_required
def create_event(request):
    """Vista para crear un nuevo evento con temas predefinidos"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Crear el evento
            event = Event.objects.create(
                title=data['title'],
                description=data['description'],
                event_type=data['type'],
                location=data['location'],
                max_attendees=data['capacity'],
                is_public=data['isPublic'],
                theme=data['theme_id'],
                organizer=request.user,
                start_datetime=timezone.make_aware(parse_datetime(f"{data['date']} {data['time']}")),
                status='published'
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Evento creado exitosamente',
                'redirect_url': event.get_absolute_url()
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return render(request, 'core/event_create.html')

@login_required
def event_detail(request, event_id):
    """Vista detallada del evento con diseño tipo Partiful"""
    event = get_object_or_404(Event, id=event_id)
    
    context = {
        'event': event,
        'is_organizer': request.user == event.organizer,
        'user_rsvp': event.eventattendance_set.filter(user=request.user).first(),
        'attendees_count': event.eventattendance_set.count(),
        'comments': event.eventcomment_set.order_by('-created_at')[:10],
    }
    
    return render(request, 'core/event_detail.html', context)
