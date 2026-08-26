from pathlib import Path
import os
import json
import base64
import dj_database_url
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured
from google.oauth2 import service_account

# Load environment variables from .env
load_dotenv()

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        raise ImproperlyConfigured(f"Set the {var_name} environment variable.")

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key
SECRET_KEY = get_env_variable("DJANGO_SECRET_KEY")

# Debug and hosts
DEBUG = False

ALLOWED_HOSTS = [
    "event-planner-live-619e438f027c.herokuapp.com",
    "localhost",
    "127.0.0.1",
]

# Installed apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "planner",
    "accounts",
    "storages",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URLs and templates
ROOT_URLCONF = "event_planner.urls"

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

WSGI_APPLICATION = "event_planner.wsgi.application"


if os.getenv("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.config(
            default=os.getenv("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "planner" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


GS_BUCKET_NAME = os.getenv("GS_BUCKET_NAME")
GS_CREDENTIALS = None

if not DEBUG:
    
    encoded_json = os.getenv("GCS_CREDENTIALS_JSON")
    if encoded_json:
        decoded_json = base64.b64decode(encoded_json).decode("utf-8")
        credentials_info = json.loads(decoded_json)
        GS_CREDENTIALS = service_account.Credentials.from_service_account_info(credentials_info)

    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/"

else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

# Auth redirects
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# Session & CSRF cookies
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
    "https://event-planner-live-619e438f027c.herokuapp.com",
]

# Default primary key field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR',
    },
}


def generate_public_url(file):
    return f"https://storage.googleapis.com/{GS_BUCKET_NAME}/{file.name}"
