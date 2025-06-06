from pathlib import Path
import os
from dotenv import load_dotenv
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega variáveis de ambiente do .env SOMENTE se não estiver no Azure
# A variável WEBSITE_SITE_NAME é definida pelo Azure App Service
if not os.environ.get('WEBSITE_SITE_NAME'):
    load_dotenv(BASE_DIR / '.env')

# Adicione esta linha para debug (útil para logs de implantação)
print(f"TARGET_ENV: {os.getenv('TARGET_ENV', 'not_set')}")

# Modifique esta linha para fornecer um valor padrão
# Converte TARGET_ENV para minúsculas imediatamente para consistência
TARGET_ENV = os.getenv('TARGET_ENV', '').lower()
NOT_PROD = not TARGET_ENV.startswith('prod') # Será True se TARGET_ENV não começar com 'prod'

# Configurações comuns para todos os ambientes
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-@ec)_2r9hm(7tk-tgwbqk29_8c5b!z%h@iy39(lxczmh4m8msr')

# --- CONFIGURAÇÕES POR AMBIENTE ---
if NOT_PROD:
    # Configurações de DESENVOLVIMENTO
    DEBUG = True
    ALLOWED_HOSTS = ['*'] # Permite todos os hosts em desenvolvimento
    CSRF_TRUSTED_ORIGINS = [] # Não necessário em desenvolvimento com '*' em ALLOWED_HOSTS

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Configurações de PRODUÇÃO
    DEBUG = False # Sempre False em produção por segurança!

    # A URL explícita do seu aplicativo
    APP_HOSTNAME = 'lispector-dae9a7fqaxghgrfj.brazilsouth-01.azurewebsites.net'
    # Pega o hostname do ambiente do Azure, se disponível, para maior flexibilidade
    azure_webapp_env_host = os.getenv('WEBSITE_HOSTNAME')
    if azure_webapp_env_host:
        APP_HOSTNAME = azure_webapp_env_host # Sobrescreve se a variável de ambiente existir

    # Lista de hosts permitidos para produção.
    # Inclua IPs de saúde do Azure e o hostname do seu App Service.
    ALLOWED_HOSTS = [
        '127.0.0.1', # Loopback
        'localhost', # Loopback
        '169.254.129.2', # IP interno do Azure para health checks (comum)
        '169.254.129.4', # Outro IP interno comum do Azure
        APP_HOSTNAME, # Seu hostname principal
    ]
    # Se você tiver um domínio personalizado, adicione-o aqui também:
    # ALLOWED_HOSTS.append('seu-dominio-personalizado.com')

    # Origens confiáveis para CSRF em produção (use HTTPS)
    CSRF_TRUSTED_ORIGINS = [
        f'https://{APP_HOSTNAME}', # Seu hostname principal via HTTPS
    ]
    # Se você tiver um domínio personalizado, adicione-o aqui:
    # CSRF_TRUSTED_ORIGINS.append('https://seu-dominio-personalizado.com')


    # Redirecionamento HTTPS
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', '1').lower() in ['true', 't', '1'] # Padrão para True em produção

    if SECURE_SSL_REDIRECT:
        SECURE_PROXY_SSL_HEADER = ('X-Forwarded-Proto', 'https')
        USE_X_FORWARDED_HOST = True

    # Configuração do banco de dados PostgreSQL para produção
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

# --- FIM DAS CONFIGURAÇÕES POR AMBIENTE ---


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
    'core.professor',
    'core.aluno',
    'processo_seletivo',
    'widget_tweaks',
    'whitenoise.runserver_nostatic',
]

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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core' / 'user' / 'templates' / 'home'],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' },
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = os.environ.get('DJANGO_STATIC_URL', '/static/')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = '/user/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
