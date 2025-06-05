from pathlib import Path
import os
from dotenv import load_dotenv
from decouple import config # Certifique-se de que decouple está importado para ambos os ambientes

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega variáveis de ambiente do .env
# É uma boa prática carregar .env apenas para desenvolvimento local.
# No Azure, as variáveis de ambiente são configuradas diretamente no serviço de aplicativo.
if not os.environ.get('WEBSITE_SITE_NAME'): # Verifica se não está no Azure (exemplo simples)
    load_dotenv(BASE_DIR / '.env')

# Ambiente
TARGET_ENV = os.getenv('TARGET_ENV', '').lower() # Converte para minúsculas imediatamente
NOT_PROD = not TARGET_ENV.startswith('prod')

# Debug
# No Azure, é melhor desabilitar o DEBUG em produção por segurança.
# Use TARGET_ENV para controle mais explícito.
DEBUG = NOT_PROD # DEBUG será True em ambientes que não são 'prod'

# Chave secreta
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-@ec)_2r9hm(7tk-tgwbqk29_8c5b!z%h@iy39(lxczmh4m8msr')
# Para produção, garanta que SECRET_KEY seja uma variável de ambiente forte no Azure.

# Hosts permitidos
# Adicione os IPs de saúde do Azure e o hostname do seu aplicativo.
ALLOWED_HOSTS = [
    '127.0.0.1', # Localhost padrão para desenvolvimento local
    'localhost', # Localhost padrão para desenvolvimento local
    '169.254.129.2', # IP interno comum para verificações de saúde do Azure
    '169.254.129.4', # Outro IP interno comum para verificações de saúde do Azure
]

# Adiciona o hostname do Azure Web App se estiver disponível
AZURE_WEBAPP_HOST = os.getenv('WEBSITE_HOSTNAME')
if AZURE_WEBAPP_HOST:
    ALLOWED_HOSTS.append(AZURE_WEBAPP_HOST)

# Se você tiver domínios personalizados, adicione-os aqui
# ALLOWED_HOSTS.append('seu-dominio-personalizado.com')

# Origins Confiáveis para CSRF
# Adicione a URL HTTPS do seu aplicativo Azure e quaisquer domínios personalizados.
CSRF_TRUSTED_ORIGINS = [
    'https://lispector-dae9a7fqaxghgrfj.brazilsouth-01.azurewebsites.net',
]
if AZURE_WEBAPP_HOST:
    CSRF_TRUSTED_ORIGINS.append(f'https://{AZURE_WEBAPP_HOST}')
# Se você tiver um domínio personalizado, adicione-o aqui
# CSRF_TRUSTED_ORIGINS.append('https://seu-dominio-personalizado.com')


# Redirecionamento HTTPS
# Esta configuração já estava boa, apenas organizando para clareza.
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', '0').lower() in ['true', 't', '1']
if SECURE_SSL_REDIRECT:
    SECURE_PROXY_SSL_HEADER = ('X-Forwarded-Proto', 'https') # Cabeçalho correto para proxy


# Banco de dados
if NOT_PROD:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # `decouple.config` é bom para produção, assume que as variáveis de ambiente estão definidas.
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
    # Suas aplicações do core, certifique-se de que cada uma é um app Django válido
    'core.avisos',
    'core.user',
    'core.home',
    'core.professor',
    'core.aluno',
    'processo_seletivo',
    'widget_tweaks',
    'whitenoise.runserver_nostatic', # Adicionado para Whitenoise
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Certifique-se de que Whitenoise está aqui
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
        # Inclua o diretório de templates de nível superior do projeto para melhor organização
        'DIRS': [BASE_DIR / 'templates'], # Pode ser BASE_DIR / 'templates'
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug', # Bom para ter em DEBUG
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
LANGUAGE_CODE = 'pt-br' # Definido para português do Brasil
TIME_ZONE = 'America/Sao_Paulo' # Definido para o fuso horário de São Paulo
USE_I18N = True
USE_TZ = True

# Arquivos estáticos
STATIC_URL = os.environ.get('DJANGO_STATIC_URL', '/static/')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Adicione a configuração do Whitenoise para servir arquivos estáticos em produção
# if not DEBUG: # Não precisa deste 'if not DEBUG' se STATICFILES_STORAGE já está definido
#     STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Arquivos de mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Segurança de host e proxy
# Estas já estavam boas, mas certifique-se de que SECURE_PROXY_SSL_HEADER use 'X-Forwarded-Proto'
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('X-Forwarded-Proto', 'https')

# Autenticação
LOGIN_URL = '/user/login/'

# Tipo padrão de campo ID
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
