#!/usr/bin/env python
"""
Script para crear inversores de ejemplo
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mydevsite.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile, InvestorProfile

def create_sample_investors():
    print("Creando inversores de ejemplo...")
    
    # Inversor 1: Angel Investor
    user1, created1 = User.objects.get_or_create(
        username='investor1',
        defaults={
            'email': 'investor1@example.com',
            'first_name': 'María',
            'last_name': 'González'
        }
    )
    if created1:
        user1.set_password('password123')
        user1.save()
        print(f"✓ Usuario creado: {user1.username}")
    
    profile1, created_p1 = UserProfile.objects.get_or_create(
        user=user1,
        defaults={
            'user_type': 'investor',
            'bio': 'Angel investor con 10 años de experiencia en tecnología',
            'location': 'San Francisco, CA'
        }
    )
    
    investor1, created_inv1 = InvestorProfile.objects.get_or_create(
        user=user1,
        defaults={
            'fund_name': 'TechAngel Ventures',
            'investor_type': 'angel',
            'fund_size': 5000000,  # $5M
            'min_investment': 50000,  # $50k
            'max_investment': 250000,  # $250k
            'typical_investment': 100000,  # $100k
            'thesis': 'Invierto en startups B2B SaaS en etapa temprana con tracción demostrable',
            'sweet_spot': 'Series A, startups con ARR >$500k',
            'geographic_focus': 'north_america',
            'portfolio_companies_count': 25,
            'investments_per_year': 5,
            'notable_investments': 'Stripe (Angel round), Notion (Seed)',
            'investment_stages': ['seed', 'series_a'],
            'is_active': True,
            'is_accepting_pitches': True,
            'featured': True
        }
    )
    if created_inv1:
        print(f"✓ Inversor creado: {investor1.fund_name}")
    
    # Inversor 2: VC Fund
    user2, created2 = User.objects.get_or_create(
        username='investor2',
        defaults={
            'email': 'investor2@example.com',
            'first_name': 'Carlos',
            'last_name': 'Rodríguez'
        }
    )
    if created2:
        user2.set_password('password123')
        user2.save()
        print(f"✓ Usuario creado: {user2.username}")
    
    profile2, created_p2 = UserProfile.objects.get_or_create(
        user=user2,
        defaults={
            'user_type': 'investor',
            'bio': 'Partner en fondo de venture capital enfocado en Latinoamérica',
            'location': 'México City, MX'
        }
    )
    
    investor2, created_inv2 = InvestorProfile.objects.get_or_create(
        user=user2,
        defaults={
            'fund_name': 'LATAM Ventures',
            'investor_type': 'vc_fund',
            'fund_size': 50000000,  # $50M
            'min_investment': 500000,  # $500k
            'max_investment': 5000000,  # $5M
            'typical_investment': 2000000,  # $2M
            'thesis': 'Invertimos en startups tecnológicas de América Latina con potencial de expansión global',
            'sweet_spot': 'Series A y B, startups con revenue >$1M',
            'geographic_focus': 'latin_america',
            'portfolio_companies_count': 15,
            'investments_per_year': 8,
            'notable_investments': 'Rappi (Series A), Nubank (Series B)',
            'investment_stages': ['series_a', 'series_b'],
            'is_active': True,
            'is_accepting_pitches': True,
            'featured': True
        }
    )
    if created_inv2:
        print(f"✓ Inversor creado: {investor2.fund_name}")
    
    # Inversor 3: Corporate VC
    user3, created3 = User.objects.get_or_create(
        username='investor3',
        defaults={
            'email': 'investor3@example.com',
            'first_name': 'Ana',
            'last_name': 'Martínez'
        }
    )
    if created3:
        user3.set_password('password123')
        user3.save()
        print(f"✓ Usuario creado: {user3.username}")
    
    profile3, created_p3 = UserProfile.objects.get_or_create(
        user=user3,
        defaults={
            'user_type': 'investor',
            'bio': 'Corporate VC especializado en HealthTech y BioTech',
            'location': 'Boston, MA'
        }
    )
    
    investor3, created_inv3 = InvestorProfile.objects.get_or_create(
        user=user3,
        defaults={
            'fund_name': 'HealthCorp Ventures',
            'investor_type': 'corporate_vc',
            'fund_size': 100000000,  # $100M
            'min_investment': 1000000,  # $1M
            'max_investment': 10000000,  # $10M
            'typical_investment': 3000000,  # $3M
            'thesis': 'Inversiones estratégicas en tecnología médica y biotecnología',
            'sweet_spot': 'Series B+, empresas con productos validados clínicamente',
            'geographic_focus': 'global',
            'portfolio_companies_count': 12,
            'investments_per_year': 4,
            'notable_investments': 'Oscar Health (Series C), 23andMe (Series D)',
            'investment_stages': ['series_b', 'series_c'],
            'is_active': True,
            'is_accepting_pitches': True,
            'featured': False
        }
    )
    if created_inv3:
        print(f"✓ Inversor creado: {investor3.fund_name}")
    
    # Inversor 4: Family Office
    user4, created4 = User.objects.get_or_create(
        username='investor4',
        defaults={
            'email': 'investor4@example.com',
            'first_name': 'Jorge',
            'last_name': 'Silva'
        }
    )
    if created4:
        user4.set_password('password123')
        user4.save()
        print(f"✓ Usuario creado: {user4.username}")
    
    profile4, created_p4 = UserProfile.objects.get_or_create(
        user=user4,
        defaults={
            'user_type': 'investor',
            'bio': 'Family office con enfoque en CleanTech y sostenibilidad',
            'location': 'Barcelona, España'
        }
    )
    
    investor4, created_inv4 = InvestorProfile.objects.get_or_create(
        user=user4,
        defaults={
            'fund_name': 'Green Future Family Office',
            'investor_type': 'family_office',
            'fund_size': 25000000,  # $25M
            'min_investment': 200000,  # $200k
            'max_investment': 2000000,  # $2M
            'typical_investment': 750000,  # $750k
            'thesis': 'Inversión en tecnologías limpias y empresas sostenibles',
            'sweet_spot': 'Seed a Series A, startups con impacto ambiental positivo',
            'geographic_focus': 'europe',
            'portfolio_companies_count': 18,
            'investments_per_year': 6,
            'notable_investments': 'Too Good To Go (Seed), Fairphone (Series A)',
            'investment_stages': ['seed', 'series_a'],
            'is_active': True,
            'is_accepting_pitches': True,
            'featured': True
        }
    )
    if created_inv4:
        print(f"✓ Inversor creado: {investor4.fund_name}")
    
    print("\n" + "="*50)
    print("✅ Inversores de ejemplo creados exitosamente!")
    print("="*50)
    print("\nCredenciales de acceso:")
    print("- investor1 / password123")
    print("- investor2 / password123")
    print("- investor3 / password123")
    print("- investor4 / password123")
    print("\nAhora puedes verlos en: http://127.0.0.1:8000/investors/")

if __name__ == '__main__':
    create_sample_investors()
