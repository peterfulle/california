from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

# MODELOS CORE PARA LA PLATAFORMA STARTUP-INVESTOR

class Industry(models.Model):
    """Sectores/Verticales de industria"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Industries"
        ordering = ['name']

# MODELO DE PERFIL DE USUARIO PRINCIPAL
class UserProfile(models.Model):
    """Perfil extendido de usuario con roles en el ecosistema"""
    USER_TYPES = [
        ('founder', 'Founder'),
        ('investor', 'Investor'),
        ('advisor', 'Advisor'),
        ('community', 'Community Member'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    
    # Información básica
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    # Configuración
    is_verified = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    show_contact_info = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user_type})"
    
    class Meta:
        ordering = ['-created_at']

# MODELO DE EVENTOS
class Event(models.Model):
    """Modelo para eventos estilo Partiful"""
    EVENT_TYPES = [
        ('networking', 'Networking'),
        ('workshop', 'Workshop'),
        ('conference', 'Conference'),
        ('hackathon', 'Hackathon'),
    ]
    
    THEME_CHOICES = [
        ('modern', 'Modern'),
        ('classic', 'Classic'),
        ('tech', 'Tech'),
        ('corporate', 'Corporate'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
    ]

    # Campos básicos
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    
    # Fecha y hora
    date = models.DateField()
    time = models.TimeField()
    
    # Ubicación
    location = models.CharField(max_length=200)
    
    # Estilo y tema
    theme = models.CharField(max_length=20, choices=THEME_CHOICES)
    
    # Configuración
    capacity = models.IntegerField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Registro y búsqueda
    search_vector = models.TextField(null=True, blank=True)  # Para búsqueda full-text si se implementa
    
    # Relaciones
    attendees = models.ManyToManyField(User, through='EventAttendance', related_name='events_attending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Campos básicos
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    
    # Fecha y hora
    date = models.DateField()
    time = models.TimeField()
    
    # Ubicación
    location = models.CharField(max_length=200)
    
    # Estilo y tema
    theme = models.CharField(max_length=20, choices=THEME_CHOICES)
    
    # Configuración
    capacity = models.IntegerField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Registro y búsqueda
    search_vector = models.TextField(null=True, blank=True)  # Para búsqueda full-text si se implementa
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-time']
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('event_detail', kwargs={'event_id': self.id})
    
    def is_past_event(self):
        from django.utils import timezone
        return timezone.now().date() > self.date

# MODELO DE STARTUP COMPLETO
class Startup(models.Model):
    """Modelo principal para startups en la plataforma"""
    COMPANY_STAGES = [
        ('idea', 'Idea Stage'),
        ('prototype', 'Prototype'),
        ('mvp', 'MVP'),
        ('early_traction', 'Early Traction'),
        ('growth', 'Growth'),
        ('scale', 'Scale'),
        ('exit', 'Exit'),
    ]
    
    REVENUE_STAGES = [
        ('no_revenue', 'No Revenue'),
        ('pre_revenue', 'Pre-Revenue'),
        ('early_revenue', 'Early Revenue ($1K-$10K MRR)'),
        ('growing_revenue', 'Growing Revenue ($10K-$100K MRR)'),
        ('scale_revenue', 'Scale Revenue ($100K+ MRR)'),
    ]
    
    # Relación con fundador
    founder = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'user_type': 'founder'})
    
    # Información básica
    company_name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=150, help_text="Descripción en una línea")
    description = models.TextField(help_text="Descripción detallada de la startup")
    logo = models.ImageField(upload_to='startup_logos/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='startup_covers/', blank=True, null=True)
    
    # Estado de la compañía
    stage = models.CharField(max_length=20, choices=COMPANY_STAGES)
    revenue_stage = models.CharField(max_length=20, choices=REVENUE_STAGES, null=True, blank=True)
    founded_date = models.DateField(null=True, blank=True)
    employees_count = models.IntegerField(null=True, blank=True)
    
    # Tesis de inversión
    problem_statement = models.TextField(help_text="¿Qué problema resuelven?", blank=True)
    solution_description = models.TextField(help_text="¿Cómo lo resuelven?", blank=True)
    market_size = models.TextField(help_text="Tamaño del mercado", blank=True)
    business_model = models.TextField(help_text="Modelo de negocio", blank=True)
    competitive_advantage = models.TextField(help_text="Ventaja competitiva", blank=True)
    
    # Industria
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True)
    sub_industry = models.CharField(max_length=100, blank=True)
    
    # Métricas clave
    monthly_revenue = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    annual_revenue = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    monthly_users = models.IntegerField(null=True, blank=True)
    burn_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    runway_months = models.IntegerField(null=True, blank=True)
    customer_acquisition_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    lifetime_value = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    churn_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Funding
    total_funding_raised = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    seeking_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    valuation = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Enlaces
    website = models.URLField(blank=True)
    pitch_deck_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    
    # Configuración
    is_public = models.BooleanField(default=True)
    is_fundraising = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.company_name
    
    def calculate_growth_score(self):
        """
        Calcula el Growth Score basado en múltiples factores
        Score: 0-100 donde 100 es el mejor
        """
        score = 0
        
        # Factor 1: Etapa de la empresa (0-25 puntos)
        stage_scores = {
            'idea': 5,
            'prototype': 10,
            'mvp': 15,
            'early_traction': 20,
            'growth': 25,
            'scale': 22,  # Slightly lower as growth might be slowing
            'exit': 18    # Company might be winding down
        }
        score += stage_scores.get(self.stage, 0)
        
        # Factor 2: Ingresos mensuales (0-25 puntos)
        if self.monthly_revenue:
            if self.monthly_revenue >= 100000:  # $100K+ MRR
                score += 25
            elif self.monthly_revenue >= 50000:  # $50K+ MRR
                score += 22
            elif self.monthly_revenue >= 10000:  # $10K+ MRR
                score += 18
            elif self.monthly_revenue >= 1000:   # $1K+ MRR
                score += 12
            elif self.monthly_revenue > 0:       # Any revenue
                score += 8
        
        # Factor 3: Financiación total (0-20 puntos)
        if self.total_funding_raised:
            if self.total_funding_raised >= 10000000:  # $10M+
                score += 20
            elif self.total_funding_raised >= 5000000:  # $5M+
                score += 18
            elif self.total_funding_raised >= 1000000:  # $1M+
                score += 15
            elif self.total_funding_raised >= 100000:   # $100K+
                score += 10
            elif self.total_funding_raised > 0:         # Any funding
                score += 5
        
        # Factor 4: Crecimiento del equipo (0-15 puntos)
        if self.employees_count:
            if self.employees_count >= 100:
                score += 15
            elif self.employees_count >= 50:
                score += 13
            elif self.employees_count >= 20:
                score += 11
            elif self.employees_count >= 10:
                score += 8
            elif self.employees_count >= 5:
                score += 5
            else:
                score += 2
        
        # Factor 5: Completitud del perfil (0-15 puntos)
        profile_completeness = 0
        if self.description: profile_completeness += 2
        if self.website: profile_completeness += 2
        if self.logo: profile_completeness += 2
        if self.industry: profile_completeness += 2
        if self.business_model: profile_completeness += 2
        if self.problem_statement: profile_completeness += 2
        if self.solution_description: profile_completeness += 2
        if self.founded_date: profile_completeness += 1
        
        score += profile_completeness
        
        return min(score, 100)  # Cap at 100
    
    def calculate_heat_score(self):
        """
        Calcula el Heat Score basado en actividad reciente y tendencias
        Score: 0-100 donde 100 es el más "hot"
        """
        from django.utils import timezone
        from datetime import datetime, timedelta
        
        score = 0
        now = timezone.now()
        
        # Factor 1: Actividad reciente del perfil (0-30 puntos)
        if self.updated_at:
            days_since_update = (now - self.updated_at).days
            if days_since_update <= 7:
                score += 30
            elif days_since_update <= 30:
                score += 20
            elif days_since_update <= 90:
                score += 10
            else:
                score += 5
        
        # Factor 2: Estado de fundraising (0-25 puntos)
        if self.is_fundraising:
            score += 25
        elif self.seeking_amount:
            score += 15
        
        # Factor 3: Crecimiento reciente estimado (0-25 puntos)
        # Si tiene métricas de ingresos, asumimos crecimiento
        if self.monthly_revenue:
            if self.monthly_revenue >= 10000:
                score += 25
            elif self.monthly_revenue >= 1000:
                score += 20
            elif self.monthly_revenue > 0:
                score += 15
        
        # Factor 4: Industria trending (0-20 puntos)
        trending_industries = ['AI', 'Blockchain', 'FinTech', 'HealthTech', 'EdTech', 'CleanTech']
        if self.industry and any(trend in self.industry.name for trend in trending_industries):
            score += 20
        elif self.industry:
            score += 10
        
        return min(score, 100)  # Cap at 100
    
    def calculate_cb_rank(self):
        """
        Calcula el CB Rank (ranking global)
        Rank más bajo = mejor posición
        """
        # Calcular score combinado
        growth_score = self.calculate_growth_score()
        heat_score = self.calculate_heat_score()
        combined_score = (growth_score * 0.6) + (heat_score * 0.4)
        
        # Contar startups mejor rankeadas
        from django.db.models import Q
        better_startups = Startup.objects.filter(
            Q(total_funding_raised__gt=self.total_funding_raised) |
            Q(monthly_revenue__gt=self.monthly_revenue or 0) |
            Q(employees_count__gt=self.employees_count or 0)
        ).distinct().count()
        
        # Base rank + factor aleatorio para variación
        base_rank = better_startups + 1
        
        # Ajustar según score combinado
        if combined_score >= 80:
            rank_adjustment = -500
        elif combined_score >= 60:
            rank_adjustment = -200
        elif combined_score >= 40:
            rank_adjustment = 0
        else:
            rank_adjustment = 500
        
        final_rank = max(1, base_rank + rank_adjustment)
        return final_rank
    
    def get_ranking_percentile(self):
        """
        Calcula en qué percentil está esta startup
        """
        total_startups = Startup.objects.count()
        rank = self.calculate_cb_rank()
        
        if total_startups == 0:
            return 100
        
        percentile = max(1, 100 - ((rank / total_startups) * 100))
        return round(percentile, 1)
    
    def get_score_summary(self):
        """
        Retorna un resumen de todos los scores para fácil acceso
        """
        return {
            'growth_score': self.calculate_growth_score(),
            'heat_score': self.calculate_heat_score(),
            'cb_rank': self.calculate_cb_rank(),
            'ranking_percentile': self.get_ranking_percentile()
        }
    
    def get_performance_grade(self):
        """
        Retorna una calificación basada en el Growth Score
        """
        score = self.calculate_growth_score()
        if score >= 85:
            return {'grade': 'A+', 'color': 'green'}
        elif score >= 75:
            return {'grade': 'A', 'color': 'green'}
        elif score >= 65:
            return {'grade': 'B+', 'color': 'blue'}
        elif score >= 55:
            return {'grade': 'B', 'color': 'blue'}
        elif score >= 45:
            return {'grade': 'C+', 'color': 'yellow'}
        elif score >= 35:
            return {'grade': 'C', 'color': 'yellow'}
        else:
            return {'grade': 'D', 'color': 'red'}
    
    def get_market_position(self):
        """
        Retorna la posición en el mercado basada en el percentil
        """
        percentile = self.get_ranking_percentile()
        if percentile >= 90:
            return 'Top 10%'
        elif percentile >= 75:
            return 'Top 25%'
        elif percentile >= 50:
            return 'Top 50%'
        elif percentile >= 25:
            return 'Top 75%'
        else:
            return 'Developing'
    
    def format_funding_amount(self):
        """
        Formatea el amount de funding de forma legible
        """
        if not self.total_funding_raised:
            return 'No disclosed'
        
        amount = float(self.total_funding_raised)
        if amount >= 1000000:
            return f'${amount/1000000:.1f}M'
        elif amount >= 1000:
            return f'${amount/1000:.0f}K'
        else:
            return f'${amount:.0f}'
    
    def format_revenue_amount(self):
        """
        Formatea el revenue mensual de forma legible
        """
        if not self.monthly_revenue:
            return 'Not disclosed'
        
        amount = float(self.monthly_revenue)
        if amount >= 1000000:
            return f'${amount/1000000:.1f}M/mo'
        elif amount >= 1000:
            return f'${amount/1000:.0f}K/mo'
        else:
            return f'${amount:.0f}/mo'
    
    def is_investor_approved_for_access(self, user):
        """
        Verifica si un usuario tiene acceso a la información privada de esta startup
        """
        if not user.is_authenticated:
            return False
        
        # El fundador siempre tiene acceso
        if self.founder.user == user:
            return True
        
        # Verificar si es un inversionista con acceso aprobado
        if hasattr(user, 'profile') and user.profile.user_type == 'investor':
            try:
                # Importación local para evitar circular import
                access = PrivateDataAccess.objects.get(
                    startup=self,
                    investor=user.profile,
                    is_active=True
                )
                return True
            except PrivateDataAccess.DoesNotExist:
                return False
        
        return False
    
    class Meta:
        ordering = ['-created_at']

# Modelos nuevos - comentados temporalmente para migraciones
"""
class UserProfile(models.Model):
    # ...existing code...

class Startup(models.Model):
    # ...existing code...

class FoundingTeam(models.Model):
    # ...existing code...

class AdvisorNetwork(models.Model):
    # ...existing code...

class FundingRound(models.Model):
    # ...existing code...

class EventRegistration(models.Model):
    # ...existing code...
"""

class Event(models.Model):
    """Sistema de eventos y comunidad mejorado"""
    EVENT_TYPES = [
        ('networking', 'Networking Mixer'),
        ('pitch_night', 'Pitch Night'),
        ('panel', 'Panel Discussion'),
        ('workshop', 'Workshop'),
        ('breakfast', 'Founders Breakfast'),
        ('demo_day', 'Demo Day'),
        ('investor_day', 'Investor Day'),
        ('conference', 'Conference'),
        ('webinar', 'Webinar'),
    ]
    
    THEME_CHOICES = [
        (1, 'Gradiente Moderno'),
        (2, 'Noche Estrellada'),
        (3, 'Aurora Boreal'),
        (4, 'Atardecer'),
        (5, 'Tech Minimal'),
        (6, 'Neón'),
    ]
    
    EVENT_STATUS = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    # Información básica
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    status = models.CharField(max_length=20, choices=EVENT_STATUS, default='draft')
    
    # Fecha y ubicación
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    location = models.CharField(max_length=300, blank=True)
    is_virtual = models.BooleanField(default=False)
    meeting_url = models.URLField(blank=True)
    
    # Registro y asistencia
    max_attendees = models.IntegerField(default=50)
    registration_required = models.BooleanField(default=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    is_free = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Organización
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # co_organizers = models.ManyToManyField(UserProfile, related_name='co_organized_events', blank=True)
    target_audience = models.JSONField(default=list, help_text="founders, investors, advisors, community")
    
    # Contenido
    agenda = models.TextField(blank=True)
    # speakers = models.ManyToManyField(UserProfile, related_name='speaking_events', blank=True)
    sponsors = models.TextField(blank=True)
    
    # Media
    featured_image = models.ImageField(upload_to='events/', blank=True, null=True)
    gallery_images = models.JSONField(default=list, blank=True)
    
    # Configuración
    featured = models.BooleanField(default=False)
    is_recurring = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-start_datetime']

class EventRegistration(models.Model):
    """Registro de usuarios a eventos"""
    REGISTRATION_STATUS = [
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('no_show', 'No Show'),
        ('cancelled', 'Cancelled'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=REGISTRATION_STATUS, default='registered')
    registration_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.event.title}"
    
    class Meta:
        unique_together = ['event', 'user']

# MODELO PARA INVERSORES ACTUALIZADO
class InvestorProfile(models.Model):
    """Perfiles de inversores con categorización detallada"""
    INVESTOR_TYPES = [
        ('angel', 'Angel Investor'),
        ('vc_fund', 'VC Fund'),
        ('corporate_vc', 'Corporate VC'),
        ('family_office', 'Family Office'),
        ('accelerator', 'Accelerator'),
        ('government', 'Government Fund'),
        ('strategic', 'Strategic Investor'),
    ]
    
    GEOGRAPHIC_FOCUS = [
        ('global', 'Global'),
        ('north_america', 'North America'),
        ('latin_america', 'Latin America'),
        ('europe', 'Europe'),
        ('asia', 'Asia'),
        ('africa', 'Africa'),
        ('local', 'Local Market Only'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Información básica
    fund_name = models.CharField(max_length=200)
    investor_type = models.CharField(max_length=20, choices=INVESTOR_TYPES)
    
    # Foco de inversión - simplificado temporalmente
    # focus_industries = models.ManyToManyField(Industry, blank=True)
    investment_stages = models.JSONField(default=list, help_text="Etapas de inversión preferidas")
    geographic_focus = models.CharField(max_length=20, choices=GEOGRAPHIC_FOCUS, null=True, blank=True)
    
    # Ticket promedio
    min_investment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_investment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    typical_investment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Información del fondo
    fund_size = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    portfolio_companies_count = models.IntegerField(null=True, blank=True)
    investments_per_year = models.IntegerField(null=True, blank=True)
    
    # Información adicional
    thesis = models.TextField(help_text="Tesis de inversión", blank=True)
    sweet_spot = models.TextField(help_text="Sweet spot de inversiones", blank=True)
    notable_investments = models.TextField(blank=True)
    
    # Configuración
    is_active = models.BooleanField(default=True)
    is_accepting_pitches = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.fund_name} ({self.investor_type})"
    
    class Meta:
        ordering = ['-created_at']

# MODELO DE CONTACTO (mantener para formularios)
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']

# Mantener modelo legacy para compatibilidad
class FounderProfile(models.Model):
    """Modelo legacy - usar Startup en su lugar"""
    INDUSTRY_CHOICES = [
        ('fintech', 'Fintech'),
        ('healthtech', 'HealthTech'),
        ('edtech', 'EdTech'),
        ('proptech', 'PropTech'),
        ('deeptech', 'DeepTech'),
        ('saas', 'SaaS'),
        ('ecommerce', 'E-commerce'),
        ('ai_ml', 'AI/ML'),
        ('biotech', 'Biotech'),
        ('cleantech', 'CleanTech'),
    ]
    
    FUNDING_STAGE = [
        ('pre_seed', 'Pre-Seed'),
        ('seed', 'Seed'),
        ('series_a', 'Series A'),
        ('series_b', 'Series B+'),
        ('revenue', 'Revenue Stage'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    funding_stage = models.CharField(max_length=50, choices=FUNDING_STAGE)
    country_origin = models.CharField(max_length=100)
    linkedin_url = models.URLField(blank=True)
    company_website = models.URLField(blank=True)
    pitch_deck_url = models.URLField(blank=True)
    brief_description = models.TextField(max_length=500)
    logo = models.ImageField(upload_to='founder_logos/', blank=True, null=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.company_name}"
    
    class Meta:
        verbose_name = "Founder Profile (Legacy)"

# Comentando temporalmente los modelos que requieren UserProfile y Startup
"""
class FoundingTeam(models.Model):
    # ...existing code...

class AdvisorNetwork(models.Model):
    # ...existing code...

class FundingRound(models.Model):
    # ...existing code...
"""

# ===========================================
# SISTEMA DE INFORMACIÓN PRIVADA PARA STARTUPS
# ===========================================

class InvestorAccessRequest(models.Model):
    """Solicitudes de acceso de inversionistas a información privada"""
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('revoked', 'Access Revoked'),
    ]
    
    # Relaciones principales
    investor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, 
                               limit_choices_to={'user_type': 'investor'},
                               related_name='access_requests')
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, 
                              related_name='access_requests')
    
    # Estado de la solicitud
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(help_text="Mensaje del inversionista explicando su interés", max_length=1000)
    
    # Tracking de decisiones
    reviewed_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='reviewed_requests')
    review_message = models.TextField(blank=True, help_text="Respuesta del fundador")
    
    # Fechas importantes
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True, 
                                    help_text="Fecha de expiración del acceso")
    
    class Meta:
        unique_together = ['investor', 'startup']
        ordering = ['-requested_at']
    
    def __str__(self):
        return f"{self.investor.user.get_full_name()} -> {self.startup.company_name} ({self.status})"
    
    @property
    def is_active(self):
        """Verifica si el acceso está activo y no ha expirado"""
        from django.utils import timezone
        if self.status != 'approved':
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True


class StartupFinancials(models.Model):
    """Información financiera privada de la startup"""
    startup = models.OneToOneField(Startup, on_delete=models.CASCADE, related_name='private_financials')
    
    # Métricas detalladas de revenue
    arr_current = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                    help_text="Annual Recurring Revenue actual")
    mrr_growth_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                        help_text="Tasa de crecimiento MRR (porcentaje)")
    revenue_forecast_12m = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    revenue_forecast_24m = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Métricas de unit economics
    cac_payback_period = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True,
                                           help_text="Meses para recuperar CAC")
    gross_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                     help_text="Margen bruto (porcentaje)")
    net_revenue_retention = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Información de funding detallada
    cash_position = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                      help_text="Efectivo actual en banco")
    burn_rate_detailed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                           help_text="Burn rate mensual detallado")
    runway_calculation = models.TextField(blank=True, help_text="Cálculo detallado del runway")
    
    # Proyecciones y use of funds
    funding_use_breakdown = models.JSONField(default=dict, blank=True,
                                           help_text="Desglose de uso de fondos por categoría")
    financial_projections = models.JSONField(default=dict, blank=True,
                                           help_text="Proyecciones financieras detalladas")
    
    # Información de rondas
    current_round_details = models.TextField(blank=True)
    previous_investors = models.TextField(blank=True, help_text="Lista de inversionistas previos")
    terms_and_conditions = models.TextField(blank=True)
    
    # Documentos financieros (URLs o referencias)
    financial_statements_url = models.URLField(blank=True)
    cap_table_url = models.URLField(blank=True)
    business_plan_url = models.URLField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Financials - {self.startup.company_name}"


class StartupPeople(models.Model):
    """Información privada del equipo y personas"""
    startup = models.OneToOneField(Startup, on_delete=models.CASCADE, related_name='private_people')
    
    # Métricas del equipo
    total_employees = models.IntegerField(default=0, help_text="Total de empleados")
    founders_count = models.IntegerField(default=1, help_text="Número de fundadores")
    tech_team_size = models.IntegerField(default=0, help_text="Tamaño del equipo técnico")
    leadership_team_size = models.IntegerField(default=0, help_text="Tamaño del equipo de liderazgo")
    
    # Información del equipo fundador
    founders_detailed_bios = models.JSONField(default=dict, blank=True,
                                            help_text="Biografías detalladas de fundadores")
    equity_distribution = models.JSONField(default=dict, blank=True,
                                         help_text="Distribución de equity del equipo")
    
    # Cultura organizacional
    company_mission = models.TextField(blank=True, help_text="Misión de la empresa")
    company_vision = models.TextField(blank=True, help_text="Visión de la empresa")
    company_values = models.TextField(blank=True)
    work_mode = models.CharField(max_length=20, default='hybrid', 
                                choices=[('remote', 'Remoto'), ('hybrid', 'Híbrido'), ('onsite', 'Presencial')])
    main_location = models.CharField(max_length=100, blank=True, help_text="Ubicación principal")
    remote_work_policy = models.TextField(blank=True)
    compensation_philosophy = models.TextField(blank=True)
    diversity_initiatives = models.TextField(blank=True)
    
    # Plan de crecimiento del equipo
    hiring_plan_12m = models.JSONField(default=dict, blank=True,
                                     help_text="Plan de contrataciones a 12 meses")
    hiring_budget_annual = models.CharField(max_length=50, blank=True, help_text="Presupuesto anual de contratación")
    hiring_priority_1 = models.CharField(max_length=100, blank=True, help_text="Prioridad #1 de contratación")
    recruitment_strategy = models.TextField(blank=True, help_text="Estrategia de reclutamiento")
    key_roles_needed = models.TextField(blank=True)
    org_chart_url = models.URLField(blank=True)
    
    # Advisors y board
    advisory_board = models.JSONField(default=list, blank=True,
                                    help_text="Lista de advisors con detalles")
    board_composition = models.JSONField(default=dict, blank=True)
    
    # Cultura y beneficios
    employee_benefits = models.JSONField(default=dict, blank=True)
    company_culture_deck_url = models.URLField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"People - {self.startup.company_name}"


class StartupNews(models.Model):
    """Noticias y updates privados de la startup"""
    startup = models.OneToOneField(Startup, on_delete=models.CASCADE, related_name='private_news')
    
    # Updates internos
    monthly_updates = models.JSONField(default=list, blank=True,
                                     help_text="Updates mensuales para inversionistas")
    milestone_achievements = models.JSONField(default=list, blank=True)
    upcoming_milestones = models.JSONField(default=list, blank=True)
    
    # Información de mercado y competencia
    competitive_analysis = models.TextField(blank=True)
    market_developments = models.TextField(blank=True)
    partnership_opportunities = models.TextField(blank=True)
    
    # Media y PR
    media_coverage = models.JSONField(default=list, blank=True,
                                    help_text="Cobertura de medios")
    press_releases = models.JSONField(default=list, blank=True)
    upcoming_events = models.JSONField(default=list, blank=True)
    
    # Comunicaciones con inversionistas
    investor_letter_template = models.TextField(blank=True)
    quarterly_reports = models.JSONField(default=list, blank=True)
    
    # Social proof y testimonios
    customer_testimonials = models.JSONField(default=list, blank=True)
    case_studies = models.JSONField(default=list, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"News - {self.startup.company_name}"


class StartupTechnology(models.Model):
    """Información técnica y de producto privada"""
    startup = models.OneToOneField(Startup, on_delete=models.CASCADE, related_name='private_technology')
    
    # Stack técnico detallado
    technology_stack = models.JSONField(default=dict, blank=True,
                                      help_text="Stack completo de tecnologías")
    architecture_overview = models.TextField(blank=True)
    infrastructure_details = models.TextField(blank=True)
    
    # Producto y roadmap
    product_roadmap = models.JSONField(default=dict, blank=True,
                                     help_text="Roadmap detallado del producto")
    feature_specifications = models.JSONField(default=list, blank=True)
    technical_milestones = models.JSONField(default=list, blank=True)
    
    # Métricas técnicas
    performance_metrics = models.JSONField(default=dict, blank=True,
                                         help_text="Métricas de performance del producto")
    uptime_statistics = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    security_measures = models.TextField(blank=True)
    
    # Propiedad intelectual
    patents_filed = models.JSONField(default=list, blank=True)
    trademarks = models.JSONField(default=list, blank=True)
    trade_secrets = models.TextField(blank=True)
    
    # Escalabilidad y desarrollo
    scalability_plan = models.TextField(blank=True)
    technical_debt_assessment = models.TextField(blank=True)
    development_methodology = models.TextField(blank=True)
    
    # Compliance y regulación
    compliance_standards = models.JSONField(default=list, blank=True)
    data_privacy_measures = models.TextField(blank=True)
    regulatory_considerations = models.TextField(blank=True)
    
    # Documentación técnica
    api_documentation_url = models.URLField(blank=True)
    technical_architecture_url = models.URLField(blank=True)
    code_quality_reports_url = models.URLField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Technology - {self.startup.company_name}"


class PrivateDataAccess(models.Model):
    """Log de accesos a información privada para auditoría"""
    investor = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                               limit_choices_to={'user_type': 'investor'})
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    section_accessed = models.CharField(max_length=50, choices=[
        ('financials', 'Financials'),
        ('people', 'People'),
        ('news', 'News'),
        ('technology', 'Technology'),
    ])
    
    # Tracking
    accessed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-accessed_at']
    
    def __str__(self):
        return f"{self.investor.user.get_full_name()} accessed {self.section_accessed} - {self.startup.company_name}"

class EventComment(models.Model):
    """Comentarios en eventos"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.get_full_name()} on {self.event.title}"


class EventAttendance(models.Model):
    """Asistencia confirmada a eventos"""
    ATTENDANCE_STATUS = [
        ('will_attend', 'Asistiré'),
        ('maybe', 'Tal vez'),
        ('wont_attend', 'No asistiré'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendances')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS, default='will_attend')
    guest_count = models.IntegerField(default=1, help_text="Número de personas que asistirán (incluyéndote)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['event', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.event.title} ({self.status})"


# MODELO DE CONVERSACIÓN DEL CHATBOT IA
class ChatConversation(models.Model):
    """Conversaciones del chatbot IA con el usuario"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_conversations')
    title = models.CharField(max_length=255, default="Nueva conversación")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class ChatMessage(models.Model):
    """Mensajes individuales dentro de una conversación"""
    ROLE_CHOICES = [
        ('user', 'Usuario'),
        ('assistant', 'Asistente'),
        ('system', 'Sistema'),
    ]
    
    conversation = models.ForeignKey(ChatConversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."


# =====================================================
# SISTEMA DE CONEXIONES Y MENSAJERÍA
# =====================================================

class ConnectionRequest(models.Model):
    """Solicitudes de conexión entre startups e inversores (estilo LinkedIn)"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Quien envía y quien recibe (puede ser startup->inversor o inversor->startup)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_connection_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_connection_requests')
    
    # Contexto
    message = models.TextField(max_length=500, blank=True, help_text="Mensaje personalizado de la solicitud")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['sender', 'receiver']
        indexes = [
            models.Index(fields=['sender', 'status']),
            models.Index(fields=['receiver', 'status']),
        ]
    
    def __str__(self):
        return f"{self.sender.get_full_name()} -> {self.receiver.get_full_name()} ({self.status})"
    
    def accept(self):
        """Acepta la solicitud y crea una conversación automáticamente"""
        self.status = 'accepted'
        self.save()
        
        # Crear conversación automática
        Conversation.objects.create(
            participant1=self.sender,
            participant2=self.receiver
        )
    
    def reject(self):
        """Rechaza la solicitud"""
        self.status = 'rejected'
        self.save()
    
    def cancel(self):
        """Cancela la solicitud"""
        self.status = 'cancelled'
        self.save()


class Conversation(models.Model):
    """Conversaciones 1-a-1 entre usuarios conectados"""
    participant1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_p1')
    participant2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_p2')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Estado de lectura
    p1_last_read = models.DateTimeField(null=True, blank=True)
    p2_last_read = models.DateTimeField(null=True, blank=True)
    
    # Google Meet Integration
    meet_enabled = models.BooleanField(default=False, verbose_name="Videollamadas habilitadas")
    meet_link = models.URLField(blank=True, null=True, verbose_name="Enlace de Google Meet")
    meet_created_at = models.DateTimeField(null=True, blank=True)
    meet_created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_meets')
    
    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['participant1', 'participant2']),
            models.Index(fields=['-updated_at']),
        ]
    
    def __str__(self):
        return f"Conversación: {self.participant1.get_full_name()} - {self.participant2.get_full_name()}"
    
    def get_other_participant(self, user):
        """Obtiene el otro participante de la conversación"""
        return self.participant2 if self.participant1 == user else self.participant1
    
    def get_unread_count(self, user):
        """Cuenta mensajes no leídos para un usuario específico"""
        last_read = self.p1_last_read if self.participant1 == user else self.p2_last_read
        
        if last_read:
            return self.messages.filter(
                created_at__gt=last_read
            ).exclude(sender=user).count()
        else:
            return self.messages.exclude(sender=user).count()
    
    def mark_as_read(self, user):
        """Marca la conversación como leída para un usuario"""
        from django.utils import timezone
        now = timezone.now()
        
        if self.participant1 == user:
            self.p1_last_read = now
        else:
            self.p2_last_read = now
        self.save(update_fields=['p1_last_read' if self.participant1 == user else 'p2_last_read'])


class Message(models.Model):
    """Mensajes dentro de una conversación"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    
    # Contenido
    content = models.TextField()
    
    # Archivos adjuntos (opcional)
    attachment = models.FileField(upload_to='message_attachments/', blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.sender.get_full_name()}: {self.content[:50]}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Actualizar timestamp de la conversación
        self.conversation.save()


class Notification(models.Model):
    """Notificación interna del sistema (no push)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=255)  # Preview del mensaje
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
    
    def __str__(self):
        return f"Notificación para {self.user.username}: {self.content[:50]}"
    
    def mark_as_read(self):
        """Marca la notificación como leída"""
        self.is_read = True
        self.save()