# Silicon Founder - Plataforma de Emprendimiento e Innovación

![Silicon Founder Banner](docs/images/silicon-founder-banner.png)

[![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![HTMX](https://img.shields.io/badge/HTMX-3366CC?style=for-the-badge&logo=htmx&logoColor=white)](https://htmx.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

Una plataforma premium y moderna para emprendedores e innovadores del ecosistema tecnológico. Construida con Django, Tailwind CSS y HTMX para ofrecer una experiencia fluida, responsiva e interactiva que impulsa la innovación digital.

## 🚀 Características

- **🎨 Diseño Premium**: Interfaz moderna con tema oscuro y efectos visuales impactantes
- **📱 Totalmente Responsivo**: Experiencia perfecta en todos los dispositivos, desde móviles hasta desktop
- **✨ Animaciones Interactivas**: Transiciones fluidas y efectos 3D potenciados por GSAP y AOS
- **⚡ Integración HTMX**: Formularios dinámicos y funcionalidad Ajax sin escribir JavaScript
- **🔍 SEO Optimizado**: Mejores prácticas para visibilidad en motores de búsqueda
- **📊 Gestión Dinámica**: Sistema de administración fácil para servicios, proyectos y testimonios
- **💻 Showcase de Código**: Muestras de código con resaltado de sintaxis para demostrar expertise técnico
- **🛡️ Panel de Administración**: Dashboard personalizado de Django para gestión de contenido

## 📸 Capturas de Pantalla

<table>
  <tr>
    <td><img src="docs/images/screenshots/home-page.png" alt="Página Principal" width="100%"></td>
    <td><img src="docs/images/screenshots/services-page.png" alt="Página de Servicios" width="100%"></td>
  </tr>
  <tr>
    <td><img src="docs/images/screenshots/projects-page.png" alt="Página de Proyectos" width="100%"></td>
    <td><img src="docs/images/screenshots/contact-form.png" alt="Formulario de Contacto" width="100%"></td>
  </tr>
</table>

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.8+** - [Descargar Python](https://python.org/downloads/)
- **pip** - Gestor de paquetes de Python
- **Git** - [Descargar Git](https://git-scm.com/)
- **Node.js** (opcional, para desarrollo avanzado) - [Descargar Node.js](https://nodejs.org/)

## 🛠️ Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/peterfulle/siliconfounder.git
cd siliconfounder


🏗️ Estructura del Proyecto
Code
siliconfounder/
├── core/                        # Aplicación principal
│   ├── migrations/              # Migraciones de la base de datos
│   ├── static/                  # Activos estáticos específicos de la app
│   ├── templates/               # Plantillas HTML
│   ├── admin.py                 # Configuración del panel de administración
│   ├── forms.py                 # Definiciones de formularios
│   ├── models.py                # Modelos de base de datos
│   ├── urls.py                  # Configuración de URLs
│   └── views.py                 # Controladores de vistas
├── docs/                        # Documentación
│   ├── images/                  # Imágenes del README
│   └── deployment/              # Guías de despliegue
├── media/                       # Contenido subido por usuarios
├── mydevsite/                   # Configuración del proyecto
│   ├── settings/                # Configuraciones separadas por entorno
│   │   ├── base.py             # Configuración base
│   │   ├── development.py      # Configuración de desarrollo
│   │   └── production.py       # Configuración de producción
│   ├── urls.py                  # URLs principales
│   └── wsgi.py                  # Configuración WSGI
├── static/                      # Archivos estáticos globales
├── templates/                   # Plantillas globales
│   └── base.html               # Template base
├── utils/                       # Utilidades personalizadas
├── .env                         # Variables de entorno
├── .gitignore                   # Archivo gitignore
├── docker-compose.yml           # Configuración Docker
├── manage.py                    # Script de gestión de Django
├── requirements.txt             # Dependencias de Python
└── tailwind.config.js           # Configuración de Tailwind CSS


Colores y Tema
Los colores principales se definen en templates/base.html:

JavaScript
colors: {
  accent: {
    primary: '#6366F1',   // Indigo
    secondary: '#22D3EE', // Cyan
    third: '#10B981',     // Emerald
  }
}
Contenido
Servicios: Edita core/models.py para agregar nuevos servicios
Proyectos: Usa el panel de administración Django para gestionar proyectos
Testimonios: Configura testimonios de clientes desde el admin
Información de contacto: Modifica templates/base.html

Configuración de la Aplicación
bash
# Cambiar al usuario de la aplicación
sudo su - siliconfounder

# Clonar el repositorio
git clone https://github.com/peterfulle/siliconfounder.git
cd siliconfounder

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Configurar variables de entorno de producción
nano .env
Contenido del .env para producción:

env
SECRET_KEY=tu_clave_secreta_super_segura_de_produccion
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,tu_ip_servidor
DATABASE_URL=postgresql://siliconfounder_user:tu_password_seguro@localhost/siliconfounder_db
STATIC_ROOT=/home/siliconfounder/siliconfounder/staticfiles/
MEDIA_ROOT=/home/siliconfounder/siliconfounder/media/
Configuración de Gunicorn
bash
# Crear archivo de configuración para Gunicorn
nano gunicorn.conf.py
Python
bind = "127.0.0.1:8000"
workers = 3
user = "siliconfounder"
timeout = 120
keepalive = 5
max_requests = 1000
preload_app = True
Configuración de Systemd
bash
sudo nano /etc/systemd/system/siliconfounder.service
INI
[Unit]
Description=Silicon Founder Django Application
After=network.target

[Service]
User=siliconfounder
Group=siliconfounder
WorkingDirectory=/home/siliconfounder/siliconfounder
Environment=PATH=/home/siliconfounder/siliconfounder/venv/bin
ExecStart=/home/siliconfounder/siliconfounder/venv/bin/gunicorn --config gunicorn.conf.py mydevsite.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
Configuración de Nginx
bash
sudo nano /etc/nginx/sites-available/siliconfounder
Nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/siliconfounder/siliconfounder;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        root /home/siliconfounder/siliconfounder;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
Finalizar Configuración
bash
# Ejecutar migraciones y recopilar archivos estáticos
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# Habilitar y iniciar servicios
sudo systemctl enable siliconfounder
sudo systemctl start siliconfounder
sudo systemctl status siliconfounder

# Configurar Nginx
sudo ln -s /etc/nginx/sites-available/siliconfounder /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
SSL con Let's Encrypt (Opcional pero Recomendado)
bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado SSL
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# Verificar renovación automática
sudo certbot renew --dry-run
🔧 Tecnologías Utilizadas
Backend: Django 4.2+, Python 3.8+
Frontend: Tailwind CSS, HTMX, JavaScript ES6+
Animaciones: GSAP, AOS (Animate On Scroll)
3D Graphics: Three.js
Icons: Font Awesome 6
Database: SQLite (desarrollo), PostgreSQL (producción)
Web Server: Nginx
WSGI Server: Gunicorn
Deployment: Docker, Heroku, VPS
📝 API Endpoints
Endpoint	Método	Descripción
/	GET	Página principal
/admin/	GET	Panel de administración Django
/contact/	POST	Envío de formulario de contacto
/api/stats/	GET	Estadísticas del sitio (JSON)
🔒 Seguridad
Configuraciones de Seguridad Implementadas
CSRF Protection: Protección contra ataques Cross-Site Request Forgery
XSS Protection: Prevención de ataques Cross-Site Scripting
SQL Injection Prevention: ORM de Django previene inyección SQL
Secure Headers: Headers de seguridad configurados
HTTPS Enforcement: Redirección automática a HTTPS en producción
Variables de Entorno Sensibles
Nunca incluir en el código:

SECRET_KEY
Credenciales de base de datos
Claves de API
Tokens de autenticación
📊 Monitoreo y Performance
Métricas Incluidas
Page Load Speed: Optimización de carga de páginas
Database Queries: Optimización de consultas SQL
Static Files: Compresión y cache de archivos estáticos
Error Tracking: Logging de errores y excepciones
Herramientas Recomendadas
Sentry: Para tracking de errores en producción
New Relic: Para monitoreo de performance
Google Analytics: Para análisis de tráfico
GTmetrix: Para análisis de velocidad
🧪 Testing
Ejecutar Tests
bash
# Ejecutar todos los tests
python manage.py test

# Ejecutar tests específicos
python manage.py test core.tests

# Ejecutar tests con coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
Tipos de Tests Incluidos
Unit Tests: Tests de modelos y funciones
Integration Tests: Tests de vistas y formularios
UI Tests: Tests de interface de usuario (opcional con Selenium)
🤝 Contribución
¡Las contribuciones son bienvenidas! Por favor:

Haz un Fork del proyecto
Crea una rama para tu feature (git checkout -b feature/AmazingFeature)
Confirma tus cambios (git commit -m 'Add some AmazingFeature')
Push a la rama (git push origin feature/AmazingFeature)
Abre un Pull Request
Guías de Contribución
Sigue las convenciones de código de Django
Escribe tests para nuevas funcionalidades
Actualiza la documentación según sea necesario
Usa commits descriptivos siguiendo Conventional Commits
Estilo de Código
bash
# Instalar herramientas de formateo
pip install black flake8 isort

# Formatear código
black .
isort .
flake8 .
🐛 Reporte de Bugs
Si encuentras un bug, por favor:

Verifica que no haya sido reportado anteriormente
Crea un nuevo issue
Incluye detalles del error, pasos para reproducirlo y tu entorno
Template para Reporte de Bugs
Markdown
**Describe el bug**
Una descripción clara y concisa del problema.

**Para Reproducir**
Pasos para reproducir el comportamiento:
1. Ve a '...'
2. Haz clic en '....'
3. Desplázate hacia abajo hasta '....'
4. Ve el error

**Comportamiento Esperado**
Una descripción clara y concisa de lo que esperabas que sucediera.

**Screenshots**
Si aplica, agrega screenshots para ayudar a explicar tu problema.

**Información del Entorno:**
- OS: [e.g. Ubuntu 20.04, Windows 10, macOS Big Sur]
- Python Version: [e.g. 3.9.7]
- Django Version: [e.g. 4.2.7]
- Browser: [e.g. Chrome 96, Firefox 94, Safari 15]

**Contexto Adicional**
Agrega cualquier otro contexto sobre el problema aquí.
📄 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

Code
MIT License

Copyright (c) 2025 Peter Fulle

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
