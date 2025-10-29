from django.contrib import admin
from .models import (
    Contact, Industry, UserProfile, Startup, InvestorProfile, Event, EventRegistration, FounderProfile,
    InvestorAccessRequest, StartupFinancials, StartupPeople, StartupNews, StartupTechnology, PrivateDataAccess,
    ConnectionRequest, Conversation, Message, Notification
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

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'start_datetime', 'status', 'featured']
    search_fields = ['title', 'description']
    list_filter = ['event_type', 'status', 'featured', 'is_virtual']
    list_editable = ['featured', 'status']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'status', 'registration_date']
    search_fields = ['event__title', 'user__first_name', 'user__last_name']
    list_filter = ['status', 'registration_date']

@admin.register(InvestorProfile)
class InvestorProfileAdmin(admin.ModelAdmin):
    list_display = ['fund_name', 'investor_type', 'geographic_focus', 'is_active', 'featured']
    search_fields = ['fund_name', 'user__first_name', 'user__last_name', 'thesis']
    list_filter = ['investor_type', 'geographic_focus', 'is_active', 'featured']
    list_editable = ['featured', 'is_active']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(FounderProfile)
class FounderProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'industry', 'funding_stage', 'featured']
    search_fields = ['user__first_name', 'user__last_name', 'company_name', 'brief_description']
    list_filter = ['industry', 'funding_stage', 'featured', 'country_origin']
    list_editable = ['featured']
    readonly_fields = ['created_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'location', 'is_verified', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'bio']
    list_filter = ['user_type', 'is_verified', 'is_public']
    list_editable = ['is_verified']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'founder', 'stage', 'industry', 'is_fundraising', 'featured', 'created_at']
    search_fields = ['company_name', 'tagline', 'description', 'founder__user__first_name', 'founder__user__last_name']
    list_filter = ['stage', 'revenue_stage', 'industry', 'is_fundraising', 'featured', 'is_public']
    list_editable = ['featured', 'is_fundraising']
    readonly_fields = ['created_at', 'updated_at']

# ===========================================
# ADMIN PARA SISTEMA DE INFORMACIÓN PRIVADA
# ===========================================

@admin.register(InvestorAccessRequest)
class InvestorAccessRequestAdmin(admin.ModelAdmin):
    list_display = ['investor', 'startup', 'status', 'requested_at', 'reviewed_at']
    search_fields = ['investor__user__first_name', 'investor__user__last_name', 'startup__company_name']
    list_filter = ['status', 'requested_at', 'reviewed_at']
    readonly_fields = ['requested_at', 'reviewed_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('investor', 'startup', 'status')
        }),
        ('Solicitud', {
            'fields': ('message', 'requested_at')
        }),
        ('Revisión', {
            'fields': ('reviewed_by', 'review_message', 'reviewed_at', 'expires_at')
        }),
    )

@admin.register(StartupFinancials)
class StartupFinancialsAdmin(admin.ModelAdmin):
    list_display = ['startup', 'arr_current', 'mrr_growth_rate', 'cash_position', 'updated_at']
    search_fields = ['startup__company_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('startup',)
        }),
        ('Métricas de Revenue', {
            'fields': ('arr_current', 'mrr_growth_rate', 'revenue_forecast_12m', 'revenue_forecast_24m')
        }),
        ('Unit Economics', {
            'fields': ('cac_payback_period', 'gross_margin', 'net_revenue_retention')
        }),
        ('Cash & Runway', {
            'fields': ('cash_position', 'burn_rate_detailed', 'runway_calculation')
        }),
        ('Funding Details', {
            'fields': ('current_round_details', 'previous_investors', 'terms_and_conditions')
        }),
        ('Documentos', {
            'fields': ('financial_statements_url', 'cap_table_url', 'business_plan_url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(StartupPeople)
class StartupPeopleAdmin(admin.ModelAdmin):
    list_display = ['startup', 'updated_at']
    search_fields = ['startup__company_name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(StartupNews)
class StartupNewsAdmin(admin.ModelAdmin):
    list_display = ['startup', 'updated_at']
    search_fields = ['startup__company_name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(StartupTechnology)
class StartupTechnologyAdmin(admin.ModelAdmin):
    list_display = ['startup', 'uptime_statistics', 'updated_at']
    search_fields = ['startup__company_name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(PrivateDataAccess)
class PrivateDataAccessAdmin(admin.ModelAdmin):
    list_display = ['investor', 'startup', 'section_accessed', 'accessed_at']
    search_fields = ['investor__user__first_name', 'investor__user__last_name', 'startup__company_name']
    list_filter = ['section_accessed', 'accessed_at']
    readonly_fields = ['accessed_at']


# Importar los modelos del chatbot
from .models import ChatConversation, ChatMessage

@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at', 'updated_at', 'is_active']
    search_fields = ['user__username', 'title']
    list_filter = ['is_active', 'created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'role', 'content_preview', 'created_at']
    search_fields = ['conversation__title', 'content']
    list_filter = ['role', 'created_at']
    readonly_fields = ['created_at']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Contenido'


# =====================================================
# ADMIN PARA SISTEMA DE CONEXIONES Y MENSAJERÍA
# =====================================================

@admin.register(ConnectionRequest)
class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status', 'created_at']
    search_fields = ['sender__first_name', 'sender__last_name', 'receiver__first_name', 'receiver__last_name']
    list_filter = ['status', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'participant1', 'participant2', 'created_at', 'updated_at']
    search_fields = ['participant1__first_name', 'participant1__last_name', 'participant2__first_name', 'participant2__last_name']
    list_filter = ['created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'sender', 'content_preview', 'created_at', 'is_read']
    search_fields = ['conversation__id', 'sender__first_name', 'sender__last_name', 'content']
    list_filter = ['is_read', 'created_at']
    readonly_fields = ['created_at']
    list_editable = ['is_read']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Mensaje'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_preview', 'is_read', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'content']
    list_filter = ['is_read', 'created_at']
    readonly_fields = ['created_at']
    list_editable = ['is_read']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Contenido'

