from pathlib import Path
import os
from dotenv import load_dotenv

# Base
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# ENV
TARGET_ENV = os.getenv('TARGET_ENV', '').lower()
NOT_PROD = not TARGET_ENV.startswith('prod')

# Debug e chaves
DEBUG = NOT_PROD
SECRET_KEY = os.getenv('SECRET_KEY', 'chave-insegura-padrao')
ALLOWED_HOSTS = ['*'] if NOT_PROD else [
    'lispector1-hjc6cvdjgedcakeb.brazilsouth-01.azurewebsites.net',
    '169.254.129.2',
    '169.254.130.4',
]

# CSRF
if not NOT_PROD:
    CSRF_TRUSTED_ORIGINS = [
        'https://lispector1-hjc6cvdjgedcakeb.brazilsouth-01.azurewebsites.net',
    ]

# Banco de dados
if NOT_PROD:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    from decouple import config
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DBNAME'),
            'HOST': config('DBHOST'),
            'USER': config('DBUSER'),
            'PASSWORD': config('DBPASS'),
            'OPTIONS': {'sslmode': 'require'},
        }
    }

# Static
STATIC_URL = os.environ.get('DJANGO_STATIC_URL', '/static/')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_collected')

# Armazenamento estático
STATICFILES_STORAGE = (
    'django.contrib.staticfiles.storage.StaticFilesStorage'
    if NOT_PROD
    else 'whitenoise.storage.CompressedManifestStaticFilesStorage'
)

# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Segurança
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', '0').lower() in ['true', 't', '1']
if SECURE_SSL_REDIRECT:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

USE_X_FORWARDED_HOST = True

# Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.avisos',
    'core.user',
    'core.home',
    'core.professor',
    'core.aluno',
    'processo_seletivo',
    'widget_tweaks',
    'whitenoise.runserver_nostatic',  # Corrigido: mover para o final
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Corrigido: whitenoise deve vir logo após security
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'core' / 'user' / 'templates' / 'home',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# URLs / WSGI
ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

# Senhas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Idioma / Fuso
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Login
LOGIN_URL = '/user/login/'

# Default PK
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
