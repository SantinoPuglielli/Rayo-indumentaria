import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
DEBUG = True

# ✅ Hosts permitidos
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".ngrok-free.app",  # Permite túneles públicos de ngrok
    ".ngrok-free.dev",
]

# ✅ Seguridad para peticiones POST desde ngrok
CSRF_TRUSTED_ORIGINS = [
    "https://*.ngrok-free.app",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://*.ngrok-free.dev",
]

# -----------------------------------------------------------
# 🧱 APLICACIONES INSTALADAS
# -----------------------------------------------------------
INSTALLED_APPS = [
    "jazzmin",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Tus apps locales
    'aplications.accounts',
    'aplications.catalog',
    'aplications.cart',
    'aplications.orders',
    'aplications.payments',
    'aplications.reports',
    'core',
]

# -----------------------------------------------------------
# ⚙️ MIDDLEWARE
# -----------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rayo_shop.urls'

# -----------------------------------------------------------
# 🎨 TEMPLATES
# -----------------------------------------------------------
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
        'core.context_processors.carousel_slides',  # carrusel
        'core.context_processors.layout_meta',      # categorías + contador carrito
    ]},
}]

WSGI_APPLICATION = 'rayo_shop.wsgi.application'

# -----------------------------------------------------------
# 💾 BASE DE DATOS
# -----------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME": "Rayo indumentaria",
        "HOST": r"localhost\SQLEXPRESS",
        "OPTIONS": {
            "driver": "ODBC Driver 17 for SQL Server",
            "trusted_connection": "yes",
        },
    }
}

AUTH_PASSWORD_VALIDATORS = []

# -----------------------------------------------------------
# 🌍 REGIONALIZACIÓN
# -----------------------------------------------------------
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------------
# 🖼️ ARCHIVOS ESTÁTICOS Y MEDIA
# -----------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'core' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------------------------------------
# 💰 MERCADO PAGO (modo desarrollo con ngrok)
# -----------------------------------------------------------
# === Mercado Pago ===
MP_PUBLIC_KEY = "APP_USR-0236871f-2e40-4e2d-8d9c-c70123a868f3"
MP_ACCESS_TOKEN = "APP_USR-2447108626717792-101900-1fc7854bacbdbc9aca36420fa001e03e-2932784221"

# URL pública o de ngrok para pruebas (ejemplo)
SITE_DOMAIN = "https://tu-url.ngrok-free.app"

# URL del sitio local
SITE_URL = os.getenv('SITE_URL', 'http://127.0.0.1:8000')

# -----------------------------------------------------------
# 🎨 JAZZMIN - PANEL ADMIN RAYO INDUMENTARIA
# -----------------------------------------------------------
JAZZMIN_SETTINGS = {
    "site_title": "Panel Rayo Indumentaria",
    "site_header": "Rayo Indumentaria",
    "site_brand": "Rayo Admin",
    "site_logo": "img/logo.png",
    "site_icon": "img/favicon.png",
    "welcome_sign": "Bienvenido al panel de administración de Rayo Indumentaria",
    "copyright": "Rayo Indumentaria © 2025",
    "show_sidebar": True,
    "navigation_expanded": True,
     "topmenu_links": [
        {"name": "Inicio", "url": "admin:index", "permissions": ["auth.view_user"], "icon": "fas fa-home"},
        {"name": "Ver sitio", "url": "/", "permissions": ["auth.view_user"], "icon": "fas fa-globe"},
        {"name": "Reportes", "url": "/reports/", "permissions": ["auth.view_user"], "icon": "fas fa-chart-line"},
    ],
    
    "icons": {
        "accounts": "fas fa-users",
        "catalog": "fas fa-tshirt",
        "orders": "fas fa-shopping-cart",
        "cart": "fas fa-shopping-bag",
        "payments": "fas fa-credit-card",
        "reports": "fas fa-chart-line",
        "auth": "fas fa-user-shield",
    },
    "order_with_respect_to": [
        "accounts",
        "catalog",
        "orders",
        "payments",
        "reports",
    ],
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    "language_chooser": False,
    "custom_links": {
        "accounts": [{
            "name": "Ver sitio web",
            "url": "/",
            "icon": "fas fa-home",
            "permissions": ["auth.view_user"]
        }]
    },
}

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
    "dark_mode_theme": "cyborg",
    "navbar": "navbar-dark navbar-danger",
    "sidebar": "sidebar-dark-danger",
    "brand_colour": "navbar-danger",
    "accent": "accent-danger",
    "button_classes": {"primary": "btn-danger", "secondary": "btn-dark"},
    "actions_sticky_top": True,
}
