#!/bin/bash

# Configuración del nombre del proyecto
PROJECT_NAME="mydevsite"
echo "Iniciando la configuración del proyecto: $PROJECT_NAME"

# Crear entorno virtual
echo "Creando entorno virtual..."
python -m venv venv

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Crear archivo requirements.txt
echo "Creando archivo requirements.txt..."
cat > requirements.txt << EOL
Django==5.0.0
python-dotenv==1.0.0
django-compressor==4.4
django-htmx==1.17.0
pillow==10.0.0
gunicorn==21.2.0
whitenoise==6.5.0
EOL

# Instalar dependencias
echo "Instalando dependencias de Python..."
pip install -r requirements.txt

# Crear proyecto Django
echo "Creando proyecto Django: $PROJECT_NAME..."
django-admin startproject $PROJECT_NAME .

# Crear aplicaciones
echo "Creando aplicaciones..."
python manage.py startapp core
python manage.py startapp portfolio

# Crear estructura de directorios
echo "Creando estructura de directorios..."
mkdir -p templates
mkdir -p core/templates/core
mkdir -p portfolio/templates/portfolio
mkdir -p static/css
mkdir -p static/js
mkdir -p static/img
mkdir -p media/projects
mkdir -p media/testimonials
mkdir -p static/src

# Configurar archivo .env
echo "Configurando archivo .env..."
cat > .env << EOL
SECRET_KEY=django-insecure-mydevsite-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EOL

# Crear package.json
echo "Creando package.json..."
cat > package.json << EOL
{
  "name": "mydevsite",
  "version": "1.0.0",
  "description": "Landing page for custom development services",
  "scripts": {
    "build": "tailwindcss build -i ./static/src/input.css -o ./static/css/output.css --minify",
    "watch": "tailwindcss build -i ./static/src/input.css -o ./static/css/output.css --watch"
  },
  "dependencies": {
    "alpinejs": "^3.13.0",
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.24",
    "tailwindcss": "^3.3.2"
  }
}
EOL

# Crear tailwind.config.js
echo "Creando configuración de Tailwind CSS..."
cat > tailwind.config.js << EOL
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './core/templates/**/*.html',
    './portfolio/templates/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#0f172a',
        'secondary': '#38bdf8',
        'accent': '#f97316',
      },
      fontFamily: {
        'sans': ['Inter', 'sans-serif'],
        'display': ['Poppins', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-in': 'slideIn 0.5s ease-in-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideIn: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
EOL

# Crear archivo de entrada para Tailwind CSS
echo "Configurando CSS de entrada para Tailwind..."
cat > static/src/input.css << EOL
@tailwind base;
@tailwind components;
@tailwind utilities;
EOL

# Configurar settings.py
echo "Configurando settings.py..."
cat > $PROJECT_NAME/settings.py << EOL
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-key-for-development-only')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Aplicaciones de terceros
    'compressor',
    'django_htmx',
    
    # Aplicaciones propias
    'core',
    'portfolio',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para servir archivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',  # Para HTMX
]

ROOT_URLCONF = '$PROJECT_NAME.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '$PROJECT_NAME.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Comprimir archivos estáticos
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'webmaster@localhost')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Archivos estáticos en producción
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
EOL

# Configurar urls.py del proyecto
echo "Configurando urls.py del proyecto..."
cat > $PROJECT_NAME/urls.py << EOL
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('portfolio/', include('portfolio.urls')),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
EOL

# Crear modelos en core/models.py
echo "Creando modelos en core..."
cat > core/models.py << EOL
from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, help_text="Nombre del ícono de Font Awesome")
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['order']

class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    quote = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} - {self.company}"
    
    class Meta:
        ordering = ['order']

class ContactMessage(models.Model):
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
EOL

# Crear admin.py en core
echo "Configurando admin.py de core..."
cat > core/admin.py << EOL
from django.contrib import admin
from .models import Service, Testimonial, ContactMessage

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'rating', 'active', 'order')
    list_editable = ('active', 'order')
    list_filter = ('active', 'rating')
    search_fields = ('name', 'company', 'quote')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'read')
    list_editable = ('read',)
    list_filter = ('read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
EOL

# Crear forms.py en core
echo "Creando forms.py en core..."
cat > core/forms.py << EOL
from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-secondary', 'placeholder': 'Tu nombre'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-secondary', 'placeholder': 'tu@email.com'}),
            'subject': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-secondary', 'placeholder': 'Asunto'}),
            'message': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-secondary', 'placeholder': 'Tu mensaje', 'rows': 5}),
        }
EOL

# Crear views.py en core
echo "Creando views.py en core..."
cat > core/views.py << EOL
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from .models import Service, Testimonial
from .forms import ContactForm
from portfolio.models import Project

class IndexView(TemplateView):
    template_name = 'core/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['testimonials'] = Testimonial.objects.filter(active=True)
        context['featured_projects'] = Project.objects.filter(featured=True)[:3]
        context['contact_form'] = ContactForm()
        return context

class ContactFormView(FormView):
    form_class = ContactForm
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        # Guardar el mensaje
        form.save()
        
        if self.request.htmx:
            return HttpResponse(
                '<div class="p-4 mb-4 text-green-800 bg-green-100 rounded-lg">'
                'Gracias por tu mensaje. Te contactaremos pronto.'
                '</div>',
                headers={'HX-Trigger': 'contactFormSubmitted'}
            )
        
        messages.success(self.request, 'Mensaje enviado correctamente.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if self.request.htmx:
            return HttpResponse(
                '<div class="p-4 mb-4 text-red-800 bg-red-100 rounded-lg">'
                'Por favor corrige los errores en el formulario.'
                '</div>' + form.as_p(),
                status=400
            )
        
        return super().form_invalid(form)

def services_view(request):
    services = Service.objects.all()
    return render(request, 'core/services.html', {'services': services})
EOL

# Crear urls.py en core
echo "Creando urls.py en core..."
cat > core/urls.py << EOL
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('servicios/', views.services_view, name='services'),
    path('contacto/', views.ContactFormView.as_view(), name='contact'),
]
EOL

# Crear modelos en portfolio
echo "Creando modelos en portfolio..."
cat > portfolio/models.py << EOL
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Technology(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, help_text="Nombre del icono o clase CSS")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Technologies"

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200)
    client = models.CharField(max_length=200, blank=True)
    completed_date = models.DateField()
    image = models.ImageField(upload_to='projects/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    technologies = models.ManyToManyField(Technology)
    url = models.URLField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-completed_date']

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.project.title} - Image {self.order}"
    
    class Meta:
        ordering = ['order']
EOL

# Crear views.py en portfolio
echo "Creando views.py en portfolio..."
cat > portfolio/views.py << EOL
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Project, Category

class ProjectListView(ListView):
    model = Project
    template_name = 'portfolio/project_list.html'
    context_object_name = 'projects'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.GET.get('category')
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        return queryset

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener proyectos relacionados (misma categoría)
        context['related_projects'] = Project.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context
EOL

# Crear urls.py en portfolio
echo "Creando urls.py en portfolio..."
cat > portfolio/urls.py << EOL
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
]
EOL

# Crear admin.py en portfolio
echo "Configurando admin.py de portfolio..."
cat > portfolio/admin.py << EOL
from django.contrib import admin
from .models import Category, Technology, Project, ProjectImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'completed_date', 'featured')
    list_filter = ('category', 'featured', 'technologies')
    search_fields = ('title', 'description', 'client')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
EOL

# Crear plantilla base.html
echo "Creando plantilla base.html..."
mkdir -p templates
cat > templates/base.html << EOL
<!DOCTYPE html>
<html lang="es" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Tu Nombre - Desarrollos a Medida{% endblock %}</title>
    <meta name="description" content="{% block meta_description %}Desarrollo de software a medida con las últimas tecnologías. Soluciones personalizadas para tu negocio.{% endblock %}">
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Tailwind CSS -->
    <link rel="stylesheet" href="/static/css/output.css">
    
    <!-- Alpine.js -->
    <script defer src="https://unpkg.com/alpinejs@3.13.0/dist/cdn.min.js"></script>
    
    <!-- HTMX -->
    <script src="https://unpkg.com/htmx.org@1.9.4"></script>
    
    {% block extra_head %}{% endblock %}
</head>
<body class="font-sans antialiased text-gray-800 bg-white">
    <!-- Header/Navbar -->
    <header x-data="{ mobileMenuOpen: false }" class="sticky top-0 z-50 bg-white shadow-sm">
        <nav class="container px-4 py-4 mx-auto sm:px-6 lg:px-8">
            <div class="flex items-center justify-between">
                <!-- Logo -->
                <div class="flex-shrink-0">
                    <a href="{% url 'index' %}" class="text-2xl font-bold text-primary">
                        <span class="text-accent">Dev</span>Studio
                    </a>
                </div>
                
                <!-- Desktop Navigation -->
                <div class="hidden space-x-8 md:flex">
                    <a href="{% url 'index' %}" class="px-2 py-1 font-medium text-gray-700 transition-colors hover:text-accent">Inicio</a>
                    <a href="#servicios" class="px-2 py-1 font-medium text-gray-700 transition-colors hover:text-accent">Servicios</a>
                    <a href="{% url 'project_list' %}" class="px-2 py-1 font-medium text-gray-700 transition-colors hover:text-accent">Portfolio</a>
                    <a href="#contacto" class="px-2 py-1 font-medium text-gray-700 transition-colors hover:text-accent">Contacto</a>
                </div>
                
                <!-- CTA Button -->
                <div class="hidden md:block">
                    <a href="#contacto" class="px-5 py-2 font-medium text-white transition-all rounded-lg bg-accent hover:bg-accent/90">Contáctame</a>
                </div>
                
                <!-- Mobile menu button -->
                <div class="flex md:hidden">
                    <button @click="mobileMenuOpen = !mobileMenuOpen" class="text-gray-700">
                        <svg x-show="!mobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
                        <svg x-show="mobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    </button>
                </div>
            </div>
            
            <!-- Mobile Menu -->
            <div x-show="mobileMenuOpen" class="md:hidden" 
                 x-transition:enter="transition ease-out duration-200"
                 x-transition:enter-start="opacity-0 -translate-y-4"
                 x-transition:enter-end="opacity-100 translate-y-0"
                 x-transition:leave="transition ease-in duration-150"
                 x-transition:leave-start="opacity-100 translate-y-0"
                 x-transition:leave-end="opacity-0 -translate-y-4">
                <div class="px-2 pt-2 pb-3 space-y-1 bg-white rounded-md shadow-lg">
                    <a href="{% url 'index' %}" class="block px-3 py-2 text-base font-medium text-gray-700 rounded-md hover:bg-gray-50 hover:text-accent">Inicio</a>
                    <a href="#servicios" class="block px-3 py-2 text-base font-medium text-gray-700 rounded-md hover:bg-gray-50 hover:text-accent">Servicios</a>
                    <a href="{% url 'project_list' %}" class="block px-3 py-2 text-base font-medium text-gray-700 rounded-md hover:bg-gray-50 hover:text-accent">Portfolio</a>
                    <a href="#contacto" class="block px-3 py-2 text-base font-medium text-gray-700 rounded-md hover:bg-gray-50 hover:text-accent">Contacto</a>
                    <a href="#contacto" class="block px-3 py-2 text-base font-medium text-white rounded-md bg-accent hover:bg-accent/90">Contáctame</a>
                </div>
            </div>
        </nav>
    </header>
    
    <!-- Main Content -->
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer -->
    <footer class="py-12 text-white bg-primary">
        <div class="container px-4 mx-auto sm:px-6 lg:px-8">
            <div class="grid gap-8 md:grid-cols-3">
                <!-- Logo & About -->
                <div>
                    <a href="{% url 'index' %}" class="text-2xl font-bold">
                        <span class="text-accent">Dev</span>Studio
                    </a>
                    <p class="mt-4 text-gray-400">
                        Soluciones de desarrollo a medida con las últimas tecnologías para potenciar tu negocio.
                    </p>
                    <div class="flex mt-6 space-x-4">
                        <a href="#" class="text-gray-400 hover:text-white">
                            <i class="fab fa-twitter"></i>
                        </a>
                        <a href="#" class="text-gray-400 hover:text-white">
                            <i class="fab fa-linkedin-in"></i>
                        </a>
                        <a href="#" class="text-gray-400 hover:text-white">
                            <i class="fab fa-github"></i>
                        </a>
                    </div>
                </div>
                
                <!-- Links -->
                <div>
                    <h3 class="text-lg font-semibold text-white">Enlaces Rápidos</h3>
                    <ul class="mt-4 space-y-2">
                        <li><a href="{% url 'index' %}" class="text-gray-400 transition-colors hover:text-white">Inicio</a></li>
                        <li><a href="#servicios" class="text-gray-400 transition-colors hover:text-white">Servicios</a></li>
                        <li><a href="{% url 'project_list' %}" class="text-gray-400 transition-colors hover:text-white">Portfolio</a></li>
                        <li><a href="#contacto" class="text-gray-400 transition-colors hover:text-white">Contacto</a></li>
                    </ul>
                </div>
                
                <!-- Contact -->
                <div>
                    <h3 class="text-lg font-semibold text-white">Contacto</h3>
                    <ul class="mt-4 space-y-2">
                        <li class="flex items-center">
                            <i class="w-5 mr-2 text-gray-400 fa-solid fa-envelope"></i>
                            <a href="mailto:tu@email.com" class="text-gray-400 hover:text-white">tu@email.com</a>
                        </li>
                        <li class="flex items-center">
                            <i class="w-5 mr-2 text-gray-400 fa-solid fa-phone"></i>
                            <a href="tel:+123456789" class="text-gray-400 hover:text-white">+12 345 6789</a>
                        </li>
                        <li class="flex items-center">
                            <i class="w-5 mr-2 text-gray-400 fa-solid fa-location-dot"></i>
                            <span class="text-gray-400">Tu Ciudad, País</span>
                        </li>
                    </ul>
                </div>
            </div>
            
            <div class="pt-8 mt-8 border-t border-gray-700">
                <p class="text-center text-gray-400">
                    © {% now 'Y' %} DevStudio. Todos los derechos reservados.
                </p>
            </div>
        </div>
    </footer>
    
    <!-- Notification for messages -->
    {% if messages %}
    <div class="fixed bottom-4 right-4 z-50" x-data="{ show: true }" x-init="setTimeout(() => { show = false }, 5000)" x-show="show"
         x-transition:enter="transition ease-out duration-300"
         x-transition:enter-start="opacity-0 transform scale-90"
         x-transition:enter-end="opacity-100 transform scale-100"
         x-transition:leave="transition ease-in duration-300"
         x-transition:leave-start="opacity-100 transform scale-100"
         x-transition:leave-end="opacity-0 transform scale-90">
        {% for message in messages %}
        <div class="p-4 mb-4 text-white rounded-lg shadow-lg {% if message.tags == 'success' %}bg-green-600{% elif message.tags == 'error' %}bg-red-600{% else %}bg-blue-600{% endif %}">
            <div class="flex items-center">
                <div class="mr-2">
                    {% if message.tags == 'success' %}
                    <i class="fas fa-check-circle"></i>
                    {% elif message.tags == 'error' %}
                    <i class="fas fa-exclamation-circle"></i>
                    {% else %}
                    <i class="fas fa-info-circle"></i>
                    {% endif %}
                </div>
                <div>{{ message }}</div>
                <button @click="show = false" class="ml-4">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
        {% endfor %}
    </div>
    {% endif %}
    
    {% block extra_js %}{% endblock %}
</body>
</html>
EOL

# Crear plantillas clave
echo "Creando plantillas para la aplicación core..."

# Crear index.html de core
mkdir -p core/templates/core
cat > core/templates/core/index.html << EOL
{% extends 'base.html' %}
{% load static %}

{% block title %}DevStudio - Desarrollo de Software a Medida{% endblock %}

{% block content %}
<!-- Hero Section -->
<section class="relative py-20 overflow-hidden bg-gradient-to-br from-primary to-primary/90">
    <div class="container relative px-4 mx-auto sm:px-6 lg:px-8">
        <div class="grid items-center grid-cols-1 gap-12 lg:grid-cols-2">
            <div class="animate-fade-in">
                <h1 class="text-4xl font-bold text-white md:text-5xl lg:text-6xl font-display">
                    Desarrollo a medida para impulsar tu <span class="text-accent">visión</span>
                </h1>
                <p class="mt-6 text-xl text-gray-300">
                    Transformamos tus ideas en soluciones digitales excepcionales con las tecnologías más avanzadas
                </p>
                <div class="flex flex-wrap gap-4 mt-8">
                    <a href="#contacto" class="px-6 py-3 text-lg font-medium text-white transition-all rounded-lg bg-accent hover:bg-accent/90">
                        Solicitar presupuesto
                    </a>
                    <a href="#servicios" class="px-6 py-3 text-lg font-medium transition-colors rounded-lg text-accent border border-accent hover:bg-accent/10">
                        Ver servicios
                    </a>
                </div>
            </div>
            <div class="relative order-first lg:order-last animate-fade-in">
                <div class="relative z-10 p-4 bg-white rounded-lg shadow-xl lg:p-8">
                    <img src="{% static 'img/hero-image.jpg' %}" alt="Desarrollo a medida" class="w-full h-auto rounded">
                </div>
                <!-- Decorative elements -->
                <div class="absolute -top-4 -left-4 w-24 h-24 bg-secondary/20 rounded-full blur-xl"></div>
                <div class="absolute -bottom-8 -right-8 w-32 h-32 bg-accent/20 rounded-full blur-xl"></div>
            </div>
        </div>
        
        <!-- Brands/Tech stack -->
        <div class="pt-16 mt-16 border-t border-gray-700/30">
            <p class="mb-6 text-sm font-medium tracking-wider text-center text-gray-400 uppercase">Tecnologías que dominamos</p>
            <div class="flex flex-wrap items-center justify-center gap-8 text-gray-400">
                <div class="flex items-center">
                    <i class="text-3xl fab fa-python"></i>
                    <span class="ml-2 text-xl">Python</span>
                </div>
                <div class="flex items-center">
                    <i class="text-3xl fab fa-react"></i>
                    <span class="ml-2 text-xl">React</span>
                </div>
                <div class="flex items-center">
                    <i class="text-3xl fab fa-js"></i>
                    <span class="ml-2 text-xl">JavaScript</span>
                </div>
                <div class="flex items-center">
                    <i class="text-3xl fab fa-node-js"></i>
                    <span class="ml-2 text-xl">Node.js</span>
                </div>
                <div class="flex items-center">
                    <svg class="w-8 h-8" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12.9547 22.5195C12.9771 22.8731 12.6343 23.2093 12.1403 23.1142C5.61965 21.9678 0.885254 16.3931 0.885254 9.67376C0.885254 8.65198 1.01718 7.66154 1.2667 6.71313C1.39361 6.24426 1.90175 5.99112 2.33104 6.16745C2.76033 6.34379 3.14999 6.84302 3.01766 7.31058C2.80136 8.10632 2.68637 8.93368 2.68637 9.78209C2.68637 15.5477 6.72528 20.3505 12.2583 21.3541C12.7523 21.4507 12.9323 22.166 12.9547 22.5195ZM20.053 4.88457C20.053 4.88457 19.3797 6.9351 17.4823 7.80887C16.1624 8.40165 15.1853 9.24929 14.0865 10.1346C13.4129 10.6771 13.1798 11.6058 13.1798 12.4687C13.1798 13.3317 13.1798 14.348 13.1798 14.348C13.1798 14.348 14.1967 14.348 14.543 14.348C15.0985 14.348 15.559 14.8085 15.559 15.364V16.3809C15.559 16.9364 15.0985 17.3969 14.543 17.3969H11.4878C10.9323 17.3969 10.4718 16.9364 10.4718 16.3809V14.7728C10.4718 14.7728 10.4718 12.553 10.4718 10.8372C10.4718 9.12135 11.0512 7.14698 13.1798 5.70103C15.3084 4.25509 17.109 4.06368 17.109 4.06368C17.109 4.06368 16.8923 3.05831 16.8923 2.55671C16.8923 2.05511 17.1339 1.69765 17.6854 2.02051C20.053 3.39924 22.0185 5.42853 23.2737 7.85506C23.5337 8.339 23.4236 8.89082 22.9289 9.08429C22.4342 9.27777 21.9115 9.04981 21.648 8.56722C21.0361 7.4639 20.2631 6.46674 19.3685 5.61696C19.2734 5.52186 19.4452 5.18125 19.6429 5.10224C19.8405 5.02323 20.053 4.88457 20.053 4.88457Z" fill="currentColor"/>
                    </svg>
                    <span class="ml-2 text-xl">Django</span>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Resto de secciones aquí (esto es solo una parte del index.html) -->
<!-- Para mantener el script en un tamaño manejable, solo incluyo parte del HTML -->
<!-- Services Section -->
<section id="servicios" class="py-20 bg-gray-50">
    <div class="container px-4 mx-auto sm:px-6 lg:px-8">
        <div class="max-w-3xl mx-auto text-center">
            <h2 class="text-3xl font-bold text-primary md:text-4xl font-display">Nuestros Servicios</h2>
            <p class="mt-4 text-xl text-gray-600">
                Ofrecemos soluciones digitales a medida para impulsar tu negocio
            </p>
        </div>
        
        <div class="grid gap-8 mt-16 md:grid-cols-2 lg:grid-cols-3">
            {% for service in services %}
            <div class="p-6 transition-all bg-white rounded-lg shadow-md hover:shadow-lg animate-slide-in" style="animation-delay: {{ forloop.counter|add:"-1" }}00ms;">
                <div class="inline-flex items-center justify-center w-12 h-12 text-white rounded-lg bg-secondary">
                    <i class="text-xl fa-solid {{ service.icon }}"></i>
                </div>
                <h3 class="mt-4 text-xl font-semibold text-primary">{{ service.title }}</h3>
                <p class="mt-2 text-gray-600">{{ service.description }}</p>
                <a href="#contacto" class="inline-flex items-center mt-4 font-medium text-secondary hover:text-secondary/80">
                    Saber más
                    <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                </a>
            </div>
            {% empty %}
            <!-- Default services if none exist in database -->
            <div class="p-6 transition-all bg-white rounded-lg shadow-md hover:shadow-lg animate-slide-in">
                <div class="inline-flex items-center justify-center w-12 h-12 text-white rounded-lg bg-secondary">
                    <i class="text-xl fa-solid fa-laptop-code"></i>
                </div>
                <h3 class="mt-4 text-xl font-semibold text-primary">Desarrollo Web</h3>
                <p class="mt-2 text-gray-600">Creamos sitios web modernos, responsivos y optimizados para SEO que causan una gran impresión.</p>
                <a href="#contacto" class="inline-flex items-center mt-4 font-medium text-secondary hover:text-secondary/80">
                    Saber más
                    <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                </a>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<!-- Contact Section -->
<section id="contacto" class="py-20">
    <div class="container px-4 mx-auto sm:px-6 lg:px-8">
        <div class="max-w-3xl mx-auto text-center">
            <h2 class="text-3xl font-bold text-primary md:text-4xl font-display">Contáctanos</h2>
            <p class="mt-4 text-xl text-gray-600">
                ¿Tienes un proyecto en mente? Estamos aquí para ayudarte
            </p>
        </div>
        
        <div class="grid gap-8 mt-16 lg:grid-cols-2">
            <!-- Contact Form -->
            <div class="p-6 bg-white rounded-lg shadow-md">
                <h3 class="text-2xl font-semibold text-primary">Envíanos un mensaje</h3>
                <p class="mt-2 text-gray-600">
                    Completa el formulario y nos pondremos en contacto contigo en un plazo de 24 horas.
                </p>
                
                <!-- Form with HTMX -->
                <form hx-post="{% url 'contact' %}" hx-target="#form-response" class="mt-6 space-y-4">
                    {% csrf_token %}
                    <div>
                        <label for="id_name" class="block mb-1 font-medium text-gray-700">Nombre</label>
                        {{ contact_form.name }}
                    </div>
                    <div>
                        <label for="id_email" class="block mb-1 font-medium text-gray-700">Email</label>
                        {{ contact_form.email }}
                    </div>
                    <div>
                        <label for="id_subject" class="block mb-1 font-medium text-gray-700">Asunto</label>
                        {{ contact_form.subject }}
                    </div>
                    <div>
                        <label for="id_message" class="block mb-1 font-medium text-gray-700">Mensaje</label>
                        {{ contact_form.message }}
                    </div>
                    <div>
                        <button type="submit" class="w-full px-6 py-3 font-medium text-white transition-colors rounded-lg bg-secondary hover:bg-secondary/90">
                            Enviar Mensaje
                        </button>
                    </div>
                </form>
                
                <!-- Form Response Display Area -->
                <div id="form-response" class="mt-4"></div>
            </div>
        </div>
    </div>
</section>
{% endblock %}
EOL

# Crear services.html de core
cat > core/templates/core/services.html << EOL
{% extends 'base.html' %}
{% load static %}

{% block title %}Servicios - DevStudio{% endblock %}

{% block content %}
<section class="py-12 bg-primary">
    <div class="container px-4 mx-auto sm:px-6 lg:px-8">
        <div class="max-w-3xl mx-auto text-center">
            <h1 class="text-3xl font-bold text-white md:text-4xl font-display">Nuestros Servicios</h1>
            <p class="mt-4 text-xl text-gray-300">
                Soluciones digitales a medida para impulsar tu negocio
            </p>
        </div>
    </div>
</section>

<section class="py-16">
    <div class="container px-4 mx-auto sm:px-6 lg:px-8">
        <div class="grid gap-12 md:grid-cols-2">
            {% for service in services %}
            <div class="flex">
                <div class="flex-shrink-0 mt-1">
                    <div class="flex items-center justify-center w-12 h-12 text-white rounded-lg bg-secondary">
                        <i class="text-xl fa-solid {{ service.icon }}"></i>
                    </div>
                </div>
                <div class="ml-4">
                    <h3 class="text-xl font-semibold text-primary">{{ service.title }}</h3>
                    <p class="mt-2 text-gray-600">{{ service.description }}</p>
                </div>
            </div>
            {% empty %}
            <div class="md:col-span-2">
                <div class="p-8 text-center">
                    <p class="text-gray-600">No hay servicios disponibles en este momento.</p>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endblock %}
EOL

# Crear plantillas para la aplicación portfolio
mkdir -p portfolio/templates/portfolio
echo "Creando plantillas para la aplicación portfolio..."

# Crear project_list.html
cat > portfolio/templates/portfolio/project_list.html << EOL
{% extends 'base.html' %}
{% load static %}

{% block title %}Portfolio - DevStudio{% endblock %}

{% block content %}
<section class="py-12 bg-primary">
    <div class="container px-4 mx-auto sm:px-6 lg:px-8">
        <div class="max-w-3xl mx-auto text-center">
            <h1 class="text-3xl font-bold text-white md:text-4xl font-display">Nuestro Portfolio</h1>
            <p class="mt-4 text-xl text-gray-300">
                Descubre nuestros proyectos y casos de éxito
            </p>
        </div>
    </div>
</section>

<section class="py-16">
    <div class="container px-4 mx-auto sm:px-6 lg:px-8">
        <!-- Filter by category -->
        <div class="flex flex-wrap items-center justify-center gap-4 mb-12">
            <a href="{% url 'project_list' %}" class="px-4 py-2 transition-colors rounded-full {% if not request.GET.category %}bg-secondary text-white{% else %}bg-gray-100 text-gray-700 hover:bg-gray-200{% endif %}">
                Todos
            </a>
            
            {% for category in categories %}
            <a href="{% url 'project_list' %}?category={{ category.slug }}" class="px-4 py-2 transition-colors rounded-full {% if request.GET.category == category.slug %}bg-secondary text-white{% else %}bg-gray-100 text-gray-700 hover:bg-gray-200{% endif %}">
                {{ category.name }}
            </a>
            {% endfor %}
        </div>
        
        <!-- Projects grid -->
        <div class="grid gap-8 mt-8 md:grid-cols-2 lg:grid-cols-3">
            {% for project in projects %}
            <div class="overflow-hidden transition-all bg-white rounded-lg shadow-md hover:shadow-lg">
                <a href="{% url 'project_detail' project.slug %}">
                    <img src="{{ project.image.url }}" alt="{{ project.title }}" class="object-cover w-full h-48">
                </a>
                <div class="p-6">
                    <span class="px-3 py-1 text-xs font-medium text-white rounded-full bg-secondary">{{ project.category.name }}</span>
                    <h3 class="mt-2 text-xl font-semibold text-primary">{{ project.title }}</h3>
                    <p class="mt-2 text-gray-600">{{ project.short_description }}</p>
                    <a href="{% url 'project_detail' project.slug %}" class="inline-flex items-center mt-4 font-medium text-secondary hover:text-secondary/80">
                        Ver detalles
                        <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                    </a>
                </div>
            </div>
            {% empty %}
            <div class="col-span-full">
                <div class="p-8 text-center text-gray-600">
                    <h3 class="mt-4 text-xl font-semibold">No hay proyectos disponibles</h3>
                    <p class="mt-2">No se encontraron proyectos en esta categoría</p>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endblock %}
EOL

# Crear project_detail.html
