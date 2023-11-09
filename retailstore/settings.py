"""
Django settings for retailstore project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from decouple import config
import boto3
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
from django.core.management.utils import get_random_secret_key

try: 
    SECRET_KEY = config('SECRET_KEY')
    os.environ['SECRET_KEY'] = SECRET_KEY
    print("try: "+ SECRET_KEY)
except:
    SECRET_KEY = get_random_secret_key()
    os.environ['SECRET_KEY'] = SECRET_KEY
    config.__setattr__('SECRET_KEY', SECRET_KEY)
    print("except: "+ SECRET_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'category',
    'accounts',
    'store',
    'carts',
    'orders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'retailstore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'category.context_processors.menu_links',
                'carts.context_processors.counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'retailstore.wsgi.application'

AUTH_USER_MODEL = 'accounts.Account'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Initialize secrets manager
secrets = boto3.client('secretsmanager', region_name=config("AWS_DEFAULT_REGION"))
response = secrets.get_secret_value(
    SecretId=config('AWS_DATABASE_SECRET_ID')
)
database_secrets = json.loads(response['SecretString'])

dbhost = database_secrets['host']
dbport = database_secrets['port']
dbuser = database_secrets['username']
dbpass = database_secrets['password']
dbname = database_secrets['name']

# RDS Aurora Postgres Configuration
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': dbname,
            'USER': dbuser,
            'PASSWORD': dbpass,
            'HOST': dbhost,
            'PORT': dbport,
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

AWS_CLOUDFRONT_DOMAIN = config('AWS_CLOUDFRONT_DOMAIN')
AWS_LOCATION = 'static'

STATIC_URL = 'https://%s/%s/' % (AWS_CLOUDFRONT_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'retailstore.storage_backends.StaticStorage'

DEFAULT_FILE_STORAGE = 'retailstore.storage_backends.PublicMediaStorage'

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: "danger",
}

DEFAULT_AUTO_FIELD='django.db.models.AutoField'