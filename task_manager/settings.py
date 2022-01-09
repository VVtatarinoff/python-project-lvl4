"""
Django settings for task_manager project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
import rollbar
from django.utils.translation import gettext_lazy as _

load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
ROLL_KEY = os.getenv("ROLL_KEY")
DEBUG = (os.getenv('DEBUG') == 'True')
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

ALLOWED_HOSTS = ['localhost',
                 'ancient-gorge-78100.herokuapp.com',
                 'www.ancient-gorge-78100.herokuapp.com',
                 '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['http://webserver:9000']
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'task_manager.apps.TMConfig',
    'bootstrap4',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]

ROLLBAR = {
    'access_token': ROLL_KEY,
    'environment': 'development' if DEBUG else 'production',
    'branch': 'main',
    'root': BASE_DIR,
}

rollbar.init(**ROLLBAR)

ROOT_URLCONF = 'task_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
OPTIONS = {
    'libraries': {
        'admin.urls': 'django.contrib.admin.templatetags.admin_urls',
    },
}
WSGI_APPLICATION = 'task_manager.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
db_from_env = dj_database_url.config(conn_max_age=500)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# Heroku: Update database configuration from $DATABASE_URL.
DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [{
    'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa 501
},
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 3}
    },  # noqa 125
]
#  {
#     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', # noqa 501
#     },
#     {
#     NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', # noqa 501
#     },
LOGOUT_REDIRECT_URL = 'home'
# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian'))
)

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'task_manager')
STATIC_URL = '/static/'
# Extra places for collectstatic to find static files.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            'filters': ['require_debug_true'],
            "class": "logging.StreamHandler",
        },
        'rollbar': {
            'filters': ['require_debug_false'],
            'access_token': ROLL_KEY,
            'environment': 'production',
            'class': 'rollbar.logger.RollbarHandler'
        },

    },
    "loggers": {
        "django": {
            "handlers": ["console", 'rollbar'],
            "level": "INFO",
            "propagate": True},
        "task_manager": {
            "handlers": ["console", 'rollbar'],
            "level": "DEBUG",
            "propagate": True},

    }
}
