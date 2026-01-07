#!/usr/bin/env python
"""
Script para poblar la base de datos con startups de ejemplo
con datos realistas para probar el sistema de scoring dinámico
"""

import os
import sys
import django
from decimal import Decimal
from datetime import date, datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mydevsite.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile, Startup, Industry

def create_sample_startups():
    """Crea startups de ejemplo con datos realistas"""
    
    # Crear industrias si no existen
    industries_data = [
        'FinTech', 'HealthTech', 'EdTech', 'E-commerce', 'AI/ML', 
        'SaaS', 'CleanTech', 'FoodTech', 'PropTech', 'Gaming'
    ]
    
    industries = {}
    for industry_name in industries_data:
        industry, created = Industry.objects.get_or_create(name=industry_name)
        industries[industry_name] = industry
        if created:
            print(f"✅ Creada industria: {industry_name}")
    
    # Crear founder de ejemplo si no existe
    founder_user, created = User.objects.get_or_create(
        username='demo_founder',
        defaults={
            'email': 'founder@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
    )
    
    if created:
        founder_user.set_password('demo123')
        founder_user.save()
    
    founder_profile, created = UserProfile.objects.get_or_create(
        user=founder_user,
        defaults={
            'user_type': 'founder',
            'bio': 'Experienced entrepreneur and startup founder'
        }
    )
    
    if created:
        print(f"✅ Creado founder: {founder_user.username}")
    
    # Datos de startups ejemplo con diferentes perfiles de scoring
    sample_startups = [
        {
            'company_name': 'PayFlow Solutions',
            'tagline': 'Simplifying B2B payments for small businesses',
            'industry': 'FinTech',
            'stage': 'growth',
            'monthly_revenue': Decimal('25000'),
            'annual_revenue': Decimal('300000'),
            'total_funding_raised': Decimal('2500000'),
            'employees_count': 15,
            'monthly_users': 5000,
            'founded_date': date(2022, 3, 15),
            'is_fundraising': True,
            'seeking_amount': Decimal('5000000'),
            'description': 'PayFlow Solutions offers automated payment processing and invoice management for small and medium businesses.',
        },
        {
            'company_name': 'HealthTrack AI',
            'tagline': 'AI-powered health monitoring for better outcomes',
            'industry': 'HealthTech', 
            'stage': 'early_traction',
            'monthly_revenue': Decimal('8000'),
            'annual_revenue': Decimal('96000'),
            'total_funding_raised': Decimal('500000'),
            'employees_count': 8,
            'monthly_users': 2500,
            'founded_date': date(2023, 6, 10),
            'is_fundraising': True,
            'seeking_amount': Decimal('2000000'),
            'description': 'Using AI and wearable technology to provide personalized health insights and early disease detection.',
        },
        {
            'company_name': 'EduConnect Platform',
            'tagline': 'Connecting students with personalized learning experiences',
            'industry': 'EdTech',
            'stage': 'mvp',
            'monthly_revenue': Decimal('3000'),
            'annual_revenue': Decimal('36000'),
            'total_funding_raised': Decimal('250000'),
            'employees_count': 5,
            'monthly_users': 1200,
            'founded_date': date(2024, 1, 20),
            'is_fundraising': False,
            'description': 'An educational platform that uses adaptive learning algorithms to personalize education for K-12 students.',
        },
        {
            'company_name': 'GreenShop Marketplace',
            'tagline': 'Sustainable products for conscious consumers',
            'industry': 'E-commerce',
            'stage': 'scale',
            'monthly_revenue': Decimal('150000'),
            'annual_revenue': Decimal('1800000'),
            'total_funding_raised': Decimal('8000000'),
            'employees_count': 45,
            'monthly_users': 25000,
            'founded_date': date(2020, 8, 5),
            'is_fundraising': False,
            'description': 'Curated marketplace for eco-friendly and sustainable products with carbon-neutral shipping.',
        },
        {
            'company_name': 'DataViz Pro',
            'tagline': 'Enterprise data visualization made simple',
            'industry': 'SaaS',
            'stage': 'growth',
            'monthly_revenue': Decimal('45000'),
            'annual_revenue': Decimal('540000'),
            'total_funding_raised': Decimal('3200000'),
            'employees_count': 22,
            'monthly_users': 8500,
            'founded_date': date(2021, 11, 12),
            'is_fundraising': True,
            'seeking_amount': Decimal('10000000'),
            'description': 'Advanced data visualization and business intelligence platform for enterprise clients.',
        },
        {
            'company_name': 'CleanWave Energy',
            'tagline': 'Next-generation solar energy solutions',
            'industry': 'CleanTech',
            'stage': 'prototype',
            'monthly_revenue': Decimal('500'),
            'annual_revenue': Decimal('6000'),
            'total_funding_raised': Decimal('1200000'),
            'employees_count': 12,
            'monthly_users': 50,
            'founded_date': date(2023, 9, 30),
            'is_fundraising': True,
            'seeking_amount': Decimal('5000000'),
            'description': 'Developing high-efficiency solar panels with integrated energy storage technology.',
        },
        {
            'company_name': 'FoodieBot',
            'tagline': 'AI-powered restaurant automation',
            'industry': 'FoodTech',
            'stage': 'idea',
            'monthly_revenue': Decimal('0'),
            'annual_revenue': Decimal('0'),
            'total_funding_raised': Decimal('50000'),
            'employees_count': 3,
            'monthly_users': 0,
            'founded_date': date(2024, 11, 1),
            'is_fundraising': True,
            'seeking_amount': Decimal('500000'),
            'description': 'Robotic solutions for restaurant kitchen automation and food preparation.',
        }
    ]
    
    created_count = 0
    
    for startup_data in sample_startups:
        # Verificar si ya existe
        existing = Startup.objects.filter(company_name=startup_data['company_name']).first()
        if existing:
            print(f"⚠️  Startup ya existe: {startup_data['company_name']}")
            continue
        
        # Crear la startup
        industry_name = startup_data.pop('industry')
        startup_data['industry'] = industries[industry_name]
        startup_data['founder'] = founder_profile
        
        startup = Startup.objects.create(**startup_data)
        created_count += 1
        
        # Calcular y mostrar scores
        growth_score = startup.calculate_growth_score()
        heat_score = startup.calculate_heat_score()
        cb_rank = startup.calculate_cb_rank()
        percentile = startup.get_ranking_percentile()
        performance = startup.get_performance_grade()
        
        print(f"""✅ Creada startup: {startup.company_name}
   📊 Growth Score: {growth_score}
   🔥 Heat Score: {heat_score}  
   🏆 CB Rank: #{cb_rank}
   📈 Percentil: {percentile}%
   🎓 Grade: {performance['grade']}
   💰 Revenue: {startup.format_revenue_amount()}
   💵 Funding: {startup.format_funding_amount()}
   👥 Employees: {startup.employees_count}
   """)
    
    print(f"\n🎉 Proceso completado! Se crearon {created_count} startups nuevas.")
    
    # Mostrar ranking general
    print("\n📊 RANKING GENERAL DE STARTUPS:")
    print("="*50)
    
    all_startups = Startup.objects.all()
    startup_scores = []
    
    for startup in all_startups:
        startup_scores.append({
            'name': startup.company_name,
            'growth_score': startup.calculate_growth_score(),
            'cb_rank': startup.calculate_cb_rank(),
            'percentile': startup.get_ranking_percentile(),
            'grade': startup.get_performance_grade()['grade']
        })
    
    # Ordenar por Growth Score
    startup_scores.sort(key=lambda x: x['growth_score'], reverse=True)
    
    for i, startup in enumerate(startup_scores, 1):
        print(f"{i:2d}. {startup['name']:<25} | Score: {startup['growth_score']:2d} | Rank: #{startup['cb_rank']:>6} | Grade: {startup['grade']}")

if __name__ == '__main__':
    print("🚀 Iniciando creación de startups de ejemplo...")
    create_sample_startups()
