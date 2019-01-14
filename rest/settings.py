"""
Django settings for rest project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4-21pc=8iekadd63wvh12ayu)xfw#0-6a)8!huk#t95#6ybs!('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django.contrib.sites',
    'rest_auth',
    'rest_auth.registration',
    'rest_framework.authtoken',
    'post',
    'bot',
    'users',

]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ALLAUTH = {
    'ACCOUNT_EMAIL_VERIFICATION': 'none',
}

ROOT_URLCONF = 'rest.urls'

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

WSGI_APPLICATION = 'rest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES =  {'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_test',
        'USER': 'root',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '5432',
    }

    #{
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #}
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
            'simple': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
        },
        'loggers': {
            'bot': {
                'handlers': ['file1'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'users': {
                'handlers': ['file2'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
        'handlers': {
            'file1': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'logs', "bot.log"),
                'formatter': 'simple',
            },
            'file2': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'logs', 'users.log'),
                'formatter': 'simple',
            },
        },

    }


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_ID = 1

NUMBER_OF_USERS = 3
MAX_POSTS_PER_USER = 5
MAX_LIKES_PER_USER = 4

URL_POST = "http://127.0.0.1:8000/api/v1/posts/"
URL_LIKE = "http://127.0.0.1:8000/api/v1/posts/like/"
URL_TOKEN = "http://localhost:8000/api-token-auth/"
URL_SIGNUP = "http://localhost:8000/api/v1/registration/"

HUNTER_KEY = "c0a3ee15498dc4521cfbe2304898a34b0bae0051"
CLEARBIT_KEY = "sk_206285f2d558dbe9a2d864396cb9d215"