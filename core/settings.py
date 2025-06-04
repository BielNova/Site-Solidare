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
    SECRET_KEY = os.getenv('SECRET_KEY', '&5a!rl#@#mkn+2%1s#01^3^f8n(i59^-@r#c(v=8e-j@g%2e_s')
    # Modificado para aceitar todos os hosts em ambiente de desenvolvimento
    ALLOWED_HOSTS = ['*']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    # === MODIFICAÇÃO: Ajustar STATICFILES_STORAGE para desenvolvimento ===
    # Em desenvolvimento, não queremos que o Whitenoise armazene arquivos staticos
    # para que as mudanças no CSS/JS sejam refletidas imediatamente.
    # O Django serve arquivos estáticos de STATICFILES_DIRS por padrão em DEBUG=True.
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

else:
    # Production settings
    SECRET_KEY = os.getenv('SECRET_KEY', '&5a!rl#@#mkn+2%1s#01^3^f8n(i59^-@r#c(v=8e-j@g%2e_s')
    # Esta linha define DEBUG para produção baseado na variável de ambiente
    DEBUG = os.getenv('DEBUG', '0').lower() in ['true', 't', '1']
    
    # Adicione seu domínio do Azure e o IP interno
    ALLOWED_HOSTS = ['lispector1-hjc6cvdjgedcakeb.brazilsouth-01.azurewebsites.net', '169.254.129.2', '169.254.130.4']
    CSRF_TRUSTED_ORIGINS = ['lispector1-hjc6cvdjgedcakeb.brazilsouth-01.azurewebsites.net']

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
    # === CONFIGURAÇÃO DE PRODUÇÃO: Whitenoise ===
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
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
    'whitenoise.runserver_nostatic'
    # pois ele é mais adequado para o MIDDLEWARE e vamos gerenciar
    # o STATICFILES_STORAGE condicionalmente.
    'core.professor',
    'widget_tweaks',
    # 'core.frequencia',
    # 'core.documentacao',
    'processo_seletivo', # Seu app, essencial para templates e models
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
    'whitenoise.middleware.WhiteNoiseMiddleware', # Mantenha o Whitenoise para produção
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Adicione BASE_DIR / 'templates' para templates globais se tiver
        'DIRS': [
            BASE_DIR / 'core' / 'user' / 'templates' / 'home',
            # Adicione aqui para que o Django procure na raiz dos templates
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True, # Isso já faz o Django procurar em 'app_name/templates/'
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

# === MODIFICAÇÃO: Definir STATICFILES_DIRS para o seu static global ===
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# STATIC_ROOT é o diretório onde `collectstatic` coleta todos os arquivos estáticos.
# Ele é usado principalmente para produção.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_collected') # Sugestão de nome para clareza

# STATICFILES_STORAGE está agora condicionalmente definido acima (dentro do IF/ELSE)

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configurações adicionais para resolver o problema de DisallowedHost no Azure
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

LOGIN_URL = '/user/login/'
