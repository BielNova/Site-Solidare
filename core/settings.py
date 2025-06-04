from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

# Adicione esta linha para debug
print(f"TARGET_ENV: {os.getenv('TARGET_ENV')}")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# Modifique esta linha para fornecer um valor padrão
TARGET_ENV = os.getenv('TARGET_ENV', '')  # Valor padrão vazio se não existir
NOT_PROD = not TARGET_ENV.lower().startswith('prod')


if NOT_PROD:
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-@ec)_2r9hm(7tk-tgwbqk29_8c5b!z%h@iy39(lxczmh4m8msr')
    # Modificado para aceitar todos os hosts em ambiente de desenvolvimento
    ALLOWED_HOSTS = ['*']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Production settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-@ec)_2r9hm(7tk-tgwbqk29_8c5b!z%h@iy39(lxczmh4m8msr')
    # Esta linha define DEBUG para produção baseado na variável de ambiente
    DEBUG = os.getenv('DEBUG', '0').lower() in ['true', 't', '1']
    
    # Adicione seu domínio do Azure e o IP interno
    ALLOWED_HOSTS = ['lispector-dyh0dfc6cegeetab.brazilsouth-01.azurewebsites.net', '169.254.129.2', '169.254.130.4']
    CSRF_TRUSTED_ORIGINS = ['https://lispector-dyh0dfc6cegeetab.brazilsouth-01.azurewebsites.net']

    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', '0').lower() in ['true', 't', '1']

    if SECURE_SSL_REDIRECT:
        SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    from decouple import config

    # Configuração do banco de dados para produção
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DBNAME'),
            'HOST': config('DBHOST'),
            'USER': config('DBUSER'),
            'PASSWORD': config('DBPASS'),
            'OPTIONS': {'sslmode': 'require',}
        }
    }
    
# Application definition

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
    'whitenoise.runserver_nostatic',
    'core.professor',
    'widget_tweaks',
    # 'core.frequencia',
    # 'core.documentacao',
    'processo_seletivo',
    'core.aluno',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

STATIC_URL = os.environ.get('DJANGO_STATIC_URL', '/static/')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# STATICFILES_DIRS = [BASE_DIR / 'user/static'] # Comentado pois STATIC_ROOT é usado

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configurações adicionais para resolver o problema de DisallowedHost no Azure
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

LOGIN_URL = '/user/login/'

