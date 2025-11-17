import os
import environ
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables del entorno (.env)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

# -----------------------------------------------------------
# 🔐 Seguridad y modo debug
# -----------------------------------------------------------
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
DEBUG = env.bool("DEBUG", True)

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".ngrok-free.app",     # Permite túneles de ngrok para entorno sandbox
    ".ngrok-free.dev",
]

CSRF_TRUSTED_ORIGINS = [
    "https://*.ngrok-free.app",
    "https://*.ngrok-free.dev",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

# -----------------------------------------------------------
# 🧱 Aplicaciones instaladas
# -----------------------------------------------------------
INSTALLED_APPS = [
    "jazzmin",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps del proyecto
    'aplications.accounts',
    'aplications.catalog',
    'aplications.cart',
    'aplications.orders',
    'aplications.payments',   # ⚡ Tu nueva app de pagos (Mercado Pago)
    'aplications.reports',
    'core',
    'aplications.auditoria',
]

# -----------------------------------------------------------
# ⚙️ Middleware
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
# 🎨 Templates
# -----------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.carousel_slides',
                'core.context_processors.layout_meta',
            ],
        },
    },
]

WSGI_APPLICATION = 'rayo_shop.wsgi.application'

# -----------------------------------------------------------
# 💾 Base de datos (SQL Server)
# -----------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME": "Rayo indumentaria",
        "HOST": r"DESKTOP-QGF6VK9\SQLEXPRESS",
        "OPTIONS": {
            "driver": "ODBC Driver 17 for SQL Server",
            "trusted_connection": "yes",
        },
    }
}

AUTH_PASSWORD_VALIDATORS = []

# -----------------------------------------------------------
# 🌎 Localización
# -----------------------------------------------------------
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------------
# 🖼️ Archivos estáticos y media
# -----------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'core' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------------------------------------
# 💰 Mercado Pago (modo sandbox)
# -----------------------------------------------------------
# ✅ Usá el token de prueba desde .env
MERCADOPAGO_ACCESS_TOKEN = env("MP_ACCESS_TOKEN", default="TEST-xxxxxxxxxxxxxxxxxxxxxxxxxxxx")

# ✅ URL pública o de ngrok (para webhook)
SITE_URL = env("SITE_URL", default="http://127.0.0.1:8000")

# -----------------------------------------------------------
# 🎨 Jazzmin - panel administrativo
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
        {"name": "Inicio", "url": "admin:index", "icon": "fas fa-home"},
        {"name": "Ver sitio", "url": "/", "icon": "fas fa-globe"},
       {"name": "Reportes", "url": "/reports/", "icon": "fas fa-chart-line"},
    ],

    # Íconos para apps y modelos
    "icons": {
        "accounts": "fas fa-users",
        "catalog": "fas fa-tshirt",
        "orders": "fas fa-shopping-cart",
        "payments": "fas fa-credit-card",
        "reports": "fas fa-chart-line",
        "auth": "fas fa-user-shield",
    },

    # Orden y estructura de menú lateral
    "order_with_respect_to": ["accounts", "catalog", "orders", "payments", "reports"],

    # 🚫 Ocultamos modelos secundarios o técnicos
    "hide_models": [
    "accounts.PerfilUsuario",
    "accounts.UsuarioEstado",
    "accounts.Rol",
    "accounts.Funcion",
    "accounts.RolFuncion",
    ],
    # Enlaces rápidos personalizados
    "custom_links": {
        "reports": [{
            "name": "Ver reportes",
            "url": "/reports/",
            "icon": "fas fa-chart-line",
        }],
    },

    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    "language_chooser": False,
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


LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
