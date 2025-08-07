import os

from .base import *

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

CORS_ALLOWED_ORIGINS = [
    "http://190.210.137.203",
    "https://190.210.137.203",
    "http://190.210.137.203:3000",
    "https://190.210.137.203:3000",
    "http://190.210.137.203:8080",
    "https://190.210.137.203:8080",
    "http://mapa.oei.org.ar",
    "https://mapa.oei.org.ar",
    "http://mapa.oei.org.ar:3000",
    "https://mapa.oei.org.ar:3000",
    "http://mapa.oei.org.ar:8080",
    "https://mapa.oei.org.ar:8080",
]

CORS_ORIGIN_WHITELIST = [
    'http://190.210.137.203',
    'https://190.210.137.203',
    'http://190.210.137.203:3000',
    'https://190.210.137.203:3000',
    'http://190.210.137.203:8080',
    'https://190.210.137.203:8080',
    'http://mapa.oei.org.ar:3000',
    'https://mapa.oei.org.ar:3000',
    'http://mapa.oei.org.ar',
    'https://mapa.oei.org.ar',
    'http://mapa.oei.org.ar:8080',
    'https://mapa.oei.org.ar:8080',
    
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
    os.path.join(BASE_DIR, 'staticfiles'),
]
STATIC_ROOT = os.path.join(BASE_DIR, "static")
