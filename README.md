# 🚀 StartupConnect - Silicon Valley Ecosystem Platform

![Django](https://img.shields.io/badge/Django-4.2.20-green)
![Python](https://img.shields.io/badge/Python-3.13+-blue)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0+-cyan)
![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen)

**StartupConnect** es una plataforma integral para el ecosistema de startups de Silicon Valley que conecta founders, inversores y builders en un ambiente colaborativo y profesional.

## ✨ Características Principales

### 🏢 **Para Founders**
- **Perfiles de Startup**: Crea y gestiona el perfil completo de tu startup
- **Demo Days**: Organiza y participa en eventos de presentación
- **Red de Contactos**: Conecta con inversores y otros founders
- **Gestión de Equity**: Herramientas para managing equity y cap table

### 💰 **Para Inversores**
- **Directorio de Startups**: Explora startups categorizadas por industria
- **Perfiles de Inversor**: Muestra tu portfolio y criterios de inversión
- **Event Networking**: Participa en eventos exclusivos del ecosistema
- **Deal Flow**: Gestiona y rastrea oportunidades de inversión

### 📅 **Sistema de Eventos**
- **Creación Profesional**: Modal avanzado con validación robusta
- **Tipos Diversos**: Demo Days, Networking, Workshops, Panels, Pitch Competitions
- **Modalidades**: Eventos presenciales y virtuales
- **California Focus**: 40+ ciudades de California organizadas por regiones

### 🎨 **Experiencia de Usuario**
- **Diseño Profesional**: UI/UX moderna inspirada en Silicon Valley
- **Dashboard Intuitivo**: Sidebar colapsible con navegación fluida
- **Responsive Design**: Optimizado para desktop, tablet y móvil
- **Animaciones Modernas**: Transiciones suaves y microinteracciones

## 🛠 Tech Stack

### **Backend**
- **Django 4.2.20**: Framework web robusto y escalable
- **SQLite**: Base de datos (configurable para PostgreSQL en producción)
- **Django HTMX**: Interacciones dinámicas sin JavaScript complejo

### **Frontend**
- **TailwindCSS**: Framework CSS utility-first
- **Vanilla JavaScript**: Funcionalidad moderna sin frameworks pesados
- **Responsive Design**: Mobile-first approach

## 🚀 Instalación y Setup

### Prerrequisitos
```bash
Python 3.13+
Node.js 20+
Git
```

### 1. Clonar el Repositorio
```bash
git clone https://github.com/peterfulle/california.git
cd california
```

### 2. Crear Entorno Virtual
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 3. Instalar Dependencias
```bash
# Python dependencies
pip install -r requirements.txt

# Node dependencies para TailwindCSS
npm install
```

### 4. Configurar Base de Datos
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Ejecutar Servidor
```bash
python manage.py runserver
```

Visita `http://127.0.0.1:8000` para ver la aplicación.

## 📁 Estructura del Proyecto

```
california/
├── core/                   # App principal
│   ├── models.py          # Modelos (User, Startup, Event, etc.)
│   ├── views.py           # Vistas y lógica de negocio
│   ├── forms.py           # Formularios Django
│   ├── urls.py            # URLs routing
│   └── templates/         # Templates HTML
├── mydevsite/             # Configuración Django
├── templates/             # Templates base
├── static/                # Assets estáticos
├── media/                 # Archivos subidos por usuarios
├── requirements.txt       # Dependencias Python
├── package.json          # Dependencias Node.js
└── tailwind.config.js    # Configuración TailwindCSS
```

## 🌟 Características Destacadas

### Modal de Eventos Profesional
- **3 Pasos Intuitivos**: Información básica → Fecha y capacidad → Ubicación
- **Validación Robusta**: Frontend y backend validation
- **40+ Ciudades de CA**: Organizadas por Bay Area, Peninsula, South Bay, etc.
- **Modalidades Flexibles**: Presencial con ubicaciones o virtual con URLs

### Dashboard Moderno
- **Sidebar Colapsible**: Navegación optimizada para espacio
- **Animaciones Fluidas**: Transiciones suaves entre secciones
- **Estados de Usuario**: Diferentes vistas para founders vs inversores
- **Responsive**: Adaptable a cualquier tamaño de pantalla

## 🤝 Contribución

1. Fork el proyecto
2. Crea una feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👥 Equipo

- **Lead Developer**: [Peter Fulle](https://github.com/peterfulle)
- **Design**: Inspirado en el ecosistema de Silicon Valley

---

<div align="center">
  <p><strong>Construido con ❤️ para el ecosistema de Silicon Valley</strong></p>
  <p><em>"Connecting dreams with capital, one startup at a time"</em></p>
</div>
