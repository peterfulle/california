from django.core.management.base import BaseCommand
from core.models import Industry

class Command(BaseCommand):
    help = 'Crea las industrias por defecto en la base de datos'

    def handle(self, *args, **options):
        """Comando para crear las industrias por defecto"""
        
        industries_data = [
            # Tecnología
            {'name': 'FinTech', 'description': 'Tecnología financiera y servicios bancarios digitales'},
            {'name': 'HealthTech', 'description': 'Tecnología para el sector salud y medicina'},
            {'name': 'EdTech', 'description': 'Tecnología educativa y plataformas de aprendizaje'},
            {'name': 'AI/ML', 'description': 'Inteligencia artificial y machine learning'},
            {'name': 'SaaS', 'description': 'Software como servicio y herramientas empresariales'},
            {'name': 'CleanTech', 'description': 'Tecnología limpia y sostenibilidad ambiental'},
            {'name': 'AgriTech', 'description': 'Tecnología agrícola y agricultura de precisión'},
            {'name': 'PropTech', 'description': 'Tecnología inmobiliaria y gestión de propiedades'},
            {'name': 'FoodTech', 'description': 'Tecnología alimentaria y delivery'},
            {'name': 'RetailTech', 'description': 'Tecnología para el sector retail y comercio'},
            
            # Comercio y Servicios
            {'name': 'E-commerce', 'description': 'Comercio electrónico y marketplaces'},
            {'name': 'Marketplace', 'description': 'Plataformas de intercambio y marketplace'},
            {'name': 'Logística', 'description': 'Logística, transporte y distribución'},
            {'name': 'Travel & Tourism', 'description': 'Viajes, turismo y hospitalidad'},
            {'name': 'Real Estate', 'description': 'Bienes raíces e inmobiliaria'},
            
            # Entretenimiento y Media
            {'name': 'Gaming', 'description': 'Videojuegos y entretenimiento digital'},
            {'name': 'Media & Entertainment', 'description': 'Medios de comunicación y entretenimiento'},
            {'name': 'CreatorTech', 'description': 'Herramientas para creadores de contenido'},
            {'name': 'Sports & Fitness', 'description': 'Deportes, fitness y bienestar'},
            
            # Servicios Empresariales
            {'name': 'HRTech', 'description': 'Tecnología de recursos humanos'},
            {'name': 'LegalTech', 'description': 'Tecnología legal y compliance'},
            {'name': 'Marketing & Sales', 'description': 'Marketing digital y herramientas de ventas'},
            {'name': 'CyberSecurity', 'description': 'Ciberseguridad y protección de datos'},
            {'name': 'DevTools', 'description': 'Herramientas para desarrolladores'},
            
            # Sectores Tradicionales
            {'name': 'Manufacturing', 'description': 'Manufactura e industria 4.0'},
            {'name': 'Energy', 'description': 'Energía y recursos naturales'},
            {'name': 'Automotive', 'description': 'Automotriz y movilidad'},
            {'name': 'Healthcare', 'description': 'Servicios de salud tradicionales'},
            {'name': 'Financial Services', 'description': 'Servicios financieros tradicionales'},
            {'name': 'Consulting', 'description': 'Consultoría y servicios profesionales'},
            
            # Nuevos Sectores
            {'name': 'Web3 & Crypto', 'description': 'Blockchain, criptomonedas y Web3'},
            {'name': 'IoT', 'description': 'Internet de las cosas y dispositivos conectados'},
            {'name': 'Robotics', 'description': 'Robótica y automatización'},
            {'name': 'Space Tech', 'description': 'Tecnología espacial y aeroespacial'},
            {'name': 'Biotech', 'description': 'Biotecnología e investigación científica'},
        ]
        
        created_count = 0
        updated_count = 0
        
        self.stdout.write(
            self.style.SUCCESS(f'🚀 Iniciando creación de {len(industries_data)} industrias...')
        )
        
        for industry_data in industries_data:
            industry, created = Industry.objects.get_or_create(
                name=industry_data['name'],
                defaults={
                    'description': industry_data['description'],
                    'slug': industry_data['name'].lower().replace(' ', '-').replace('&', 'and').replace('/', '-')
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Creada: {industry.name}')
                )
            else:
                # Actualizar descripción si no existe
                if not industry.description:
                    industry.description = industry_data['description']
                    industry.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'🔄 Actualizada: {industry.name}')
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Proceso completado:\n'
                f'   • {created_count} industrias creadas\n'
                f'   • {updated_count} industrias actualizadas\n'
                f'   • {Industry.objects.count()} industrias totales en la BD'
            )
        )
