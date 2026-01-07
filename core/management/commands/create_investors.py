from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile, InvestorProfile


class Command(BaseCommand):
    help = 'Crea inversores de ejemplo para la plataforma'

    def handle(self, *args, **options):
        self.stdout.write('Creando inversores de ejemplo...\n')
        
        investors_data = [
            {
                'username': 'investor1',
                'email': 'investor1@example.com',
                'first_name': 'María',
                'last_name': 'González',
                'bio': 'Angel investor con 10 años de experiencia en tecnología',
                'location': 'San Francisco, CA',
                'fund_name': 'TechAngel Ventures',
                'investor_type': 'angel',
                'fund_size': 5000000,
                'min_investment': 50000,
                'max_investment': 250000,
                'typical_investment': 100000,
                'thesis': 'Invierto en startups B2B SaaS en etapa temprana con tracción demostrable',
                'sweet_spot': 'Series A, startups con ARR >$500k',
                'geographic_focus': 'north_america',
                'investment_stages': ['seed', 'series_a'],
            },
            {
                'username': 'investor2',
                'email': 'investor2@example.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'bio': 'Managing Partner at Valley Capital Partners',
                'location': 'Palo Alto, CA',
                'fund_name': 'Valley Capital Partners',
                'investor_type': 'vc_fund',
                'fund_size': 50000000,
                'min_investment': 500000,
                'max_investment': 5000000,
                'typical_investment': 2000000,
                'thesis': 'Invertimos en empresas de tecnología disruptiva en etapas de crecimiento',
                'sweet_spot': 'Series B-C, empresas tech con product-market fit',
                'geographic_focus': 'global',
                'investment_stages': ['series_a', 'series_b', 'series_c'],
            },
            {
                'username': 'investor3',
                'email': 'investor3@example.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'bio': 'Head of Corporate Ventures',
                'location': 'Mountain View, CA',
                'fund_name': 'Corporate Innovation Fund',
                'investor_type': 'corporate_vc',
                'fund_size': 100000000,
                'min_investment': 1000000,
                'max_investment': 10000000,
                'typical_investment': 3000000,
                'thesis': 'Inversión estratégica en tecnologías que complementan nuestro core business',
                'sweet_spot': 'Series B+, empresas con fit estratégico',
                'geographic_focus': 'global',
                'investment_stages': ['series_b', 'series_c', 'growth'],
            },
            {
                'username': 'investor4',
                'email': 'investor4@example.com',
                'first_name': 'David',
                'last_name': 'Chen',
                'bio': 'Family Office Investment Manager',
                'location': 'San Jose, CA',
                'fund_name': 'Silicon Family Office',
                'investor_type': 'family_office',
                'fund_size': 25000000,
                'min_investment': 250000,
                'max_investment': 2500000,
                'typical_investment': 1000000,
                'thesis': 'Inversiones de largo plazo en tecnología y healthcare',
                'sweet_spot': 'Series A-B, empresas con fundadores experimentados',
                'geographic_focus': 'north_america',
                'investment_stages': ['seed', 'series_a', 'series_b'],
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for data in investors_data:
            # Crear usuario
            user, user_created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name']
                }
            )
            
            if user_created:
                user.set_password('password123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Usuario creado: {user.username}'))
            
            # Crear/actualizar UserProfile
            profile, _ = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'user_type': 'investor',
                    'bio': data['bio'],
                    'location': data['location']
                }
            )
            
            # Crear/actualizar InvestorProfile
            investor, inv_created = InvestorProfile.objects.update_or_create(
                user=user,
                defaults={
                    'fund_name': data['fund_name'],
                    'investor_type': data['investor_type'],
                    'fund_size': data['fund_size'],
                    'min_investment': data['min_investment'],
                    'max_investment': data['max_investment'],
                    'typical_investment': data['typical_investment'],
                    'thesis': data['thesis'],
                    'sweet_spot': data['sweet_spot'],
                    'geographic_focus': data['geographic_focus'],
                    'investment_stages': data['investment_stages'],
                    'is_active': True,
                    'is_accepting_pitches': True,
                }
            )
            
            if inv_created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ InvestorProfile creado: {investor.fund_name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'↻ InvestorProfile actualizado: {investor.fund_name}'))
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('✅ Proceso completado'))
        self.stdout.write(self.style.SUCCESS(f'   • {created_count} inversores creados'))
        self.stdout.write(self.style.SUCCESS(f'   • {updated_count} inversores actualizados'))
        self.stdout.write('='*50 + '\n')
