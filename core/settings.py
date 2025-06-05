from pathlib import Path
import os
from dotenv import load_dotenv

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega variáveis de ambiente do .env
load_dotenv(BASE_DIR / '.env')

# Ambiente
TARGET_ENV = os.getenv('TARGET_ENV', '')  # Valor padrão vazio se não definido
NOT_PROD = not TARGET_ENV.lower().startswith('prod')

# Debug
DEBUG = NOT_PROD if NOT_PROD else os.getenv('DEBUG', '0').lower() in ['true', 't', '1']

# Chave secreta
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-@ec)_2r9hm(7tk-tgwbqk29_8c5b!z%h@iy39(lxczmh4m8msr')

# Hosts permitidos
if NOT_PROD:
    ALLOWED_HOSTS = ['*']
    CSRF_TRUSTED_ORIGINS = []
else:
    ALLOWED_HOSTS = [
        'lispector-dae9a7fqaxghgrfj.brazilsouth-01.azurewebsites.net',
        '169.254.129.2',
        '169.254.130.4',
    ]
    CSRF_TRUSTED_ORIGINS = [
        'https://lispector-dae9a7fqaxghgrfj.brazilsouth-01.azurewebsites.net',
    ]

# Redirecionamento HTTPS
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', '0').lower() in ['true', 't', '1']
if SECURE_SSL_REDIRECT:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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

# Aplicações instaladas
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
    'whitenoise.runserver_nostatic',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLs principais
ROOT_URLCONF = 'core.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core' / 'user' / 'templates' / 'home'],
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

# WSGI
WSGI_APPLICATION = 'core.wsgi.application'

# Validação de senha
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalização
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Arquivos estáticos
STATIC_URL = os.environ.get('DJANGO_STATIC_URL', '/static/')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Arquivos de mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Segurança de host e proxy
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Autenticação
LOGIN_URL = '/user/login/'

# Tipo padrão de campo ID
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
