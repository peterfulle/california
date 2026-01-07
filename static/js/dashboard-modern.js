/**
 * Dashboard Modern - JavaScript Module
 * Maneja todas las interacciones y animaciones del dashboard
 */

class DashboardModern {
    constructor() {
        this.isInitialized = false;
        this.charts = {};
        this.animations = new Map();
        this.observers = new Map();
        
        this.init();
    }
    
    init() {
        if (this.isInitialized) return;
        
        // Esperar a que el DOM esté listo
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
    }
    
    setup() {
        this.setupAnimations();
        this.setupInteractions();
        this.setupCharts();
        this.setupTooltips();
        this.setupSearch();
        this.restoreUserPreferences();
        
        this.isInitialized = true;
        console.log('🚀 Dashboard Modern initialized');
    }
    
    /**
     * Configurar animaciones de entrada
     */
    setupAnimations() {
        // Intersection Observer para animaciones
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    
                    // Animación de fade-in con delay
                    const delay = Array.from(element.parentNode.children).indexOf(element) * 100;
                    
                    setTimeout(() => {
                        element.classList.add('animate-fade-slide');
                        element.style.opacity = '1';
                        element.style.transform = 'translateY(0)';
                    }, delay);
                    
                    animationObserver.unobserve(element);
                }
            });
        }, observerOptions);
        
        // Observar elementos animables
        const animatedElements = document.querySelectorAll('[data-animate], .stat-card, .card-modern');
        animatedElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            animationObserver.observe(el);
        });
        
        this.observers.set('animation', animationObserver);
    }
    
    /**
     * Configurar interacciones de la UI
     */
    setupInteractions() {
        // Sidebar toggle mejorado
        this.setupSidebarToggle();
        
        // Cards hover effects
        this.setupCardInteractions();
        
        // Smooth scrolling
        this.setupSmoothScrolling();
        
        // Keyboard shortcuts
        this.setupKeyboardShortcuts();
    }
    
    setupSidebarToggle() {
        const sidebar = document.getElementById('sidebar');
        const mainContent = document.getElementById('mainContent');
        const toggleBtn = sidebar?.querySelector('button[onclick="toggleSidebar()"]');
        
        if (!sidebar || !mainContent) return;
        
        // Mejorar la función toggle existente
        window.toggleSidebar = () => {
            const isExpanded = sidebar.classList.contains('sidebar-expanded');
            const sidebarTexts = document.querySelectorAll('.sidebar-text');
            
            if (isExpanded) {
                sidebar.classList.remove('sidebar-expanded');
                sidebar.classList.add('sidebar-collapsed');
                
                // Animar textos con stagger
                sidebarTexts.forEach((text, index) => {
                    setTimeout(() => {
                        text.style.opacity = '0';
                        text.style.transform = 'translateX(-10px)';
                    }, index * 20);
                    
                    setTimeout(() => {
                        text.classList.add('hidden');
                    }, 150);
                });
                
                mainContent.style.marginLeft = 'var(--sidebar-collapsed-width)';
                localStorage.setItem('sidebarCollapsed', 'true');
            } else {
                sidebar.classList.remove('sidebar-collapsed');
                sidebar.classList.add('sidebar-expanded');
                
                // Animar textos con stagger
                sidebarTexts.forEach((text, index) => {
                    text.classList.remove('hidden');
                    setTimeout(() => {
                        text.style.opacity = '1';
                        text.style.transform = 'translateX(0)';
                    }, 50 + index * 20);
                });
                
                mainContent.style.marginLeft = 'var(--sidebar-width)';
                localStorage.setItem('sidebarCollapsed', 'false');
            }
        };
    }
    
    setupCardInteractions() {
        const cards = document.querySelectorAll('.stat-card, .card-modern');
        
        cards.forEach(card => {
            // Efecto de hover mejorado
            card.addEventListener('mouseenter', (e) => {
                e.currentTarget.style.transform = 'translateY(-8px) scale(1.02)';
                e.currentTarget.style.boxShadow = 'var(--shadow-2xl)';
            });
            
            card.addEventListener('mouseleave', (e) => {
                e.currentTarget.style.transform = 'translateY(0) scale(1)';
                e.currentTarget.style.boxShadow = 'var(--shadow-sm)';
            });
            
            // Efecto de click
            card.addEventListener('mousedown', (e) => {
                e.currentTarget.style.transform = 'translateY(-6px) scale(0.98)';
            });
            
            card.addEventListener('mouseup', (e) => {
                e.currentTarget.style.transform = 'translateY(-8px) scale(1.02)';
            });
        });
    }
    
    setupSmoothScrolling() {
        // Smooth scroll para enlaces internos
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K para abrir búsqueda
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchInput = document.querySelector('input[placeholder*="Buscar"]');
                if (searchInput) {
                    searchInput.focus();
                    searchInput.select();
                }
            }
            
            // Ctrl/Cmd + B para toggle sidebar
            if ((e.ctrlKey || e.metaKey) && e.key === 'b') {
                e.preventDefault();
                if (window.toggleSidebar) {
                    window.toggleSidebar();
                }
            }
            
            // Escape para cerrar modales/overlays
            if (e.key === 'Escape') {
                this.closeAllOverlays();
            }
        });
    }
    
    /**
     * Configurar gráficos dinámicos
     */
    setupCharts() {
        // Chart.js configuración global
        if (window.Chart) {
            Chart.defaults.font.family = 'Inter, sans-serif';
            Chart.defaults.font.size = 12;
            Chart.defaults.font.weight = '500';
            Chart.defaults.color = '#64748b';
            
            // Configurar chart del dashboard si existe
            this.initActivityChart();
        }
    }
    
    initActivityChart() {
        const ctx = document.getElementById('activityChart');
        if (!ctx) return;
        
        const gradient1 = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
        gradient1.addColorStop(0, 'rgba(14, 165, 233, 0.3)');
        gradient1.addColorStop(1, 'rgba(14, 165, 233, 0.05)');
        
        const gradient2 = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
        gradient2.addColorStop(0, 'rgba(16, 185, 129, 0.3)');
        gradient2.addColorStop(1, 'rgba(16, 185, 129, 0.05)');
        
        this.charts.activity = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
                datasets: [{
                    label: 'Startups registradas',
                    data: [12, 19, 8, 15, 22, 8, 14],
                    borderColor: '#0ea5e9',
                    backgroundColor: gradient1,
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#0ea5e9',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 3,
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    pointHoverBorderWidth: 4
                }, {
                    label: 'Inversores activos',
                    data: [7, 11, 5, 8, 13, 5, 9],
                    borderColor: '#10b981',
                    backgroundColor: gradient2,
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#10b981',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 3,
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    pointHoverBorderWidth: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            font: {
                                size: 14,
                                weight: '600'
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: '#1e293b',
                        titleColor: '#f8fafc',
                        bodyColor: '#f8fafc',
                        borderColor: '#334155',
                        borderWidth: 1,
                        cornerRadius: 12,
                        padding: 12,
                        displayColors: true,
                        usePointStyle: true
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: {
                                size: 12,
                                weight: '500'
                            },
                            color: '#64748b'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            borderDash: [5, 5],
                            color: '#e2e8f0'
                        },
                        ticks: {
                            font: {
                                size: 12,
                                weight: '500'
                            },
                            color: '#64748b'
                        }
                    }
                },
                animation: {
                    duration: 2000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }
    
    /**
     * Sistema de tooltips mejorado
     */
    setupTooltips() {
        let tooltip = null;
        
        // Tooltips para sidebar colapsada
        const sidebarItems = document.querySelectorAll('.sidebar-item');
        
        sidebarItems.forEach(item => {
            item.addEventListener('mouseenter', (e) => {
                const sidebar = document.getElementById('sidebar');
                if (!sidebar?.classList.contains('sidebar-collapsed')) return;
                
                const text = e.currentTarget.querySelector('.sidebar-text');
                if (!text) return;
                
                this.showTooltip(e.currentTarget, text.textContent.trim());
            });
            
            item.addEventListener('mouseleave', () => {
                this.hideTooltip();
            });
        });
    }
    
    showTooltip(element, text) {
        this.hideTooltip(); // Limpiar tooltip anterior
        
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip-modern show';
        tooltip.textContent = text;
        tooltip.id = 'dashboard-tooltip';
        
        document.body.appendChild(tooltip);
        
        const rect = element.getBoundingClientRect();
        const tooltipRect = tooltip.getBoundingClientRect();
        
        tooltip.style.left = rect.right + 15 + 'px';
        tooltip.style.top = rect.top + (rect.height / 2) - (tooltipRect.height / 2) + 'px';
        
        // Verificar si está fuera de la pantalla
        if (tooltip.offsetLeft + tooltip.offsetWidth > window.innerWidth) {
            tooltip.style.left = rect.left - tooltip.offsetWidth - 15 + 'px';
        }
    }
    
    hideTooltip() {
        const tooltip = document.getElementById('dashboard-tooltip');
        if (tooltip) {
            tooltip.classList.remove('show');
            setTimeout(() => tooltip.remove(), 150);
        }
    }
    
    /**
     * Búsqueda inteligente
     */
    setupSearch() {
        const searchInput = document.querySelector('input[placeholder*="Buscar"]');
        if (!searchInput) return;
        
        let searchTimeout;
        
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            const query = e.target.value.trim();
            
            if (query.length < 2) {
                this.hideSearchResults();
                return;
            }
            
            searchTimeout = setTimeout(() => {
                this.performSearch(query);
            }, 300);
        });
        
        searchInput.addEventListener('focus', () => {
            searchInput.classList.add('ring-4', 'ring-primary-500/20');
        });
        
        searchInput.addEventListener('blur', () => {
            searchInput.classList.remove('ring-4', 'ring-primary-500/20');
            setTimeout(() => this.hideSearchResults(), 150);
        });
    }
    
    performSearch(query) {
        // Simular búsqueda (implementar según necesidades)
        console.log('Searching for:', query);
        
        // Aquí iría la lógica de búsqueda real
        // Por ahora solo mostramos un mensaje
        this.showSearchResults([
            { type: 'startup', name: 'TechVision AI', description: 'Startup de inteligencia artificial' },
            { type: 'investor', name: 'Capital Ventures', description: 'Fondo de inversión tecnológico' }
        ].filter(item => 
            item.name.toLowerCase().includes(query.toLowerCase()) ||
            item.description.toLowerCase().includes(query.toLowerCase())
        ));
    }
    
    showSearchResults(results) {
        let resultsContainer = document.getElementById('search-results');
        
        if (!resultsContainer) {
            resultsContainer = document.createElement('div');
            resultsContainer.id = 'search-results';
            resultsContainer.className = 'absolute top-full left-0 right-0 mt-2 bg-white rounded-xl shadow-xl border border-gray-200 max-h-96 overflow-y-auto z-50';
            
            const searchInput = document.querySelector('input[placeholder*="Buscar"]');
            searchInput.parentNode.appendChild(resultsContainer);
        }
        
        if (results.length === 0) {
            resultsContainer.innerHTML = `
                <div class="p-4 text-center text-gray-500">
                    <svg class="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                    No se encontraron resultados
                </div>
            `;
            return;
        }
        
        resultsContainer.innerHTML = results.map(result => `
            <div class="p-4 hover:bg-gray-50 border-b border-gray-100 last:border-b-0 cursor-pointer transition-colors">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-lg bg-gradient-to-r from-primary-500 to-purple-600 flex items-center justify-center">
                        <span class="text-white font-semibold text-sm">${result.name.charAt(0)}</span>
                    </div>
                    <div>
                        <p class="font-semibold text-gray-900">${result.name}</p>
                        <p class="text-sm text-gray-600">${result.description}</p>
                        <span class="inline-block px-2 py-1 text-xs font-medium rounded-full ${
                            result.type === 'startup' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'
                        }">${result.type}</span>
                    </div>
                </div>
            </div>
        `).join('');
    }
    
    hideSearchResults() {
        const resultsContainer = document.getElementById('search-results');
        if (resultsContainer) {
            resultsContainer.remove();
        }
    }

    /**
     * Restaurar preferencias del usuario
     */
    restoreUserPreferences() {
        // Restaurar estado del sidebar
        const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        if (isCollapsed && window.toggleSidebar) {
            window.toggleSidebar();
        }
        
        // Otras preferencias pueden ir aquí
        const theme = localStorage.getItem('dashboardTheme');
        if (theme) {
            document.documentElement.setAttribute('data-theme', theme);
        }
    }
    
    /**
     * Cerrar todos los overlays abiertos
     */
    closeAllOverlays() {
        const overlays = document.querySelectorAll('[class*="fixed"][class*="inset-0"]');
        overlays.forEach(overlay => overlay.remove());
        
        this.hideSearchResults();
        this.hideTooltip();
    }
    
    /**
     * Cleanup cuando sea necesario
     */
    destroy() {
        this.observers.forEach(observer => observer.disconnect());
        this.observers.clear();
        
        Object.values(this.charts).forEach(chart => chart.destroy());
        this.charts = {};
        
        this.isInitialized = false;
    }
}

// Inicializar automáticamente
const dashboard = new DashboardModern();

// Exportar para uso global
window.DashboardModern = DashboardModern;
window.dashboard = dashboard;
