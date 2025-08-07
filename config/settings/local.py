from .base import *
import os
from django.core.management.utils import get_random_secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

ALLOWED_HOSTS = [
    'localhost',
]

CORS_ALLOWED_ORIGINS = [
    "https://localhost:3000",
    "http://localhost:3000",
    "https://localhost:80",
    "http://localhost:80",
    "https://190.210.137.203:3000",
    "http://190.210.137.203:3000",
    "https://190.210.137.203:80",
    "http://190.210.137.203:80",
    "https://mapa.oei.org.ar:3000",
    "http://mapa.oei.org.ar:3000",
    "https://mapa.oei.org.ar:80",
    "http://mapa.oei.org.ar:80",
]

CORS_ORIGIN_WHITELIST = [
    'https://localhost:3000',
    'http://localhost:3000',
    'https://localhost:80',
    'http://localhost:80',
    'https://190.210.137.203:3000',
    'http://190.210.137.203:3000',
    'https://190.210.137.203:80',
    'http://190.210.137.203:80',
    'https://mapa.oei.org.ar:3000',
    'http://mapa.oei.org.ar:3000',
    'https://mapa.oei.org.ar:80',
    'http://mapa.oei.org.ar:80',
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': "django.contrib.gis.db.backends.postgis",
        'NAME': os.getenv("POSTGRES_DBNAME"),
        'USER': os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
        'HOST': os.getenv("POSTGRES_HOST"),
        'PORT': os.getenv("POSTGRES_PORT"),
    },
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
