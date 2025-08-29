#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append('/Users/peterfulle/Desktop/siliconfounder-main')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mydevsite.settings')

django.setup()

from core.models import Industry, UserProfile, Startup, InvestorProfile
from django.contrib.auth.models import User

def create_sample_data():
    # Crear industrias
    industries_data = [
        "Fintech", "HealthTech", "EdTech", "E-commerce", "SaaS", 
        "Marketplace", "IoT", "AI/ML", "Blockchain", "Cybersecurity",
        "Gaming", "Food Tech", "PropTech", "CleanTech", "AgriTech",
        "Transportation", "Media", "Enterprise Software", "Consumer Apps", "B2B Services"
    ]
    
    industries = []
    for name in industries_data:
        industry, created = Industry.objects.get_or_create(name=name)
        industries.append(industry)
        if created:
            print(f"Created industry: {name}")
    
    # Crear usuarios de ejemplo
    users_data = [
        {
            'username': 'founder1',
            'email': 'founder1@example.com',
            'first_name': 'María',
            'last_name': 'García',
            'password': 'password123',
            'user_type': 'founder'
        },
        {
            'username': 'founder2', 
            'email': 'founder2@example.com',
            'first_name': 'Carlos',
            'last_name': 'López',
            'password': 'password123',
            'user_type': 'founder'
        },
        {
            'username': 'investor1',
            'email': 'investor1@example.com', 
            'first_name': 'Ana',
            'last_name': 'Martínez',
            'password': 'password123',
            'user_type': 'investor'
        },
        {
            'username': 'investor2',
            'email': 'investor2@example.com',
            'first_name': 'Roberto',
            'last_name': 'Silva',
            'password': 'password123',
            'user_type': 'investor'
        }
    ]
    
    created_users = []
    for user_data in users_data:
        try:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                password=user_data['password']
            )
            
            # Crear perfil de usuario
            profile = UserProfile.objects.create(
                user=user,
                user_type=user_data['user_type'],
                bio=f"Bio de ejemplo para {user.get_full_name()}"
            )
            
            created_users.append((user, profile))
            print(f"Created user: {user.username} ({user_data['user_type']})")
            
        except Exception as e:
            print(f"Error creating user {user_data['username']}: {e}")
    
    # Crear startups de ejemplo
    founder_users = [u for u, p in created_users if p.user_type == 'founder']
    
    if len(founder_users) >= 2:
        # Startup 1
        try:
            startup1 = Startup.objects.create(
                founder=founder_users[0].profile,
                company_name="TechSolutions AI",
                tagline="Revolucionando la automatización empresarial con IA",
                description="Desarrollamos soluciones de inteligencia artificial para automatizar procesos empresariales complejos, ayudando a las empresas a aumentar su eficiencia en un 40%.",
                industry=industries[7],  # AI/ML
                stage='growth',
                founded_date='2022-01-15',
                website='https://techsolutions-ai.com',
                employees_count=25,
                total_funding_raised=2500000.0,
                monthly_revenue=45000.0,
                is_fundraising=True,
                seeking_amount=5000000.0,
                problem_statement="Las empresas gastan miles de horas en procesos manuales repetitivos que podrían automatizarse.",
                solution_description="Nuestra plataforma utiliza IA avanzada para identificar y automatizar procesos empresariales, reduciendo costos y errores humanos.",
                market_size="El mercado de automatización empresarial vale $8.8B y crecerá 9.1% anual hasta 2027.",
                business_model="SaaS con suscripción mensual ($500-5000/mes) y servicios de consultoría especializada."
            )
            print(f"Created startup: {startup1.company_name}")
        except Exception as e:
            print(f"Error creating startup 1: {e}")
        
        # Startup 2
        try:
            startup2 = Startup.objects.create(
                founder=founder_users[1].profile,
                company_name="EcoMarket",
                tagline="Marketplace sostenible para productos eco-friendly",
                description="Conectamos consumidores conscientes con marcas sostenibles, facilitando la compra de productos respetuosos con el medio ambiente.",
                industry=industries[3],  # E-commerce
                stage='early_traction',
                founded_date='2023-03-20',
                website='https://ecomarket.es',
                employees_count=8,
                total_funding_raised=500000.0,
                monthly_revenue=12000.0,
                is_fundraising=True,
                seeking_amount=1500000.0,
                problem_statement="Es difícil para los consumidores encontrar productos verdaderamente sostenibles en un solo lugar.",
                solution_description="Marketplace verificado que garantiza que todos los productos cumplen estrictos criterios de sostenibilidad.",
                market_size="El mercado de productos sostenibles vale $150B y crece 15% anualmente.",
                business_model="Comisión por venta (5-8%) y suscripciones premium para vendedores ($99-499/mes)."
            )
            print(f"Created startup: {startup2.company_name}")
        except Exception as e:
            print(f"Error creating startup 2: {e}")
    
    # Crear perfiles de inversores
    investor_users = [u for u, p in created_users if p.user_type == 'investor']
    
    if len(investor_users) >= 2:
        # Inversor 1
        try:
            investor1 = InvestorProfile.objects.create(
                user=investor_users[0],
                fund_name="InnovaVC",
                investor_type='vc_fund',
                fund_size=50000000.0,
                investment_stages=['seed', 'series_a'],
                geographic_focus='europe',
                min_investment=100000.0,
                max_investment=2000000.0,
                typical_investment=500000.0,
                portfolio_companies_count=45,
                investments_per_year=12,
                thesis="Invertimos in startups B2B con tracción comprobada y potencial de escalabilidad internacional en SaaS, AI/ML y Enterprise Software.",
                sweet_spot="Series A de startups B2B con €500K ARR y crecimiento 10%+ mensual.",
                notable_investments="Unicorn SaaS (€50M exit), TechStarter (€20M Series B), DataFlow (€15M Series A)",
                is_actively_investing=True
            )
            print(f"Created investor: {investor1.user.get_full_name()}")
        except Exception as e:
            print(f"Error creating investor 1: {e}")
        
        # Inversor 2  
        try:
            investor2 = InvestorProfile.objects.create(
                user=investor_users[1],
                fund_name="GreenTech Capital",
                investor_type='angel',
                fund_size=25000000.0,
                investment_stages=['pre_seed', 'seed'],
                geographic_focus='europe',
                min_investment=50000.0,
                max_investment=500000.0,
                typical_investment=150000.0,
                portfolio_companies_count=20,
                investments_per_year=8,
                thesis="Apoyo startups que combinan tecnología con impacto ambiental positivo y modelos de negocio escalables en CleanTech, AgriTech y Food Tech.",
                sweet_spot="Pre-seed/Seed de startups de impacto con MVP validado y equipo técnico sólido.",
                notable_investments="CleanEnergy Pro (€10M Series A), BioTech Solutions (€8M exit), SustainableFood (€5M Series A)",
                is_actively_investing=True
            )
            print(f"Created investor: {investor2.user.get_full_name()}")
        except Exception as e:
            print(f"Error creating investor 2: {e}")
    
    print("\n✅ Sample data created successfully!")
    print("Login credentials:")
    print("Founders: founder1/password123, founder2/password123")
    print("Investors: investor1/password123, investor2/password123")

if __name__ == '__main__':
    create_sample_data()
