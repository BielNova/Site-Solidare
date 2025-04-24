from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega variáveis de ambiente do arquivo .env
load_dotenv(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

TARGET_ENV = os.getenv('TARGET_ENV', '')  # Valor padrão vazio se não existir
NOT_PROD = not TARGET_ENV.lower().startswith('prod')

# Configurações específicas para cada ambiente
if NOT_PROD:
    # Ambiente de desenvolvimento
    DEBUG = True
    SECRET_KEY = 'django-insecure-@ec)_2r9hm(7tk-tgwbqk29_8c5b!z%h@iy39(lxczmh4m8msr'
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', 'lispector-dyh0dfc6cegeetab.brazilsouth-01.azurewebsites.net']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Ambiente de produção
    SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-@ec)_2r9hm(7tk-tgwbqk29_8c5b!z%h@iy39(lxczmh4m8msr')
    DEBUG = os.getenv('DEBUG', '0').lower() in ['true', 't', '1']
    
    # Configuração de hosts permitidos
    default_hosts = 'localhost 127.0.0.1 [::1] lispector-dyh0dfc6cegeetab.brazilsouth-01.azurewebsites.net'
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', default_hosts).split(' ')
    
    # Configuração de origens confiáveis para CSRF
    default_origins = 'https://lispector-dyh0dfc6cegeetab.brazilsouth-01.azurewebsites.net'
    CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', default_origins).split(' ')

    # Configuração de redirecionamento SSL
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', '0').lower() in ['true', 't', '1']
    if SECURE_SSL_REDIRECT:
        SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Configuração do banco de dados PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DBNAME', 'defaultdb'),
            'HOST': os.environ.get('DBHOST', 'localhost'),
            'USER': os.environ.get('DBUSER', 'defaultuser'),
            'PASSWORD': os.environ.get('DBPASS', ''),
            'OPTIONS': {'sslmode': 'require'},
        }
    }

# Application definition
# Removido DEBUG = True que estava sobrescrevendo a configuração anterior

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
    "whitenoise.runserver_nostatic",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Movido para cima para funcionar corretamente
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = os.environ.get('DJANGO_STATIC_URL', "/static/")
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Mantida apenas uma definição de STATIC_ROOT

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configurações adicionais para resolver o problema de DisallowedHost no Azure
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# Configurações de segurança adicionais para produção
if not NOT_PROD:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 ano
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
