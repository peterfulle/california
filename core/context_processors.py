"""
Context processors para inyectar datos globales en todos los templates
"""
from .models import Notification


def notifications_context(request):
    """
    Inyecta el contador de notificaciones no leídas en todos los templates
    """
    unread_count = 0
    
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
    
    return {
        'unread_notifications_count': unread_count
    }
