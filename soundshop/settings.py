"""Configuración de la tienda sin base de datos."""
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# La clave de firma cambia al iniciar el servidor: no queda una clave pública
# capaz de fabricar sesiones de administrador en un proyecto descargado.
SECRET_KEY = secrets.token_urlsafe(48)
# Verificadores, no credenciales legibles. El mismo acceso funciona en otra copia
# del proyecto sin distribuir la contraseña ni una configuración privada.
SOUNDSHOP_ADMIN_USERNAME_HASH = "pbkdf2_sha256$1000000$CbVgiSs5nJl0nsfOTpY9e3$uWXtlAe2yNLRU2HjN2ejvAxroS+/PBIwOGpygBmfe84="
SOUNDSHOP_ADMIN_PASSWORD_HASH = "pbkdf2_sha256$1000000$Okl8tBnr4owAoOv8mKHbyt$8D+Api5GFFQlgQimm2tvyC6cwjQz44CJ0EkMJVuiI5U="
SOUNDSHOP_ADMIN_ENABLED = True
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]

# Aplicaciones generadas por startproject y aplicación creada con startapp.
INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "core.apps.CoreConfig",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "soundshop.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [], "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]
WSGI_APPLICATION = "soundshop.wsgi.application"
# La guía deja la conexión y persistencia para otra evaluación.
DATABASES = {}
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_NAME = "soundshop_session_v2"
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"
LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
