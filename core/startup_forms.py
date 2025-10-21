from django import forms
from django.forms import modelformset_factory
from .models import Startup, Industry, UserProfile

class StartupForm(forms.ModelForm):
    class Meta:
        model = Startup
        fields = [
            'company_name', 'tagline', 'description', 'logo', 'cover_image',
            'stage', 'revenue_stage', 'founded_date', 'employees_count',
            'problem_statement', 'solution_description', 'market_size', 
            'business_model', 'competitive_advantage', 'industry', 'sub_industry',
            'monthly_revenue', 'annual_revenue', 'monthly_users', 'burn_rate',
            'runway_months', 'customer_acquisition_cost', 'lifetime_value', 'churn_rate',
            'total_funding_raised', 'seeking_amount', 'valuation',
            'website', 'pitch_deck_url', 'demo_url', 'is_public', 'is_fundraising'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Nombre de la startup'
            }),
            'tagline': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Descripción breve en una línea'
            }),
            'description': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': 6,
                'placeholder': 'Descripción completa de la startup, productos, misión, innovaciones...'
            }),
            'founded_date': forms.DateInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'type': 'date'
            }),
            'website': forms.URLInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'https://tustarrtup.com'
            }),
            'pitch_deck_url': forms.URLInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'https://link-a-tu-pitch-deck.com'
            }),
            'demo_url': forms.URLInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'https://demo.tustarrtup.com'
            }),
            'employees_count': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '5'
            }),
            'stage': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'revenue_stage': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'industry': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'sub_industry': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'ej: Mobile App, B2B SaaS, etc.'
            }),
            'seeking_amount': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '1000000'
            }),
            'monthly_revenue': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '50000'
            }),
            'annual_revenue': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '600000'
            }),
            'monthly_users': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '10000'
            }),
            'problem_statement': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': 3,
                'placeholder': '¿Qué problema específico resuelve tu startup?'
            }),
            'solution_description': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': 3,
                'placeholder': '¿Cómo resuelve el problema tu solución?'
            }),
            'market_size': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': 2,
                'placeholder': 'Tamaño del mercado objetivo (TAM, SAM, SOM)'
            }),
            'business_model': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'SaaS, Marketplace, Freemium, etc.'
            }),
            'competitive_advantage': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': 3,
                'placeholder': '¿Qué te diferencia de la competencia?'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
                'accept': 'image/*'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
                'accept': 'image/*'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer algunos campos opcionales más amigables
        self.fields['cover_image'].required = False
        self.fields['pitch_deck_url'].required = False
        self.fields['demo_url'].required = False
        self.fields['revenue_stage'].required = False
        self.fields['employees_count'].required = False
        self.fields['problem_statement'].required = False
        self.fields['solution_description'].required = False
        self.fields['market_size'].required = False
        self.fields['competitive_advantage'].required = False
        self.fields['sub_industry'].required = False
        self.fields['monthly_revenue'].required = False
        self.fields['annual_revenue'].required = False
        self.fields['monthly_users'].required = False
        self.fields['burn_rate'].required = False
        self.fields['runway_months'].required = False
        self.fields['customer_acquisition_cost'].required = False
        self.fields['lifetime_value'].required = False
        self.fields['churn_rate'].required = False
        self.fields['total_funding_raised'].required = False
        self.fields['seeking_amount'].required = False
        self.fields['valuation'].required = False
        
        # Agregar labels personalizados
        self.fields['company_name'].label = 'Nombre de la Startup'
        self.fields['tagline'].label = 'Descripción Breve'
        self.fields['description'].label = 'Descripción Completa'
        self.fields['founded_date'].label = 'Fecha de Fundación'
        self.fields['website'].label = 'Sitio Web'
        self.fields['pitch_deck_url'].label = 'URL del Pitch Deck'
        self.fields['demo_url'].label = 'URL del Demo'
        self.fields['employees_count'].label = 'Número de Empleados'
        self.fields['stage'].label = 'Etapa de la Empresa'
        self.fields['revenue_stage'].label = 'Etapa de Ingresos'
        self.fields['industry'].label = 'Industria'
        self.fields['sub_industry'].label = 'Sub-industria'
        self.fields['is_fundraising'].label = '¿Recaudando fondos actualmente?'
        self.fields['seeking_amount'].label = 'Monto Buscado ($)'
        self.fields['monthly_revenue'].label = 'Ingresos Mensuales ($)'
        self.fields['annual_revenue'].label = 'Ingresos Anuales ($)'
        self.fields['monthly_users'].label = 'Usuarios Mensuales'
        self.fields['problem_statement'].label = 'Problema que Resuelve'
        self.fields['solution_description'].label = 'Descripción de la Solución'
        self.fields['market_size'].label = 'Tamaño del Mercado'
        self.fields['business_model'].label = 'Modelo de Negocio'
        self.fields['competitive_advantage'].label = 'Ventaja Competitiva'
        self.fields['logo'].label = 'Logo'
        self.fields['cover_image'].label = 'Imagen de Portada'
        self.fields['is_public'].label = 'Perfil Público'
