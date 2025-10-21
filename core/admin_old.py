from django.contrib import admin
from .models import Contact, FounderProfile, Event, Industry, InvestorProfile

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'read']
    search_fields = ['name', 'email', 'subject', 'message']
    list_filter = ['read', 'created_at']
    readonly_fields = ['created_at']
    list_editable = ['read']

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']

@admin.register(FounderProfile)
class FounderProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'industry', 'funding_stage', 'featured', 'created_at']
    search_fields = ['company_name', 'user__first_name', 'user__last_name', 'brief_description']
    list_filter = ['industry', 'funding_stage', 'featured', 'country_origin']
    list_editable = ['featured']
    readonly_fields = ['created_at']

from django.contrib import admin
from .models import (
    Contact, Industry, UserProfile, Startup, FoundingTeam, 
    AdvisorNetwork, FundingRound, InvestorProfile, Event, 
    EventRegistration, FounderProfile
)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'read']
    search_fields = ['name', 'email', 'subject', 'message']
    list_filter = ['read', 'created_at']
    readonly_fields = ['created_at']
    list_editable = ['read']

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'location', 'is_verified', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'bio']
    list_filter = ['user_type', 'is_verified', 'created_at']
    list_editable = ['is_verified']
    readonly_fields = ['created_at', 'updated_at']

class FoundingTeamInline(admin.TabularInline):
    model = FoundingTeam
    extra = 1

class AdvisorNetworkInline(admin.TabularInline):
    model = AdvisorNetwork
    extra = 1

class FundingRoundInline(admin.TabularInline):
    model = FundingRound
    extra = 1

@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'founder', 'stage', 'industry', 'is_fundraising', 'featured', 'created_at']
    search_fields = ['company_name', 'founder__user__first_name', 'founder__user__last_name', 'description']
    list_filter = ['stage', 'industry', 'is_fundraising', 'featured', 'revenue_stage']
    list_editable = ['featured', 'is_fundraising']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [FoundingTeamInline, AdvisorNetworkInline, FundingRoundInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('company_name', 'founder', 'tagline', 'description', 'logo', 'cover_image')
        }),
        ('Estado de la Compañía', {
            'fields': ('stage', 'revenue_stage', 'founded_date', 'employees_count')
        }),
        ('Tesis de Inversión', {
            'fields': ('problem_statement', 'solution_description', 'market_size', 'business_model', 'competitive_advantage')
        }),
        ('Industria', {
            'fields': ('industry', 'sub_industry')
        }),
        ('Métricas Clave', {
            'fields': ('monthly_revenue', 'annual_revenue', 'monthly_users', 'burn_rate', 'runway_months', 'customer_acquisition_cost', 'lifetime_value', 'churn_rate')
        }),
        ('Funding', {
            'fields': ('total_funding_raised', 'seeking_amount', 'valuation')
        }),
        ('Enlaces', {
            'fields': ('website', 'pitch_deck_url', 'demo_url')
        }),
        ('Configuración', {
            'fields': ('is_public', 'is_fundraising', 'featured')
        }),
        ('Timestamps', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(FoundingTeam)
class FoundingTeamAdmin(admin.ModelAdmin):
    list_display = ['member', 'startup', 'role', 'equity_percentage', 'is_active']
    search_fields = ['member__user__first_name', 'member__user__last_name', 'startup__company_name']
    list_filter = ['role', 'is_active']

@admin.register(AdvisorNetwork)
class AdvisorNetworkAdmin(admin.ModelAdmin):
    list_display = ['advisor', 'startup', 'expertise_area', 'is_active']
    search_fields = ['advisor__user__first_name', 'advisor__user__last_name', 'startup__company_name']
    list_filter = ['is_active', 'expertise_area']

@admin.register(FundingRound)
class FundingRoundAdmin(admin.ModelAdmin):
    list_display = ['startup', 'round_type', 'amount_raised', 'round_date', 'lead_investor']
    search_fields = ['startup__company_name', 'lead_investor']
    list_filter = ['round_type', 'currency', 'round_date']
    ordering = ['-round_date']

@admin.register(InvestorProfile)
class InvestorProfileAdmin(admin.ModelAdmin):
    list_display = ['fund_name', 'investor_type', 'geographic_focus', 'is_accepting_pitches', 'featured', 'created_at']
    search_fields = ['fund_name', 'user_profile__user__first_name', 'user_profile__user__last_name', 'thesis']
    list_filter = ['investor_type', 'geographic_focus', 'is_accepting_pitches', 'featured', 'is_active']
    list_editable = ['featured', 'is_accepting_pitches']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['focus_industries']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'start_datetime', 'status', 'is_virtual', 'featured']
    search_fields = ['title', 'description', 'location']
    list_filter = ['event_type', 'status', 'is_virtual', 'featured', 'is_free']
    list_editable = ['status', 'featured']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['co_organizers', 'speakers']

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'status', 'registration_date']
    search_fields = ['user__user__first_name', 'user__user__last_name', 'event__title']
    list_filter = ['status', 'registration_date']
    list_editable = ['status']

# Mantener compatibilidad con modelo legacy
@admin.register(FounderProfile)
class FounderProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'industry', 'funding_stage', 'featured', 'created_at']
    search_fields = ['company_name', 'user__first_name', 'user__last_name', 'brief_description']
    list_filter = ['industry', 'funding_stage', 'featured', 'country_origin']
    list_editable = ['featured']
    readonly_fields = ['created_at']

@admin.register(InvestorProfile)
class InvestorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'investor_type', 'featured', 'created_at']
    search_fields = ['company_name', 'user__first_name', 'user__last_name']
    list_filter = ['investor_type', 'featured']
    list_editable = ['featured']
    readonly_fields = ['created_at']