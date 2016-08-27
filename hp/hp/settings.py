"""
Django settings for hp project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

from datetime import timedelta

from django.contrib.messages import constants as messages
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'captcha',
    'mptt',  # Tree structure for MenuItem
    'tinymce',  # Rich text editor

    'core',
    'bootstrap',  # bootstrap enhancements
    'account',
]

MIDDLEWARE_CLASSES = [
    'core.middleware.SiteMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.TranslatedUrlConfigMiddleware',
]

ROOT_URLCONF = 'hp.urls'

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
                'core.context_processors.basic',
            ],
        },
    },
]

WSGI_APPLICATION = 'hp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
AUTH_USER_MODEL = 'account.User'
LOGIN_URL = reverse_lazy('account:login')
LOGIN_REDIRECT_URL = reverse_lazy('account:detail')

# Authenticate against the XMPP server
AUTHENTICATION_BACKENDS = [
    'django_xmpp_backends.auth_backends.XmppBackendBackend',
]

###################
# CUSTOM SETTINGS #
###################

# Override message tags to match bootstrap alert classes.
#       See: https://docs.djangoproject.com/en/1.10/ref/contrib/messages/#message-tags
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.DEBUG: 'info',
}

# How long confirmation emails remain valid
USER_CONFIRMATION_TIMEOUT = timedelta(hours=48)

################
# GPG settings #
################
GPG_KEYSERVER = 'pool.sks-keyservers.net'

# Default GPG backend configuration
GPG_BACKENDS = {
    'default': {
        'BACKEND': 'gpgmime.gpgme.GpgMeBackend',
        'HOME': os.path.join(ROOT_DIR, 'gnupg'),
        # Optional settings:
        #'PATH': '/home/...',  # Path to 'gpg' binary
        #'ALWAYS_TRUST': True,   # Ignore trust in all operations
        #'OPTIONS': {...},  # Any custom options for the specific backend implementation
    },
}

# Directory where public/private keys are stored for signing
GPG_KEYDIR = os.path.join(ROOT_DIR, 'gnupg-keys')

###################
# Celery settings #
###################
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
BROKER_URL = 'redis://localhost:6379/0'

####################
# CAPTCHA settings #
####################
ENABLE_CAPTCHAS = True
CAPTCHA_LENGTH = 8
CAPTCHA_FONT_SIZE = 32
CAPTCHA_TEXT_FIELD_TEMPLATE = 'core/captcha/text_field.html'

try:
    from .localsettings import *
except ImportError:
    pass

# Make sure GPG home directories exist
for backend, config in GPG_BACKENDS.items():
    if config.get('HOME') and not os.path.exists(config['HOME']):
        os.makedirs(config['HOME'])
if not os.path.exists(GPG_KEYDIR):
    os.makedirs(GPG_KEYDIR)
