from pathlib import Path
import os
from configurations import values
from django.core.management.utils import get_random_secret_key
import configurations


class Base(configurations.Configuration):
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
    
    SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", get_random_secret_key())
    DEBUG = values.BooleanValue(True)
    ALLOWED_HOSTS = values.ListValue(os.environ.get('ALLOWED_HOSTS', '*').split(','))

    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'rest_framework',
        'corsheaders',
        'drf_spectacular',
        'driver_hos_logbook.apps.driver_hos_logbook',
    ]

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ]

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    ROOT_URLCONF = 'driver_hos_logbook.urls'
    WSGI_APPLICATION = 'driver_hos_logbook.wsgi.application'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.AllowAny',
        ],
        'DEFAULT_RENDERER_CLASSES': [
            'rest_framework.renderers.JSONRenderer',
        ],
        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    }

    SPECTACULAR_SETTINGS = {
        'TITLE': 'Driver HOS Logbook API',
        'DESCRIPTION': 'API for HOS-compliant smart routing and ELD logbook generation.',
        'VERSION': '1.0.0',
        'SERVE_INCLUDE_SCHEMA': False,
    }

    CORS_ALLOW_ALL_ORIGINS = True

    API_PREFIX = 'api/'
    API_VERSION = 'v1/'