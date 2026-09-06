"""Configuracion de SoundShop CL para la Evaluacion 1.

Esta entrega trabaja con datos JSON y no utiliza una base de datos. El carrito
se conserva temporalmente en una cookie firmada por Django.
"""

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-soundshop-cl-evaluacion-1-local"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver"]

INSTALLED_APPS = [
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "soundshop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.datos_globales",
            ],
        },
    },
]

WSGI_APPLICATION = "soundshop.wsgi.application"

# La Evaluacion 1 solicita datos simulados, sin conexion a base de datos.
DATABASES = {}

# Almacenamiento temporal del ejercicio, aislado del caché general.
CACHES = {
    'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'},
    'cuentas': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'soundshop-cuentas-locales',
        'OPTIONS': {'MAX_ENTRIES': 1000},
    },
}

LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Sesiones y mensajes sin tablas: adecuados para el prototipo de esta unidad.
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_NAME = "soundshop_session"
SESSION_COOKIE_HTTPONLY = True
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
