from django import forms
from .models import (
    StartupFinancials, StartupPeople, StartupNews, StartupTechnology,
    InvestorAccessRequest
)
import json

class StartupFinancialsForm(forms.ModelForm):
    """Formulario para gestionar información financiera privada"""
    
    class Meta:
        model = StartupFinancials
        fields = [
            'arr_current', 'mrr_growth_rate', 'revenue_forecast_12m', 'revenue_forecast_24m',
            'cac_payback_period', 'gross_margin', 'net_revenue_retention',
            'cash_position', 'burn_rate_detailed', 'runway_calculation',
            'current_round_details', 'previous_investors', 'terms_and_conditions',
            'financial_statements_url', 'cap_table_url', 'business_plan_url'
        ]
        widgets = {
            'arr_current': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 150000',
                'step': '0.01'
            }),
            'mrr_growth_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 15.5 (porcentaje)',
                'step': '0.01'
            }),
            'revenue_forecast_12m': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Proyección a 12 meses',
                'step': '0.01'
            }),
            'revenue_forecast_24m': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Proyección a 24 meses',
                'step': '0.01'
            }),
            'cac_payback_period': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Meses para recuperar CAC',
                'step': '0.1'
            }),
            'gross_margin': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 75 (porcentaje)',
                'step': '0.01'
            }),
            'net_revenue_retention': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 110 (porcentaje)',
                'step': '0.01'
            }),
            'cash_position': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Efectivo actual en banco',
                'step': '0.01'
            }),
            'burn_rate_detailed': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Burn rate mensual',
                'step': '0.01'
            }),
            'runway_calculation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Explica el cálculo del runway...'
            }),
            'current_round_details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Detalles de la ronda actual de funding...'
            }),
            'previous_investors': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Lista de inversionistas previos...'
            }),
            'terms_and_conditions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Términos y condiciones relevantes...'
            }),
            'financial_statements_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL a estados financieros'
            }),
            'cap_table_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL a cap table'
            }),
            'business_plan_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL a plan de negocio'
            }),
        }
        labels = {
            'arr_current': 'ARR Actual ($)',
            'mrr_growth_rate': 'Tasa de Crecimiento MRR (%)',
            'revenue_forecast_12m': 'Proyección Revenue 12 meses ($)',
            'revenue_forecast_24m': 'Proyección Revenue 24 meses ($)',
            'cac_payback_period': 'Periodo de Recuperación CAC (meses)',
            'gross_margin': 'Margen Bruto (%)',
            'net_revenue_retention': 'Net Revenue Retention (%)',
            'cash_position': 'Posición de Efectivo ($)',
            'burn_rate_detailed': 'Burn Rate Mensual ($)',
            'runway_calculation': 'Cálculo del Runway',
            'current_round_details': 'Detalles Ronda Actual',
            'previous_investors': 'Inversionistas Previos',
            'terms_and_conditions': 'Términos y Condiciones',
            'financial_statements_url': 'URL Estados Financieros',
            'cap_table_url': 'URL Cap Table',
            'business_plan_url': 'URL Plan de Negocio'
        }

    # Campos para JSON (funding_use_breakdown)
    funding_use_breakdown_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Ejemplo:\n{\n  "product_development": 40,\n  "marketing": 30,\n  "hiring": 20,\n  "operations": 10\n}'
        }),
        required=False,
        label='Desglose de Uso de Fondos (JSON)',
        help_text='Formato JSON con categorías y porcentajes'
    )

    financial_projections_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Ejemplo:\n{\n  "q1_2024": {"revenue": 50000, "expenses": 40000},\n  "q2_2024": {"revenue": 75000, "expenses": 50000}\n}'
        }),
        required=False,
        label='Proyecciones Financieras (JSON)',
        help_text='Formato JSON con proyecciones por periodo'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Cargar datos JSON existentes
            if self.instance.funding_use_breakdown:
                self.fields['funding_use_breakdown_text'].initial = json.dumps(
                    self.instance.funding_use_breakdown, indent=2
                )
            if self.instance.financial_projections:
                self.fields['financial_projections_text'].initial = json.dumps(
                    self.instance.financial_projections, indent=2
                )

    def clean_funding_use_breakdown_text(self):
        data = self.cleaned_data.get('funding_use_breakdown_text')
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                raise forms.ValidationError('Formato JSON inválido')
        return {}

    def clean_financial_projections_text(self):
        data = self.cleaned_data.get('financial_projections_text')
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                raise forms.ValidationError('Formato JSON inválido')
        return {}

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Guardar campos JSON
        funding_breakdown = self.cleaned_data.get('funding_use_breakdown_text')
        if funding_breakdown:
            instance.funding_use_breakdown = funding_breakdown
        
        financial_projections = self.cleaned_data.get('financial_projections_text')
        if financial_projections:
            instance.financial_projections = financial_projections
        
        if commit:
            instance.save()
        return instance


class StartupPeopleForm(forms.ModelForm):
    """Formulario para gestionar información de equipo privada"""
    
    class Meta:
        model = StartupPeople
        fields = [
            'company_values', 'remote_work_policy', 'compensation_philosophy',
            'diversity_initiatives', 'key_roles_needed', 'org_chart_url',
            'company_culture_deck_url'
        ]
        widgets = {
            'company_values': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe los valores fundamentales de la empresa...'
            }),
            'remote_work_policy': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Política de trabajo remoto...'
            }),
            'compensation_philosophy': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Filosofía de compensación...'
            }),
            'diversity_initiatives': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Iniciativas de diversidad e inclusión...'
            }),
            'key_roles_needed': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Roles clave que necesitan contratar...'
            }),
            'org_chart_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL al organigrama'
            }),
            'company_culture_deck_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL al deck de cultura empresarial'
            }),
        }
        labels = {
            'company_values': 'Valores de la Empresa',
            'remote_work_policy': 'Política de Trabajo Remoto',
            'compensation_philosophy': 'Filosofía de Compensación',
            'diversity_initiatives': 'Iniciativas de Diversidad',
            'key_roles_needed': 'Roles Clave Necesarios',
            'org_chart_url': 'URL Organigrama',
            'company_culture_deck_url': 'URL Deck de Cultura'
        }

    # Campos JSON
    founders_bios_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'placeholder': 'Ejemplo:\n{\n  "founder1": {"name": "Juan Pérez", "bio": "...", "linkedin": "..."},\n  "founder2": {"name": "María López", "bio": "...", "linkedin": "..."}\n}'
        }),
        required=False,
        label='Biografías Detalladas de Fundadores (JSON)'
    )

    equity_distribution_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Ejemplo:\n{\n  "founders": 70,\n  "employees": 15,\n  "investors": 15\n}'
        }),
        required=False,
        label='Distribución de Equity (JSON)'
    )

    hiring_plan_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Ejemplo:\n{\n  "q1": ["Senior Developer", "Product Manager"],\n  "q2": ["Sales Rep", "Designer"]\n}'
        }),
        required=False,
        label='Plan de Contrataciones 12m (JSON)'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.founders_detailed_bios:
                self.fields['founders_bios_text'].initial = json.dumps(
                    self.instance.founders_detailed_bios, indent=2
                )
            if self.instance.equity_distribution:
                self.fields['equity_distribution_text'].initial = json.dumps(
                    self.instance.equity_distribution, indent=2
                )
            if self.instance.hiring_plan_12m:
                self.fields['hiring_plan_text'].initial = json.dumps(
                    self.instance.hiring_plan_12m, indent=2
                )

    def clean_founders_bios_text(self):
        data = self.cleaned_data.get('founders_bios_text')
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                raise forms.ValidationError('Formato JSON inválido')
        return {}

    def clean_equity_distribution_text(self):
        data = self.cleaned_data.get('equity_distribution_text')
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                raise forms.ValidationError('Formato JSON inválido')
        return {}

    def clean_hiring_plan_text(self):
        data = self.cleaned_data.get('hiring_plan_text')
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                raise forms.ValidationError('Formato JSON inválido')
        return {}

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Guardar campos JSON
        founders_bios = self.cleaned_data.get('founders_bios_text')
        if founders_bios:
            instance.founders_detailed_bios = founders_bios
        
        equity_dist = self.cleaned_data.get('equity_distribution_text')
        if equity_dist:
            instance.equity_distribution = equity_dist
        
        hiring_plan = self.cleaned_data.get('hiring_plan_text')
        if hiring_plan:
            instance.hiring_plan_12m = hiring_plan
        
        if commit:
            instance.save()
        return instance


class StartupNewsForm(forms.ModelForm):
    """Formulario para gestionar noticias y updates privados"""
    
    class Meta:
        model = StartupNews
        fields = [
            'competitive_analysis', 'market_developments', 'partnership_opportunities',
            'investor_letter_template'
        ]
        widgets = {
            'competitive_analysis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Análisis competitivo detallado...'
            }),
            'market_developments': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Desarrollos importantes del mercado...'
            }),
            'partnership_opportunities': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Oportunidades de partnerships...'
            }),
            'investor_letter_template': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Template para cartas a inversionistas...'
            }),
        }
        labels = {
            'competitive_analysis': 'Análisis Competitivo',
            'market_developments': 'Desarrollos del Mercado',
            'partnership_opportunities': 'Oportunidades de Partnership',
            'investor_letter_template': 'Template Carta a Inversionistas'
        }


class StartupTechnologyForm(forms.ModelForm):
    """Formulario para gestionar información técnica privada"""
    
    class Meta:
        model = StartupTechnology
        fields = [
            'architecture_overview', 'infrastructure_details', 'uptime_statistics',
            'security_measures', 'scalability_plan', 'technical_debt_assessment',
            'development_methodology', 'data_privacy_measures', 'regulatory_considerations',
            'api_documentation_url', 'technical_architecture_url', 'code_quality_reports_url'
        ]
        widgets = {
            'architecture_overview': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Overview de la arquitectura técnica...'
            }),
            'infrastructure_details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Detalles de infraestructura...'
            }),
            'uptime_statistics': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 99.9',
                'step': '0.001'
            }),
            'security_measures': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Medidas de seguridad implementadas...'
            }),
            'scalability_plan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Plan de escalabilidad...'
            }),
            'technical_debt_assessment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Evaluación de deuda técnica...'
            }),
            'development_methodology': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Metodología de desarrollo...'
            }),
            'data_privacy_measures': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Medidas de privacidad de datos...'
            }),
            'regulatory_considerations': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Consideraciones regulatorias...'
            }),
            'api_documentation_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL documentación API'
            }),
            'technical_architecture_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL arquitectura técnica'
            }),
            'code_quality_reports_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL reportes de calidad de código'
            }),
        }
        labels = {
            'architecture_overview': 'Overview de Arquitectura',
            'infrastructure_details': 'Detalles de Infraestructura',
            'uptime_statistics': 'Estadísticas de Uptime (%)',
            'security_measures': 'Medidas de Seguridad',
            'scalability_plan': 'Plan de Escalabilidad',
            'technical_debt_assessment': 'Evaluación Deuda Técnica',
            'development_methodology': 'Metodología de Desarrollo',
            'data_privacy_measures': 'Medidas de Privacidad de Datos',
            'regulatory_considerations': 'Consideraciones Regulatorias',
            'api_documentation_url': 'URL Documentación API',
            'technical_architecture_url': 'URL Arquitectura Técnica',
            'code_quality_reports_url': 'URL Reportes Calidad'
        }


class AccessRequestForm(forms.ModelForm):
    """Formulario para solicitudes de acceso"""
    
    class Meta:
        model = InvestorAccessRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Explica tu interés en esta startup y por qué necesitas acceso a información privada...',
                'required': True
            })
        }
        labels = {
            'message': 'Mensaje de Solicitud'
        }
