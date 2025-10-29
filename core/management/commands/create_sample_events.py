from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Event
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Crea datos de prueba para eventos'

    def handle(self, *args, **options):
        # Asegurar que hay al menos un usuario
        if not User.objects.exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )

        # Obtener un usuario para crear eventos
        user = User.objects.first()

        # Datos de muestra
        event_titles = [
            'Networking Tech Startups',
            'Workshop: Pitch Perfect',
            'Inversión en Startups 101',
            'Demo Day 2024',
            'Hackathon: IA para Startups',
            'Meetup: Blockchain y Web3',
            'Taller de Growth Hacking',
            'Fintech Innovation Summit',
            'Startup Legal Workshop',
            'VC Roundtable Discussion'
        ]

        event_descriptions = [
            'Únete a nosotros para una noche de networking con las startups tech más innovadoras.',
            'Aprende a perfeccionar tu pitch con expertos en inversión.',
            'Todo lo que necesitas saber sobre inversión en startups.',
            'Las mejores startups presentan sus proyectos a inversores.',
            '48 horas de codificación intensiva enfocada en soluciones de IA.',
            'Explorando el futuro de Web3 y las oportunidades en blockchain.',
            'Estrategias avanzadas de growth hacking para tu startup.',
            'Descubre las últimas tendencias en tecnología financiera.',
            'Aspectos legales clave para startups y emprendedores.',
            'Mesa redonda con VCs líderes discutiendo el panorama de inversión.'
        ]

        locations = [
            'Centro de Innovación',
            'Hotel Business Center',
            'Campus Tecnológico',
            'Centro de Convenciones',
            'Hub de Startups',
            'Espacio de Coworking Downtown',
            'Universidad de Tecnología',
            'Centro Empresarial',
            'Innovation Lab',
            'Tech Park'
        ]

        # Crear eventos
        for i in range(10):
            days_offset = random.randint(-30, 60)  # Eventos entre 30 días atrás y 60 días adelante
            event_date = timezone.now().date() + timedelta(days=days_offset)
            event_time = f"{random.randint(9,20)}:00"  # Eventos entre 9 AM y 8 PM
            
            Event.objects.create(
                creator=user,
                title=event_titles[i],
                description=event_descriptions[i],
                date=event_date,
                time=event_time,
                location=locations[i],
                event_type=random.choice(['networking', 'workshop', 'conference', 'hackathon']),
                theme=random.choice(['modern', 'classic', 'tech', 'corporate']),
                capacity=random.choice([50, 100, 150, 200, None]),
                is_private=random.choice([True, False]),
                status='published'
            )

        self.stdout.write(self.style.SUCCESS('Se crearon exitosamente los eventos de prueba'))
