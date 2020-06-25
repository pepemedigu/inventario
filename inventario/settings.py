"""
Django settings for uca project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import os
import sys

# IMPORTANDO DATOS DE CONFIGURACIÓN
from .private import SERVERS, POSTGRES_DATABASE, POSTGRES_USER, POSTGRES_PASSWORD, AUTHENTICATION_BACKENDS, SIRE_USER, SIRE_PASSWORD

#Importar datos privados
#SERVERS
#POSTGRES_DATABASE=
#POSTGRES_USER=
#POSTGRES_PASSWORD=
#AUTHENTICATION_BACKENDS = No es necesario indicarlo si se usa el de Django
#SIRE_USER =  # Para backend autorizacon de la UCA
#SIRE_PASSWORD =

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

#SECRET_KEY = os.environ['SECRET_KEY']
SECRET_KEY = '+=2!kh4%mb7(-j#(emej^z%ibrcbxa8kr!)8k==$4x7*4g57h#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = SERVERS


# Application definition

INSTALLED_APPS = [
    'inventarioav',
    'widget_tweaks',
    'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inventario.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'inventario.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if True or 'test' in sys.argv or 'runserver' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            'ATOMIC_REQUESTS': True,
        }
    }
else:
    DATABASES = {
     'default': {
           'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': POSTGRES_DATABASE,
            'USER': POSTGRES_USER,
            'PASSWORD': POSTGRES_PASSWORD,
            'HOST': 'localhost',
            'PORT': '',
            'ATOMIC_REQUESTS': True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] [%(levelname)s] [%(module)s %(funcName)s:%(lineno)s]  %(message)s",
            'datefmt' : "%Y-%m-%d %H:%M:%S"
        },
        'normal': {
            'format': "[%(asctime)s] [%(levelname)s]  %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        'file_inventario': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/uca/inventario.log',
            'formatter': 'normal'
        },
        'file_inventario_error': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/uca/inventario.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'inventario': {
            'handlers': ['file_inventario'],
            'level': 'INFO',
            'propagate': True,
        },
        'inventario_error': {
            'handlers': ['file_inventario_error'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'

if 'test' in sys.argv or 'runserver' in sys.argv:
    SECURE_SSL_REDIRECT = False
else:
    SECURE_SSL_REDIRECT = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'