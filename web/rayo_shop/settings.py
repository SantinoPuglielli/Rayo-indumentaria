import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'aplications.catalog',
    'aplications.cart',
    'aplications.orders',
    'aplications.payments',
    'aplications.reports',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'core.middleware.UsuarioMiddleware',#
]

ROOT_URLCONF = 'rayo_shop.urls'

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

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.getenv('DB_NAME', 'RayoIndumentaria(15-9)'),
        'HOST': os.getenv('DB_HOST', r'localhost\SQLEXPRESS'),
        'PORT': os.getenv('DB_PORT', ''),  # En Express no suele hacer falta
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'trusted_connection': 'yes',
        },
    },
    'django_system': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'django_admin.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'core' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Mercado Pago / sitio
MP_ACCESS_TOKEN = os.getenv('MP_ACCESS_TOKEN','')
MP_WEBHOOK_SECRET = os.getenv('MP_WEBHOOK_SECRET','dev-secret')
SITE_URL = os.getenv('SITE_URL','http://127.0.0.1:8000')
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000','http://localhost:8000']


DATABASE_ROUTERS = ['rayo_shop.routers.DatabaseRouter']

# Sesiones en caché para evitar usar la BD
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'rayo-sessions',
    }
}