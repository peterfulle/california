from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.db.models import Q, Count, Sum, Avg
from django.db import models
from django.utils import timezone
from .models import (
    Contact, Industry, UserProfile, Startup, InvestorProfile, 
    Event, EventRegistration, FounderProfile, EventComment, EventAttendance
)
from .startup_forms import StartupForm

def home(request):
    """Homepage con estadísticas del ecosistema"""
    context = {
        'total_startups': Startup.objects.filter(is_public=True).count() or 25,
        'total_investors': InvestorProfile.objects.filter(is_active=True).count() or 15,
        'total_advisors': UserProfile.objects.filter(user_type='advisor').count() or 8,
        'featured_startups': Startup.objects.filter(featured=True, is_public=True)[:6],
        'featured_investors': InvestorProfile.objects.filter(featured=True, is_active=True)[:6],
        'upcoming_events': Event.objects.filter(status='published')[:3],
        'total_funding': '15M+'  # Hardcoded for now
    }
    return render(request, 'core/home.html', context)

def register(request):
    """Registro de nuevos usuarios con selección de tipo"""
    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_type = request.POST.get('user_type')
        
        # Validaciones básicas
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registration/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
            return render(request, 'registration/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado.')
            return render(request, 'registration/register.html')
        
        try:
            # Crear usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            
            # Crear perfil de usuario
            UserProfile.objects.create(
                user=user,
                user_type=user_type
            )
            
            # Login automático
            user = authenticate(username=username, password=password1)
            login(request, user)
            
            messages.success(request, '¡Cuenta creada exitosamente! Completa tu perfil.')
            return redirect('core:dashboard')
            
        except Exception as e:
            messages.error(request, f'Error al crear la cuenta: {str(e)}')
    
    return render(request, 'registration/register.html')

def user_login(request):
    """Vista de login personalizada"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'core:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'registration/login.html')

def user_logout(request):
    """Cerrar sesión"""
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente.')
    return redirect('core:home')

@login_required
def dashboard(request):
    """Dashboard principal estilo Crunchbase con datos dinámicos"""
    import logging
    logger = logging.getLogger('core')
    
    logger.info(f"Dashboard access attempt by user: {request.user.username}")
    
    try:
        profile = UserProfile.objects.get(user=request.user)
        logger.info(f"Profile found for user {request.user.username}: {profile.user_type}")
    except UserProfile.DoesNotExist:
        logger.info(f"Creating new profile for user: {request.user.username}")
        # Crear perfil si no existe
        profile = UserProfile.objects.create(
            user=request.user,
            user_type='community'  # Default
        )
        logger.info(f"Profile created successfully for user: {request.user.username}")
    
    try:
        logger.info("Starting to gather ecosystem statistics...")
        # Estadísticas globales del ecosistema
        total_startups = Startup.objects.filter(is_public=True).count()
        logger.info(f"Total startups counted: {total_startups}")
        
        total_investors = InvestorProfile.objects.filter(is_active=True).count()
        logger.info(f"Total investors counted: {total_investors}")
        total_funding = Startup.objects.filter(is_public=True).aggregate(
            total=Sum('total_funding_raised')
        )['total'] or 0
        logger.info(f"Total funding calculated: {total_funding}")
        
        total_seeking = Startup.objects.filter(
            is_fundraising=True, 
            is_public=True
        ).aggregate(total=Sum('seeking_amount'))['total'] or 0
        logger.info(f"Total seeking calculated: {total_seeking}")
        
        # Actividad reciente
        logger.info("Gathering recent activity data...")
        recent_startups = Startup.objects.filter(is_public=True).order_by('-created_at')[:6]
        logger.info(f"Recent startups count: {recent_startups.count()}")
        
        recent_funding = Startup.objects.filter(
            is_public=True,
            total_funding_raised__gt=0
        ).order_by('-updated_at')[:5]
        logger.info(f"Recent funding count: {recent_funding.count()}")
        
        trending_industries = Industry.objects.annotate(
            startup_count=Count('startup')
        ).order_by('-startup_count')[:5]
        logger.info(f"Trending industries count: {trending_industries.count()}")
        
        context = {
            'profile': profile,
            'user_type': profile.user_type,
            # Estadísticas globales
            'ecosystem_stats': {
                'total_startups': total_startups,
                'total_investors': total_investors,
                'total_funding': total_funding,
                'total_seeking': total_seeking,
                'active_fundraising': Startup.objects.filter(is_fundraising=True, is_public=True).count(),
                'new_this_month': Startup.objects.filter(
                    created_at__month=timezone.now().month,
                    is_public=True
                ).count()
            },
            # Actividad reciente
            'recent_activity': {
                'recent_startups': recent_startups,
                'recent_funding': recent_funding,
                'trending_industries': trending_industries,
                'upcoming_events': Event.objects.filter(
                    status='published',
                    start_datetime__gte=timezone.now()
                ).order_by('start_datetime')[:3]
            }
        }
    
        
        if profile.user_type == 'founder':
            # Dashboard específico para founders
            try:
                startup = Startup.objects.get(founder=profile)
                # Métricas del startup
                context.update({
                    'startup': startup,
                    'startup_metrics': {
                        'funding_progress': (startup.total_funding_raised / startup.seeking_amount * 100) if startup.seeking_amount else 0,
                        'time_since_founded': (timezone.now().date() - startup.founded_date).days if startup.founded_date else 0,
                        'years_since_founded': round((timezone.now().date() - startup.founded_date).days / 365.25, 1) if startup.founded_date else 0,
                        'industry_rank': Startup.objects.filter(
                            industry=startup.industry,
                            total_funding_raised__gte=startup.total_funding_raised
                        ).count() if startup.industry else 0
                    },
                    'recommended_investors': InvestorProfile.objects.filter(
                        is_accepting_pitches=True,
                        is_active=True,
                        geographic_focus__in=['global', 'local']
                    ).order_by('-fund_size')[:8],
                    'similar_startups': Startup.objects.filter(
                        industry=startup.industry,
                        stage=startup.stage,
                        is_public=True
                    ).exclude(id=startup.id)[:5] if startup.industry else []
                })
            except Startup.DoesNotExist:
                context['needs_startup'] = True
                
        elif profile.user_type == 'investor':
            # Dashboard específico para inversores
            try:
                investor = InvestorProfile.objects.get(user=request.user)
                # Deal flow y oportunidades
                relevant_startups = Startup.objects.filter(
                    is_fundraising=True,
                    is_public=True
                )
                
                # Obtener investment_stages con seguridad
                investment_stages = investor.investment_stages if investor.investment_stages else []
                
                if investment_stages:
                    relevant_startups = relevant_startups.filter(
                        stage__in=investment_stages
                    )
                
                context.update({
                    'investor': investor,
                    'deal_flow': {
                        'new_opportunities': relevant_startups.order_by('-created_at')[:8],
                        'matching_stage': relevant_startups.filter(
                            stage__in=investment_stages
                        ).count() if investment_stages else relevant_startups.count(),
                        'in_range': relevant_startups.filter(
                            seeking_amount__gte=investor.min_investment or 0,
                            seeking_amount__lte=investor.max_investment or float('inf')
                        ).count() if (investor.min_investment or investor.max_investment) else 0
                    },
                    'market_insights': {
                        'avg_valuation': Startup.objects.filter(
                            is_public=True,
                            valuation__isnull=False
                        ).aggregate(avg=Avg('valuation'))['avg'] or 0,
                        'hot_industries': trending_industries
                    }
                })
            except InvestorProfile.DoesNotExist:
                context['needs_investor_profile'] = True
                
        else:  # advisor o community
            # Dashboard para advisors y community members
            context.update({
                'discovery': {
                    'featured_startups': Startup.objects.filter(
                        featured=True,
                        is_public=True
                    ).order_by('-created_at')[:6],
                    'top_funded': Startup.objects.filter(
                        is_public=True,
                        total_funding_raised__gt=0
                    ).order_by('-total_funding_raised')[:5],
                    'recently_launched': recent_startups
                },
                'network_opportunities': {
                    'active_investors': InvestorProfile.objects.filter(
                        is_active=True,
                        is_accepting_pitches=True
                    ).order_by('-fund_size')[:6],
                    'growing_startups': Startup.objects.filter(
                        is_public=True,
                        stage__in=['growth', 'scale']
                    ).order_by('-employees_count')[:6]
                }
            })
        
        logger.info("Successfully gathered all dashboard data, rendering template...")
        return render(request, 'core/dashboard_new.html', context)
        
    except Exception as e:
        logger.error(f"Error in dashboard view: {str(e)}", exc_info=True)
        # En caso de error, crear un contexto básico de fallback
        context = {
            'profile': profile,
            'user_type': profile.user_type,
            'error_message': 'Error cargando el dashboard. Contacta soporte si persiste.',
            'ecosystem_stats': {
                'total_startups': 25,
                'total_investors': 15,
                'total_funding': 0,
                'total_seeking': 0,
                'active_fundraising': 5,
                'new_this_month': 3
            }
        }
        return render(request, 'core/dashboard_new.html', context)@login_required
def investor_create(request):
    if not request.user.is_authenticated:
        return redirect('core:login')
    
    if request.user.profile.user_type != 'investor':
        return redirect('core:dashboard')
    
    # Check if user already has an investor profile
    try:
        investor_profile = InvestorProfile.objects.get(user=request.user)
        return redirect('core:dashboard')  # Already has profile
    except InvestorProfile.DoesNotExist:
        pass
    
    if request.method == 'POST':
        # Get form data
        fund_name = request.POST.get('fund_name')
        investor_type = request.POST.get('investor_type')
        fund_size = request.POST.get('fund_size')
        investment_stage = request.POST.get('investment_stage')
        investment_range_min = request.POST.get('investment_range_min')
        investment_range_max = request.POST.get('investment_range_max')
        bio = request.POST.get('bio')
        website = request.POST.get('website')
        linkedin_profile = request.POST.get('linkedin_profile')
        location = request.POST.get('location')
        investment_thesis = request.POST.get('investment_thesis')
        geographic_focus = request.POST.get('geographic_focus')
        portfolio_companies_count = request.POST.get('portfolio_companies_count')
        years_of_experience = request.POST.get('years_of_experience')
        notable_investments = request.POST.get('notable_investments')
        is_actively_investing = 'is_actively_investing' in request.POST
        industries_of_interest = request.POST.getlist('industries_of_interest')
        
        # Create investor profile
        investor_profile = InvestorProfile.objects.create(
            user=request.user,
            fund_name=fund_name if fund_name else None,
            investor_type=investor_type if investor_type else None,
            fund_size=float(fund_size) if fund_size else None,
            investment_stage=investment_stage if investment_stage else None,
            investment_range_min=float(investment_range_min) if investment_range_min else None,
            investment_range_max=float(investment_range_max) if investment_range_max else None,
            bio=bio if bio else None,
            website=website if website else None,
            linkedin_profile=linkedin_profile if linkedin_profile else None,
            location=location if location else None,
            investment_thesis=investment_thesis if investment_thesis else None,
            geographic_focus=geographic_focus if geographic_focus else None,
            portfolio_companies_count=int(portfolio_companies_count) if portfolio_companies_count else None,
            years_of_experience=int(years_of_experience) if years_of_experience else None,
            notable_investments=notable_investments if notable_investments else None,
            is_actively_investing=is_actively_investing
        )
        
        # Add industries of interest
        if industries_of_interest:
            for industry_id in industries_of_interest:
                try:
                    industry = Industry.objects.get(id=industry_id)
                    investor_profile.industries_of_interest.add(industry)
                except Industry.DoesNotExist:
                    pass
        
        return redirect('core:dashboard')
    
    # Get industries for the form
    industries = Industry.objects.all()
    
    context = {
        'industries': industries,
    }
    
    return render(request, 'core/investor_create.html', context)


def startup_directory(request):
    search_query = request.GET.get('search', '')
    startups = Startup.objects.all()
    
    if search_query:
        startups = startups.filter(
            Q(company_name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tagline__icontains=search_query) |
            Q(industry__name__icontains=search_query)
        )
    
    startups = startups.order_by('-created_at')
    
    context = {
        'startups': startups,
        'search_query': search_query,
    }
    
    return render(request, 'core/startup_directory.html', context)


def startup_detail(request, startup_id):
    startup = get_object_or_404(Startup, id=startup_id)
    
    context = {
        'startup': startup,
    }
    
    return render(request, 'core/startup_detail.html', context)


def investor_directory(request):
    search_query = request.GET.get('search', '')
    investors = InvestorProfile.objects.all()
    
    if search_query:
        investors = investors.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(fund_name__icontains=search_query) |
            Q(bio__icontains=search_query) |
            Q(investment_thesis__icontains=search_query) |
            Q(industries_of_interest__name__icontains=search_query)
        ).distinct()
    
    investors = investors.order_by('-created_at')
    
    context = {
        'investors': investors,
        'search_query': search_query,
    }
    
    return render(request, 'core/investor_directory.html', context)


def investor_detail(request, investor_id):
    investor = get_object_or_404(InvestorProfile, id=investor_id)
    
    context = {
        'investor': investor,
    }
    
    return render(request, 'core/investor_detail.html', context)

def startup_directory(request):
    """Directorio público de startups con scores dinámicos"""
    startups = Startup.objects.filter(is_public=True).order_by('-created_at')
    
    # Filtros básicos
    search_query = request.GET.get('search')
    if search_query:
        startups = startups.filter(
            Q(company_name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tagline__icontains=search_query)
        )
    
    # Agregar scores calculados dinámicamente a cada startup
    startups_with_scores = []
    for startup in startups:
        startup_data = {
            'startup': startup,
            'growth_score': startup.calculate_growth_score(),
            'heat_score': startup.calculate_heat_score(),
            'cb_rank': startup.calculate_cb_rank(),
            'ranking_percentile': startup.get_ranking_percentile()
        }
        startups_with_scores.append(startup_data)
    
    # Ordenar por Growth Score descendente por defecto
    sort_by = request.GET.get('sort', 'growth_score')
    reverse = request.GET.get('order', 'desc') == 'desc'
    
    if sort_by == 'growth_score':
        startups_with_scores.sort(key=lambda x: x['growth_score'], reverse=reverse)
    elif sort_by == 'heat_score':
        startups_with_scores.sort(key=lambda x: x['heat_score'], reverse=reverse)
    elif sort_by == 'cb_rank':
        startups_with_scores.sort(key=lambda x: x['cb_rank'], reverse=not reverse)  # Rank más bajo = mejor
    elif sort_by == 'funding':
        startups_with_scores.sort(key=lambda x: x['startup'].total_funding_raised or 0, reverse=reverse)
    
    context = {
        'startups_with_scores': startups_with_scores,
        'search_query': search_query,
        'sort_by': sort_by,
        'order': request.GET.get('order', 'desc')
    }
    
    return render(request, 'core/startup_directory.html', context)

def investor_directory(request):
    """Directorio público de inversores"""
    investors = InvestorProfile.objects.filter(is_active=True).order_by('-created_at')
    
    # Filtros básicos
    search_query = request.GET.get('search')
    if search_query:
        investors = investors.filter(
            Q(fund_name__icontains=search_query) |
            Q(thesis__icontains=search_query)
        )
    
    context = {
        'investors': investors,
        'search_query': search_query
    }
    
    return render(request, 'core/investor_directory.html', context)

def startup_detail(request, startup_id):
    """Vista detallada de startup"""
    startup = get_object_or_404(Startup, id=startup_id, is_public=True)
    
    context = {
        'startup': startup,
        'can_edit': request.user.is_authenticated and startup.founder.user == request.user
    }
    
    return render(request, 'core/startup_detail.html', context)

def contact_view(request):
    """Vista de contacto"""
    if request.method == 'POST':
        try:
            Contact.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                subject=request.POST.get('subject'),
                message=request.POST.get('message')
            )
            return HttpResponse(
                '<div class="p-4 rounded-lg bg-green-500/20 border border-green-500/30">'
                '<p class="text-white"><i class="fa-solid fa-check-circle mr-2 text-green-400"></i> '
                'Mensaje enviado exitosamente. Te contactaremos pronto.</p>'
                '</div>'
            )
        except Exception as e:
            return HttpResponse(
                '<div class="p-4 rounded-lg bg-red-500/20 border border-red-500/30">'
                '<p class="text-white"><i class="fa-solid fa-exclamation-circle mr-2 text-red-400"></i> '
                f'Error al enviar mensaje: {str(e)}</p>'
                '</div>'
            )
    
    return render(request, 'core/contact.html')

def events_list(request):
    """Lista de eventos y creación de nuevos eventos"""
    if request.method == 'POST' and request.user.is_authenticated:
        # Crear nuevo evento
        try:
            # Validar datos requeridos
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            event_type = request.POST.get('event_type', '').strip()
            start_datetime = request.POST.get('start_datetime', '').strip()
            max_attendees = request.POST.get('max_attendees', '50')
            is_virtual = request.POST.get('is_virtual') == 'true'
            
            # Validaciones básicas
            if not title:
                raise ValueError('El título es requerido')
            if not description:
                raise ValueError('La descripción es requerida')
            if not event_type:
                raise ValueError('El tipo de evento es requerido')
            if not start_datetime:
                raise ValueError('La fecha y hora son requeridas')
            
            # Validar capacidad
            try:
                max_attendees = int(max_attendees)
                if max_attendees < 1:
                    raise ValueError('La capacidad debe ser al menos 1')
            except (ValueError, TypeError):
                max_attendees = 50
            
            # Validar ubicación según modalidad
            location = ''
            meeting_url = ''
            
            if is_virtual:
                meeting_url = request.POST.get('meeting_url', '').strip()
                if not meeting_url:
                    raise ValueError('La URL del evento virtual es requerida')
            else:
                location = request.POST.get('location', '').strip()
                if not location:
                    raise ValueError('La ubicación es requerida para eventos presenciales')
            
            # Crear el evento
            event = Event.objects.create(
                title=title,
                description=description,
                event_type=event_type,
                start_datetime=start_datetime,
                max_attendees=max_attendees,
                is_virtual=is_virtual,
                location=location,
                meeting_url=meeting_url,
                organizer=request.user,
                status='published'
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'event_id': event.id,
                    'message': f'Evento "{event.title}" creado exitosamente!'
                })
            else:
                messages.success(request, f'Evento "{event.title}" creado exitosamente!')
                return redirect('core:events_list')
                
        except ValueError as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
            else:
                messages.error(request, f'Error de validación: {str(e)}')
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': f'Error interno: {str(e)}'})
            else:
                messages.error(request, f'Error al crear el evento: {str(e)}')
    
    # Lista de eventos
    events = Event.objects.filter(status='published').order_by('start_datetime')
    
    context = {
        'events': events
    }
    
    return render(request, 'core/events.html', context)

@login_required
def create_startup(request):
    """Vista para crear perfil de startup con debugging avanzado"""
    import logging
    logger = logging.getLogger(__name__)
    
    # Print simple para verificar que la vista se ejecuta
    print(f"\n{'='*50}")
    print(f"CREATE STARTUP VIEW CALLED")
    print(f"Method: {request.method}")
    print(f"User: {request.user}")
    print(f"{'='*50}\n")
    
    logger.info(f"=== CREATE STARTUP REQUEST START ===")
    logger.info(f"User: {request.user}")
    logger.info(f"Method: {request.method}")
    logger.info(f"POST data: {request.POST}")
    logger.info(f"FILES data: {request.FILES}")
    
    # Verificar que el usuario sea fundador
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        logger.info(f"User profile found: {user_profile}, type: {user_profile.user_type}")
        
        if user_profile.user_type != 'founder':
            logger.warning(f"User {request.user} is not a founder, redirecting")
            messages.error(request, 'Only founders can create startup profiles.')
            return redirect('core:dashboard')
    except UserProfile.DoesNotExist:
        logger.info(f"Creating new founder profile for user {request.user}")
        # Si no existe perfil, crear uno como founder
        user_profile = UserProfile.objects.create(
            user=request.user,
            user_type='founder'
        )
    
    # Verificar si ya tiene una startup
    existing_startup = Startup.objects.filter(founder=user_profile).first()
    if existing_startup:
        logger.info(f"User already has startup: {existing_startup}")
        messages.info(request, 'You already have a registered startup.')
        return redirect('core:startup_profile', startup_id=existing_startup.id)
    
    if request.method == 'POST':
        logger.info("=== PROCESSING POST REQUEST ===")
        logger.info(f"POST data keys: {list(request.POST.keys())}")
        
        # Log todos los datos del POST
        for key, value in request.POST.items():
            logger.info(f"POST[{key}] = {value}")
        
        # Handle cropped logo data
        cropped_logo_data = request.POST.get('cropped_logo_data')
        
        form = StartupForm(request.POST, request.FILES)
        logger.info(f"Form created, checking validity...")
        
        if form.is_valid():
            logger.info("Form is valid, attempting to save...")
            try:
                startup = form.save(commit=False)
                logger.info(f"Startup object created: {startup}")
                
                startup.founder = user_profile
                logger.info(f"Founder assigned: {user_profile}")
                
                # Process cropped logo if available
                if cropped_logo_data and cropped_logo_data.startswith('data:image'):
                    logger.info("Processing cropped logo data...")
                    
                    import base64
                    import tempfile
                    from django.core.files.base import ContentFile
                    from django.core.files.storage import default_storage
                    import uuid
                    
                    try:
                        # Extract base64 data
                        format, imgstr = cropped_logo_data.split(';base64,')
                        ext = format.split('/')[-1]
                        
                        # Decode base64 data
                        data = ContentFile(base64.b64decode(imgstr))
                        
                        # Generate unique filename
                        filename = f"startup_logos/logo_{uuid.uuid4().hex}.{ext}"
                        
                        # Save the cropped logo
                        saved_path = default_storage.save(filename, data)
                        startup.logo = saved_path
                        
                        logger.info(f"Cropped logo saved to: {saved_path}")
                        
                    except Exception as e:
                        logger.error(f"Error processing cropped logo: {str(e)}")
                        # Continue without cropped logo
                
                startup.save()
                logger.info(f"Startup saved successfully with ID: {startup.id}")
                
                messages.success(request, '🚀 Startup profile created successfully!')
                
                redirect_url = f'/startup/{startup.id}/'
                logger.info(f"Redirecting to: {redirect_url}")
                return redirect('core:startup_profile', startup_id=startup.id)
                
            except Exception as e:
                logger.error(f"ERROR saving startup: {str(e)}", exc_info=True)
                messages.error(request, f'Error creating startup: {str(e)}')
        else:
            logger.error("Form is NOT valid")
            logger.error(f"Form errors: {form.errors}")
            
            # Log cada error individualmente
            for field, errors in form.errors.items():
                logger.error(f"Field '{field}' errors: {errors}")
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        logger.info("Creating empty form for GET request")
        form = StartupForm()
    
    context = {
        'form': form,
        'industries': Industry.objects.all(),
        'form_errors': form.errors if 'form' in locals() else {}
    }
    
    logger.info(f"Rendering template with context keys: {list(context.keys())}")
    logger.info("=== CREATE STARTUP REQUEST END ===")
    
    return render(request, 'core/create_startup.html', context)

@login_required
def startup_profile(request, startup_id):
    """Vista del perfil detallado de la startup estilo Crunchbase"""
    startup = get_object_or_404(Startup, id=startup_id)
    
    # Calcular métricas
    years_since_founded = None
    if startup.founded_date:
        years_since_founded = round((timezone.now().date() - startup.founded_date).days / 365.25, 1)
    
    # Calcular scores usando algoritmos dinámicos basados en datos reales
    growth_score = startup.calculate_growth_score()  # Calculado basado en varios factores
    heat_score = startup.calculate_heat_score()      # Basado en actividad, métricas, etc.
    cb_rank = startup.calculate_cb_rank()           # Ranking global calculado
    ranking_percentile = startup.get_ranking_percentile()  # Percentil del ranking
    
    # Obtener métricas adicionales de los nuevos métodos
    performance_grade = startup.get_performance_grade()
    market_position = startup.get_market_position()
    formatted_funding = startup.format_funding_amount()
    formatted_revenue = startup.format_revenue_amount()
    
    # Obtener datos relacionados - buscar otros fundadores de la misma startup
    team_members = UserProfile.objects.filter(
        user_type='founder',
        startup__company_name=startup.company_name
    ).exclude(id=startup.founder.id)
    
    # Datos de financiación (simulated for now)
    funding_rounds = [
        {
            'date': 'Jul 10, 2025',
            'round_type': 'Series A',
            'amount': startup.total_funding_raised if startup.total_funding_raised > 0 else None,
            'investors': []
        }
    ]
    
    # Noticias recientes (simulated)
    recent_news = [
        {
            'date': 'Jul 25, 2025',
            'title': f'Explore the 7 Top {startup.industry.name if startup.industry else "Tech"} Companies & Startups to Watch in 2026',
            'publisher': 'StartUs Insights',
            'url': 'www.startus-insights.com/innovators-guide/neuro...'
        },
        {
            'date': 'May 15, 2025',
            'title': f'{startup.company_name}: Breakthrough Innovation Moving From the Lab to Your Business',
            'publisher': 'TechCrunch',
            'url': 'techcrunch.com/posts/breakthrough-innovation-...'
        }
    ]
    
    context = {
        'startup': startup,
        'years_since_founded': years_since_founded,
        'growth_score': growth_score,
        'heat_score': heat_score,
        'cb_rank': cb_rank,
        'ranking_percentile': ranking_percentile,
        'performance_grade': performance_grade,
        'market_position': market_position,
        'formatted_funding': formatted_funding,
        'formatted_revenue': formatted_revenue,
        'team_members': team_members,
        'funding_rounds': funding_rounds,
        'recent_news': recent_news,
        'total_funding_rounds': len(funding_rounds),
        'employee_count_display': startup.employees_count or '1-10',
        'is_founder': request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile == startup.founder,
    }
    
    # Agregar datos de secciones privadas si el usuario tiene acceso
    if request.user.is_authenticated:
        # Importar modelos de secciones privadas
        from .models import StartupFinancials, StartupPeople, StartupNews, StartupTechnology
        
        # Verificar si el usuario tiene acceso a información privada
        user_has_access = startup.is_investor_approved_for_access(request.user)
        context['user_has_private_access'] = user_has_access
        
        if user_has_access:
            # Obtener datos de secciones privadas
            try:
                startup_financials = StartupFinancials.objects.get(startup=startup)
                context['startup_financials'] = startup_financials
            except StartupFinancials.DoesNotExist:
                context['startup_financials'] = None
            
            try:
                startup_people = StartupPeople.objects.get(startup=startup)
                context['startup_people'] = startup_people
            except StartupPeople.DoesNotExist:
                context['startup_people'] = None
                
            try:
                startup_news = StartupNews.objects.get(startup=startup)
                context['startup_news'] = startup_news
            except StartupNews.DoesNotExist:
                context['startup_news'] = None
                
            try:
                startup_technology = StartupTechnology.objects.get(startup=startup)
                context['startup_technology'] = startup_technology
            except StartupTechnology.DoesNotExist:
                context['startup_technology'] = None
    else:
        context['user_has_private_access'] = False
    
    return render(request, 'core/startup_profile.html', context)


# ===== SISTEMA DE INFORMACIÓN PRIVADA =====

@login_required
def request_startup_access(request, startup_id):
    """Vista para que los inversionistas soliciten acceso a información privada"""
    startup = get_object_or_404(Startup, id=startup_id)
    
    # Verificar que el usuario sea un inversionista
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'investor':
        messages.error(request, 'Solo los inversionistas pueden solicitar acceso a información privada.')
        return redirect('core:startup_profile', pk=startup_id)
    
    # Verificar si ya existe una solicitud
    from .models import InvestorAccessRequest
    existing_request = InvestorAccessRequest.objects.filter(
        investor=request.user.profile,
        startup=startup
    ).first()
    
    if request.method == 'POST':
        if existing_request and existing_request.status == 'pending':
            messages.info(request, 'Ya tienes una solicitud pendiente para esta startup.')
            return redirect('core:startup_profile', pk=startup_id)
        
        message = request.POST.get('message', '').strip()
        if not message:
            messages.error(request, 'Debes incluir un mensaje explicando tu interés.')
            return render(request, 'core/request_access.html', {'startup': startup})
        
        # Crear o actualizar la solicitud
        if existing_request:
            existing_request.message = message
            existing_request.status = 'pending'
            existing_request.requested_at = timezone.now()
            existing_request.save()
        else:
            InvestorAccessRequest.objects.create(
                investor=request.user.profile,
                startup=startup,
                message=message
            )
        
        messages.success(request, f'Tu solicitud de acceso a {startup.company_name} ha sido enviada.')
        return redirect('core:startup_profile', pk=startup_id)
    
    context = {
        'startup': startup,
        'existing_request': existing_request
    }
    return render(request, 'core/request_access.html', context)


@login_required
def startup_private_section(request, startup_id, section):
    """Vista para acceder a secciones privadas de información"""
    startup = get_object_or_404(Startup, id=startup_id)
    valid_sections = ['financials', 'people', 'news', 'technology']
    
    if section not in valid_sections:
        messages.error(request, 'Sección no válida.')
        return redirect('core:startup_profile', startup_id)
    
    # Verificar permisos de acceso
    has_access = False
    is_founder = False
    
    if hasattr(request.user, 'profile'):
        user_profile = request.user.profile
        
        # El fundador siempre tiene acceso
        if user_profile == startup.founder:
            has_access = True
            is_founder = True
        
        # Verificar si el inversionista tiene acceso aprobado
        elif user_profile.user_type == 'investor':
            from .models import InvestorAccessRequest
            access_request = InvestorAccessRequest.objects.filter(
                investor=user_profile,
                startup=startup,
                status='approved'
            ).first()
            
            if access_request and access_request.is_active:
                has_access = True
    
    if not has_access:
        messages.error(request, 'No tienes acceso a esta información privada.')
        return redirect('core:startup_profile', startup_id)
    
    # Obtener o crear la información privada según la sección
    private_data = None
    
    if section == 'financials':
        from .models import StartupFinancials
        private_data, created = StartupFinancials.objects.get_or_create(startup=startup)
        
        # Manejar POST para guardar información financiera
        if request.method == 'POST' and is_founder:
            # Actualizar campos financieros
            if 'arr_current' in request.POST:
                private_data.arr_current = request.POST.get('arr_current') or None
            if 'mrr_growth_rate' in request.POST:
                private_data.mrr_growth_rate = request.POST.get('mrr_growth_rate') or None
            if 'revenue_forecast_12m' in request.POST:
                private_data.revenue_forecast_12m = request.POST.get('revenue_forecast_12m') or None
            if 'revenue_forecast_24m' in request.POST:
                private_data.revenue_forecast_24m = request.POST.get('revenue_forecast_24m') or None
            if 'cac_payback_period' in request.POST:
                private_data.cac_payback_period = request.POST.get('cac_payback_period') or None
            if 'gross_margin' in request.POST:
                private_data.gross_margin = request.POST.get('gross_margin') or None
            if 'net_revenue_retention' in request.POST:
                private_data.net_revenue_retention = request.POST.get('net_revenue_retention') or None
            if 'cash_position' in request.POST:
                private_data.cash_position = request.POST.get('cash_position') or None
            if 'burn_rate_detailed' in request.POST:
                private_data.burn_rate_detailed = request.POST.get('burn_rate_detailed') or None
            if 'runway_calculation' in request.POST:
                private_data.runway_calculation = request.POST.get('runway_calculation') or ''
            if 'current_round_details' in request.POST:
                private_data.current_round_details = request.POST.get('current_round_details') or ''
            if 'previous_investors' in request.POST:
                private_data.previous_investors = request.POST.get('previous_investors') or ''
            if 'financial_statements_url' in request.POST:
                private_data.financial_statements_url = request.POST.get('financial_statements_url') or ''
            if 'cap_table_url' in request.POST:
                private_data.cap_table_url = request.POST.get('cap_table_url') or ''
            if 'business_plan_url' in request.POST:
                private_data.business_plan_url = request.POST.get('business_plan_url') or ''
            
            private_data.save()
            messages.success(request, 'Información financiera actualizada exitosamente.')
            return redirect('core:startup_private_section', startup_id, 'financials')
    
    elif section == 'people':
        from .models import StartupPeople
        private_data, created = StartupPeople.objects.get_or_create(startup=startup)
        
        # Manejar POST para información de personas
        if request.method == 'POST' and is_founder:
            # Información del equipo
            if 'total_employees' in request.POST:
                private_data.total_employees = request.POST.get('total_employees') or 0
            if 'founders_count' in request.POST:
                private_data.founders_count = request.POST.get('founders_count') or 0
            if 'tech_team_size' in request.POST:
                private_data.tech_team_size = request.POST.get('tech_team_size') or 0
            if 'leadership_team_size' in request.POST:
                private_data.leadership_team_size = request.POST.get('leadership_team_size') or 0
            
            # Miembros del equipo dinámicos
            team_member_names = request.POST.getlist('team_member_name[]')
            team_member_positions = request.POST.getlist('team_member_position[]')
            team_member_emails = request.POST.getlist('team_member_email[]')
            team_member_equity = request.POST.getlist('team_member_equity[]')
            team_member_bios = request.POST.getlist('team_member_bio[]')
            team_member_linkedin = request.POST.getlist('team_member_linkedin[]')
            
            # Construir lista de miembros del equipo
            team_members = []
            for i in range(len(team_member_names)):
                if team_member_names[i]:  # Solo si hay nombre
                    team_members.append({
                        'name': team_member_names[i],
                        'position': team_member_positions[i] if i < len(team_member_positions) else '',
                        'email': team_member_emails[i] if i < len(team_member_emails) else '',
                        'equity': team_member_equity[i] if i < len(team_member_equity) else '0',
                        'bio': team_member_bios[i] if i < len(team_member_bios) else '',
                        'linkedin': team_member_linkedin[i] if i < len(team_member_linkedin) else '',
                    })
            
            if team_members:
                private_data.founders_detailed_bios = {'team_members': team_members}
            
            # Equity distribution
            founders_equity = request.POST.get('founders_equity_total', '70.0')
            esop_pool = request.POST.get('esop_pool_percentage', '15.0')
            esop_allocated = request.POST.get('esop_allocated', '5.0')
            investor_equity = request.POST.get('investor_equity_total', '15.0')
            
            private_data.equity_distribution = {
                'founders_equity_total': founders_equity,
                'esop_pool_percentage': esop_pool,
                'esop_allocated': esop_allocated,
                'investor_equity_total': investor_equity
            }
            
            # Cultura corporativa
            if 'company_mission' in request.POST:
                private_data.company_mission = request.POST.get('company_mission', '')
            if 'company_vision' in request.POST:
                private_data.company_vision = request.POST.get('company_vision', '')
            if 'core_values' in request.POST:
                private_data.company_values = request.POST.get('core_values', '')
            if 'work_mode' in request.POST:
                private_data.work_mode = request.POST.get('work_mode', 'hybrid')
            if 'main_location' in request.POST:
                private_data.main_location = request.POST.get('main_location', '')
            if 'employee_benefits' in request.POST:
                private_data.employee_benefits = {'benefits_text': request.POST.get('employee_benefits', '')}
            if 'diversity_initiatives' in request.POST:
                private_data.diversity_initiatives = request.POST.get('diversity_initiatives', '')
            
            # Plan de contratación
            if 'hiring_budget_annual' in request.POST:
                private_data.hiring_budget_annual = request.POST.get('hiring_budget_annual', '')
            if 'hiring_priority_1' in request.POST:
                private_data.hiring_priority_1 = request.POST.get('hiring_priority_1', '')
            if 'recruitment_strategy' in request.POST:
                private_data.recruitment_strategy = request.POST.get('recruitment_strategy', '')
            
            hiring_plan = {
                'budget_annual': request.POST.get('hiring_budget_annual', ''),
                'priority_1': request.POST.get('hiring_priority_1', ''),
                'recruitment_strategy': request.POST.get('recruitment_strategy', '')
            }
            private_data.hiring_plan_12m = hiring_plan
            
            private_data.save()
            messages.success(request, 'Información del equipo actualizada exitosamente.')
            return redirect('core:startup_private_section', startup_id, 'people')
    
    elif section == 'news':
        from .models import StartupNews
        private_data, created = StartupNews.objects.get_or_create(startup=startup)
        
        # Manejar POST para noticias
        if request.method == 'POST' and is_founder:
            # Actualizar campos de noticias
            if 'recent_milestones' in request.POST:
                private_data.recent_milestones = request.POST.get('recent_milestones') or ''
            if 'upcoming_announcements' in request.POST:
                private_data.upcoming_announcements = request.POST.get('upcoming_announcements') or ''
            if 'partnerships' in request.POST:
                private_data.partnerships = request.POST.get('partnerships') or ''
            if 'market_updates' in request.POST:
                private_data.market_updates = request.POST.get('market_updates') or ''
            if 'competitive_intelligence' in request.POST:
                private_data.competitive_intelligence = request.POST.get('competitive_intelligence') or ''
            if 'regulatory_updates' in request.POST:
                private_data.regulatory_updates = request.POST.get('regulatory_updates') or ''
            
            private_data.save()
            messages.success(request, 'Información de noticias actualizada exitosamente.')
            return redirect('core:startup_private_section', startup_id, 'news')
    
    elif section == 'technology':
        from .models import StartupTechnology
        private_data, created = StartupTechnology.objects.get_or_create(startup=startup)
        
        # Manejar POST para tecnología
        if request.method == 'POST' and is_founder:
            # Actualizar campos de tecnología
            if 'tech_stack' in request.POST:
                private_data.tech_stack = request.POST.get('tech_stack') or ''
            if 'development_roadmap' in request.POST:
                private_data.development_roadmap = request.POST.get('development_roadmap') or ''
            if 'ip_portfolio' in request.POST:
                private_data.ip_portfolio = request.POST.get('ip_portfolio') or ''
            if 'technical_challenges' in request.POST:
                private_data.technical_challenges = request.POST.get('technical_challenges') or ''
            if 'scalability_plans' in request.POST:
                private_data.scalability_plans = request.POST.get('scalability_plans') or ''
            if 'security_measures' in request.POST:
                private_data.security_measures = request.POST.get('security_measures') or ''
            
            private_data.save()
            messages.success(request, 'Información de tecnología actualizada exitosamente.')
            return redirect('core:startup_private_section', startup_id, 'technology')
    
    context = {
        'startup': startup,
        'section': section,
        'private_data': private_data,
        'is_founder': is_founder
    }
    
    # Agregar datos específicos para el template de people
    if section == 'people' and private_data:
        # Obtener datos de equity distribution
        equity_data = private_data.equity_distribution or {}
        context.update({
            'founders_equity_total': equity_data.get('founders_equity_total', '70.0'),
            'esop_pool_percentage': equity_data.get('esop_pool_percentage', '15.0'),
            'esop_allocated': equity_data.get('esop_allocated', '5.0'),
            'investor_equity_total': equity_data.get('investor_equity_total', '15.0'),
        })
        
        # Obtener datos de cultura
        benefits_data = private_data.employee_benefits or {}
        hiring_data = private_data.hiring_plan_12m or {}
        context.update({
            'company_mission': private_data.company_mission or '',
            'company_vision': private_data.company_vision or '',
            'core_values': private_data.company_values or '',
            'work_mode': private_data.work_mode or 'hybrid',
            'main_location': private_data.main_location or '',
            'employee_benefits_text': benefits_data.get('benefits_text', ''),
            'diversity_initiatives': private_data.diversity_initiativas or '',
            'hiring_budget_annual': private_data.hiring_budget_annual or '',
            'hiring_priority_1': private_data.hiring_priority_1 or '',
            'recruitment_strategy': private_data.recruitment_strategy or '',
        })
        
        # Obtener datos del equipo
        team_data = private_data.founders_detailed_bios or {}
        context['team_members'] = team_data.get('team_members', [])
    
    # Usar el template específico para people, otros usan el template genérico
    if section == 'people':
        template_name = 'core/startup_people.html'
    elif section == 'financials':
        template_name = 'core/startup_financials.html'
    else:
        template_name = f'core/private_sections/{section}.html'
    
    return render(request, template_name, context)

@login_required
@require_POST
def add_event_comment(request, event_id):
    """Vista para agregar comentarios a eventos"""
    try:
        event = get_object_or_404(Event, id=event_id)
        content = request.POST.get('content', '').strip()
        parent_id = request.POST.get('parent_id')
        
        if not content:
            return JsonResponse({'success': False, 'error': 'El comentario no puede estar vacío'})
        
        parent = None
        if parent_id:
            parent = get_object_or_404(EventComment, id=parent_id)
        
        comment = EventComment.objects.create(
            event=event,
            user=request.user,
            content=content,
            parent=parent
        )
        
        # Obtener el perfil del usuario para el avatar
        user_profile = getattr(request.user, 'profile', None)
        
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'user_name': request.user.get_full_name() or request.user.username,
                'user_avatar': user_profile.avatar.url if user_profile and user_profile.avatar else None,
                'created_at': comment.created_at.strftime('%d %b %Y, %H:%M'),
                'parent_id': parent.id if parent else None
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def update_event_attendance(request, event_id):
    """Vista para manejar la asistencia a eventos"""
    try:
        event = get_object_or_404(Event, id=event_id)
        status = request.POST.get('status')  # will_attend, maybe, wont_attend
        guest_count = int(request.POST.get('guest_count', 0))
        
        if status not in ['will_attend', 'maybe', 'wont_attend']:
            return JsonResponse({'success': False, 'error': 'Estado de asistencia inválido'})
        
        attendance, created = EventAttendance.objects.update_or_create(
            event=event,
            user=request.user,
            defaults={
                'status': status,
                'guest_count': guest_count
            }
        )
        
        # Calcular estadísticas de asistencia
        attendance_stats = EventAttendance.objects.filter(event=event).aggregate(
            will_attend=Count('id', filter=Q(status='will_attend')),
            maybe=Count('id', filter=Q(status='maybe')),
            wont_attend=Count('id', filter=Q(status='wont_attend')),
            total_guests=Sum('guest_count', filter=Q(status='will_attend'))
        )
        
        return JsonResponse({
            'success': True,
            'attendance': {
                'status': attendance.status,
                'guest_count': attendance.guest_count,
                'stats': {
                    'will_attend': attendance_stats['will_attend'] or 0,
                    'maybe': attendance_stats['maybe'] or 0,
                    'wont_attend': attendance_stats['wont_attend'] or 0,
                    'total_attendees': (attendance_stats['will_attend'] or 0) + (attendance_stats['total_guests'] or 0)
                }
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def event_detail(request, event_id):
    """Vista para mostrar los detalles de un evento"""
    event = get_object_or_404(Event, id=event_id)
    
    # Obtener comentarios del evento (solo padres, los hijos se cargan via AJAX)
    comments = EventComment.objects.filter(
        event=event, 
        parent=None
    ).select_related('user').order_by('-created_at')
    
    # Estadísticas de asistencia
    attendance_stats = EventAttendance.objects.filter(event=event).aggregate(
        will_attend=Count('id', filter=Q(status='will_attend')),
        maybe=Count('id', filter=Q(status='maybe')),
        wont_attend=Count('id', filter=Q(status='wont_attend')),
        total_guests=Sum('guest_count', filter=Q(status='will_attend'))
    )
    
    # Verificar si el usuario actual ya tiene asistencia registrada
    user_attendance = None
    if request.user.is_authenticated:
        user_attendance = EventAttendance.objects.filter(
            event=event, 
            user=request.user
        ).first()
    
    context = {
        'event': event,
        'comments': comments,
        'user_attendance': user_attendance,
        'attendance_stats': {
            'will_attend': attendance_stats['will_attend'] or 0,
            'maybe': attendance_stats['maybe'] or 0,
            'wont_attend': attendance_stats['wont_attend'] or 0,
            'total_attendees': (attendance_stats['will_attend'] or 0) + (attendance_stats['total_guests'] or 0)
        }
    }
    
    return render(request, 'core/event_detail.html', context)

def get_event_comments(request, event_id):
    """API para obtener comentarios de un evento"""
    event = get_object_or_404(Event, id=event_id)
    parent_id = request.GET.get('parent_id')
    
    if parent_id:
        # Obtener respuestas a un comentario específico
        comments = EventComment.objects.filter(
            event=event, 
            parent_id=parent_id
        ).select_related('user').order_by('created_at')
    else:
        # Obtener comentarios principales
        comments = EventComment.objects.filter(
            event=event, 
            parent=None
        ).select_related('user').order_by('-created_at')
    
    comments_data = []
    for comment in comments:
        user_profile = getattr(comment.user, 'profile', None)
        comments_data.append({
            'id': comment.id,
            'content': comment.content,
            'user_name': comment.user.get_full_name() or comment.user.username,
            'user_avatar': user_profile.avatar.url if user_profile and user_profile.avatar else None,
            'created_at': comment.created_at.strftime('%d %b %Y, %H:%M'),
            'replies_count': comment.replies.count() if not parent_id else 0
        })
    
    return JsonResponse({'comments': comments_data})


# ============================================
# VISTAS DEL CHATBOT IA
# ============================================

from .models import ChatConversation, ChatMessage
from .ai_service import get_ai_response, get_ai_response_stream, generate_conversation_title
import json
from django.http import StreamingHttpResponse

@login_required
@require_http_methods(["GET"])
def chat_interface(request):
    """Página principal del chatbot"""
    # Obtener todas las conversaciones del usuario
    conversations = ChatConversation.objects.filter(user=request.user)
    
    # Obtener la conversación activa o crear una nueva
    active_conversation = conversations.filter(is_active=True).first()
    
    context = {
        'conversations': conversations,
        'active_conversation': active_conversation,
    }
    
    return render(request, 'core/chat.html', context)


@login_required
@require_http_methods(["POST"])
def send_message(request):
    """Enviar un mensaje al chatbot"""
    try:
        data = json.loads(request.body)
        message_content = data.get('message', '').strip()
        conversation_id = data.get('conversation_id')
        
        if not message_content:
            return JsonResponse({'error': 'Mensaje vacío'}, status=400)
        
        # Obtener o crear conversación
        if conversation_id:
            conversation = get_object_or_404(ChatConversation, id=conversation_id, user=request.user)
        else:
            # Crear nueva conversación
            conversation = ChatConversation.objects.create(
                user=request.user,
                title="Nueva conversación"
            )
        
        # Guardar mensaje del usuario
        user_message = ChatMessage.objects.create(
            conversation=conversation,
            role='user',
            content=message_content
        )
        
        # Obtener historial de conversación
        history = []
        previous_messages = conversation.messages.all().order_by('created_at')[:20]  # Últimos 20 mensajes
        for msg in previous_messages:
            if msg.id != user_message.id:  # Excluir el mensaje actual
                history.append({
                    'role': msg.role,
                    'content': msg.content
                })
        
        # Obtener respuesta del AI
        ai_response = get_ai_response(request.user, message_content, history)
        
        # Guardar respuesta del AI
        assistant_message = ChatMessage.objects.create(
            conversation=conversation,
            role='assistant',
            content=ai_response
        )
        
        # Si es la primera conversación, generar título
        if conversation.messages.count() == 2:  # user + assistant
            title = generate_conversation_title(message_content)
            conversation.title = title
            conversation.save()
        
        # Actualizar timestamp de la conversación
        conversation.save()  # Esto actualiza updated_at
        
        return JsonResponse({
            'success': True,
            'conversation_id': conversation.id,
            'conversation_title': conversation.title,
            'user_message': {
                'id': user_message.id,
                'content': user_message.content,
                'created_at': user_message.created_at.isoformat()
            },
            'assistant_message': {
                'id': assistant_message.id,
                'content': assistant_message.content,
                'created_at': assistant_message.created_at.isoformat()
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        print(f"Error en send_message: {str(e)}")
        return JsonResponse({'error': 'Error al procesar el mensaje'}, status=500)


@login_required
@require_http_methods(["POST"])
def send_message_stream(request):
    """Enviar un mensaje al chatbot con streaming"""
    try:
        data = json.loads(request.body)
        message_content = data.get('message', '').strip()
        conversation_id = data.get('conversation_id')
        
        if not message_content:
            return JsonResponse({'error': 'Mensaje vacío'}, status=400)
        
        # Obtener o crear conversación
        if conversation_id:
            conversation = get_object_or_404(ChatConversation, id=conversation_id, user=request.user)
        else:
            # Crear nueva conversación
            conversation = ChatConversation.objects.create(
                user=request.user,
                title="Nueva conversación"
            )
        
        # Guardar mensaje del usuario
        user_message = ChatMessage.objects.create(
            conversation=conversation,
            role='user',
            content=message_content
        )
        
        # Obtener historial de conversación
        history = []
        previous_messages = conversation.messages.all().order_by('created_at')[:20]
        for msg in previous_messages:
            if msg.id != user_message.id:
                history.append({
                    'role': msg.role,
                    'content': msg.content
                })
        
        # Función generadora para el streaming
        def generate():
            full_response = ""
            
            # Enviar metadata inicial
            yield f"data: {json.dumps({'type': 'start', 'conversation_id': conversation.id, 'user_message_id': user_message.id})}\n\n"
            
            # Forzar el flush inmediato
            import sys
            sys.stdout.flush()
            
            try:
                # Obtener respuesta del AI con streaming
                for chunk in get_ai_response_stream(request.user, message_content, history):
                    full_response += chunk
                    # Enviar cada chunk al cliente inmediatamente
                    chunk_data = json.dumps({'type': 'chunk', 'content': chunk})
                    yield f"data: {chunk_data}\n\n"
                    
                    # Forzar el flush para envío inmediato
                    sys.stdout.flush()
                
                # Guardar respuesta completa del AI
                assistant_message = ChatMessage.objects.create(
                    conversation=conversation,
                    role='assistant',
                    content=full_response
                )
                
                # Si es la primera conversación, generar título
                if conversation.messages.count() == 2:
                    title = generate_conversation_title(message_content)
                    conversation.title = title
                    conversation.save()
                
                # Actualizar timestamp
                conversation.save()
                
                # Enviar evento de finalización
                yield f"data: {json.dumps({'type': 'end', 'assistant_message_id': assistant_message.id, 'conversation_title': conversation.title})}\n\n"
                
            except Exception as e:
                print(f"Error en streaming: {str(e)}")
                yield f"data: {json.dumps({'type': 'error', 'message': 'Error al procesar el mensaje'})}\n\n"
        
        # Retornar respuesta con streaming sin buffering
        response = StreamingHttpResponse(generate(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache, no-transform'
        response['X-Accel-Buffering'] = 'no'
        return response
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        print(f"Error en send_message_stream: {str(e)}")
        return JsonResponse({'error': 'Error al procesar el mensaje'}, status=500)


@login_required
@require_http_methods(["GET"])
def get_conversation(request, conversation_id):
    """Obtener mensajes de una conversación específica"""
    try:
        conversation = get_object_or_404(ChatConversation, id=conversation_id, user=request.user)
        messages = conversation.messages.all().order_by('created_at')
        
        messages_data = [{
            'id': msg.id,
            'role': msg.role,
            'content': msg.content,
            'created_at': msg.created_at.isoformat()
        } for msg in messages]
        
        return JsonResponse({
            'success': True,
            'conversation': {
                'id': conversation.id,
                'title': conversation.title,
                'created_at': conversation.created_at.isoformat()
            },
            'messages': messages_data
        })
        
    except Exception as e:
        print(f"Error en get_conversation: {str(e)}")
        return JsonResponse({'error': 'Error al cargar la conversación'}, status=500)


@login_required
@require_http_methods(["POST"])
def new_conversation(request):
    """Crear una nueva conversación"""
    try:
        # Desactivar otras conversaciones activas
        ChatConversation.objects.filter(user=request.user, is_active=True).update(is_active=False)
        
        # Crear nueva conversación
        conversation = ChatConversation.objects.create(
            user=request.user,
            title="Nueva conversación",
            is_active=True
        )
        
        return JsonResponse({
            'success': True,
            'conversation': {
                'id': conversation.id,
                'title': conversation.title,
                'created_at': conversation.created_at.isoformat()
            }
        })
        
    except Exception as e:
        print(f"Error en new_conversation: {str(e)}")
        return JsonResponse({'error': 'Error al crear conversación'}, status=500)


@login_required
@require_http_methods(["POST"])
def delete_conversation(request, conversation_id):
    """Eliminar una conversación"""
    try:
        conversation = get_object_or_404(ChatConversation, id=conversation_id, user=request.user)
        conversation.delete()
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        print(f"Error en delete_conversation: {str(e)}")
        return JsonResponse({'error': 'Error al eliminar conversación'}, status=500)


@login_required
@require_http_methods(["GET"])
def get_conversations(request):
    """Obtener lista de conversaciones del usuario"""
    try:
        conversations = ChatConversation.objects.filter(user=request.user).order_by('-updated_at')
        
        conversations_data = [{
            'id': conv.id,
            'title': conv.title,
            'is_active': conv.is_active,
            'created_at': conv.created_at.isoformat(),
            'updated_at': conv.updated_at.isoformat(),
            'messages_count': conv.messages.count()
        } for conv in conversations]
        
        return JsonResponse({
            'success': True,
            'conversations': conversations_data
        })
        
    except Exception as e:
        print(f"Error en get_conversations: {str(e)}")
        return JsonResponse({'error': 'Error al cargar conversaciones'}, status=500)

