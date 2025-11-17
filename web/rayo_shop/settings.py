import os
from pathlib import Path
import environ
from dotenv import load_dotenv
import sys
BASE_DIR = Path(_file_).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "aplications"))


# Load environment variables
load_dotenv(BASE_DIR / ".env")
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

# =======================
#  SECURITY
# =======================
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = [
    "www.rayoindumentaria.shop",
    "rayoindumentaria.shop",
    "127.0.0.1",
    "localhost",
]

CSRF_TRUSTED_ORIGINS = [
    "https://www.rayoindumentaria.shop",
    "https://rayoindumentaria.shop",
]

# =======================
#  INSTALLED APPS
# =======================
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Terceros
    "jazzmin",

    # Tus apps (con el path correcto)
    "aplications.accounts",
    "aplications.auditoria",
    "aplications.cart",
    "aplications.catalog",
    "aplications.orders",
    "aplications.payments",
    "aplications.reports",
]

# =======================
#  MIDDLEWARE
# =======================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "rayo_shop.urls"

# =======================
#  TEMPLATES
# =======================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "rayo_shop.wsgi.application"

# =======================
#  DATABASE (MariaDB)
# =======================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "OPTIONS": {
            "charset": "utf8mb4",
            "sql_mode": "STRICT_TRANS_TABLES",
        },
    }
}

# =======================
#  PASSWORDS
# =======================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =======================
#  LANGUAGE & TIMEZONE
# =======================
LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

# =======================
#  STATIC & MEDIA
# =======================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
# =======================
#  MERCADO PAGO
# =======================
MP_ACCESS_TOKEN = env("MP_ACCESS_TOKEN")
MP_PUBLIC_KEY = env("MP_PUBLIC_KEY")

# =======================
#  JAZZMIN
# =======================
JAZZMIN_SETTINGS = {
    "site_title": "Panel de Administración",
    "site_header": "Rayo Indumentaria",
    "site_brand": "Rayo Admin",
    "welcome_sign": "Bienvenido al Panel Administrativo",
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

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"