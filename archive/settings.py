'''
Django settings for archive project.

Generated by 'django-admin startproject' using Django 3.2.15.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
'''

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (BASE_DIR / 'secret.key').read_text('utf-8')

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['*']

ARCHIVE_SERVER = os.environ.get('ARCHIVE_SERVER', 'DEVELOPMENT')
ARCHIVE_POSTGRESQL = {
    'HOST': os.environ.get('ARCHIVE_DB_HOST', '127.0.0.1'),
    'PORT': os.environ.get('ARCHIVE_DB_PORT', '5432'),
    'USER': os.environ.get('ARCHIVE_DB_USER', 'srv'),
    'PASSWORD': os.environ.get('ARCHIVE_DB_PASSWORD', ''),
    'NAME': os.environ.get('ARCHIVE_DB_NAME', 'archive'),
}
ARCHIVE_FILE_PATH = Path(
    os.environ.get(
        'ARCHIVE_FILE_PATH',
        BASE_DIR / 'static',
    ))
ARCHIVE_FILE_URL_PREFIX = os.environ.get('ARCHIVE_FILE_URL_PREFIX', '/static')

if ARCHIVE_SERVER.startswith('DEVELOPMENT'):
    ARCHIVE_SERVER = 'DEVELOPMENT'
    print('-----ARCHIVE_SERVER is DEVELOPMENT-----')
    DEBUG = True
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }
else:
    ARCHIVE_SERVER = 'PRODUCTION'
    print('-----ARCHIVE_SERVER is PRODUCTION-----')
    DEBUG = False
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': ARCHIVE_POSTGRESQL['NAME'],
            'USER': ARCHIVE_POSTGRESQL['USER'],
            'PASSWORD': ARCHIVE_POSTGRESQL['PASSWORD'],
            'HOST': ARCHIVE_POSTGRESQL['HOST'],
            'PORT': ARCHIVE_POSTGRESQL['PORT'],
        },
    }

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'archive_web',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'archive.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'archive.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static_root'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_TIMEZONE = TIME_ZONE
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_BROKER_URL = f"amqp://{os.getenv('ARCHIVE_MQ_HOST', '127.0.0.1')}:{os.getenv('ARCHIVE_MQ_PORT', 5672)}"
REDIS_URI = f"redis://{os.getenv('ARCHIVE_REDIS_HOST', '127.0.0.1')}:{os.getenv('ARCHIVE_REDIS_PORT', 6379)}"
CELERY_RESULT_BACKEND = f'{REDIS_URI}/0'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':
    10,
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
}
