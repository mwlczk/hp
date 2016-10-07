"""
Django settings for hp project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import ipaddress
import os

from datetime import timedelta

from celery.schedules import crontab
from django.contrib.messages import constants as messages
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from core.constants import ACTIVITY_REGISTER
from core.constants import ACTIVITY_FAILED_LOGIN
from core.constants import ACTIVITY_RESET_PASSWORD

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
    'xmpp_http_upload',  # XEP-0363

    'core',
    'bootstrap',  # bootstrap enhancements
    'account',  # account management
    'feed',  # RSS/Atom feeds
    'jsxc',  # webchat
    'conversejs',  # webchat2
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
    'core.middleware.CeleryMessageMiddleware',
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

MEDIA_URL = '/media/'
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
# The second class is the django default, needed in django admin.
MESSAGE_TAGS = {
    messages.ERROR: 'danger error',
    messages.DEBUG: 'info debug',
}

XMPP_HOSTS = {}
CONTACT_ADDRESS = None
DEFAULT_XMPP_HOST = None
DEFAULT_FROM_EMAIL = None

# How long confirmation emails remain valid
USER_CONFIRMATION_TIMEOUT = timedelta(hours=48)

LOG_FORMAT = '[%(asctime).19s %(levelname)-8s] %(message)s'  # .19s = only first 19 chars
LIBRARY_LOG_LEVEL = 'WARN'
LOG_LEVEL = 'INFO'

FACEBOOK_PAGE = ''
TWITTER_HANDLE = ''

################
# GPG settings #
################
GPG_KEYSERVER = 'http://pool.sks-keyservers.net:11371'

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

# Directory where public/private keys are stored for signing.
GPG_KEYDIR = os.path.join(BASE_DIR, 'gpg-keys')

###################
# Celery settings #
###################
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_SEND_TASK_ERROR_EMAILS = True

# Periodic tasks
CELERYBEAT_SCHEDULE = {
    'core cleanup': {
        'task': 'core.tasks.cleanup',
        'schedule': crontab(hour=3, minute=0),
    },
    'account cleanup': {
        'task': 'account.tasks.cleanup',
        'schedule': crontab(hour=3, minute=5),
    },
}
CELERYD_LOG_FORMAT = None
CELERYD_TASK_LOG_FORMAT = None

######################
# Anti-Spam settings #
######################

# Captchas
ENABLE_CAPTCHAS = True
CAPTCHA_LENGTH = 8
CAPTCHA_FONT_SIZE = 32
CAPTCHA_TEXT_FIELD_TEMPLATE = 'core/captcha/text_field.html'

# DNSBL lists
DNSBL = (
    'sbl.spamhaus.org',
    'xbl.spamhaus.org',
    'proxies.dnsbl.sorbs.net',
    'spam.abuse.ch',
    'cbl.abuseat.org',
)

# Ratelimit
RATELIMIT_CONFIG = {
    ACTIVITY_REGISTER: (
        (timedelta(hours=1), 3, ),
        (timedelta(days=1), 5, ),
    ),
    ACTIVITY_FAILED_LOGIN: (
        (timedelta(minutes=30), 3, ),
    ),
    ACTIVITY_RESET_PASSWORD: (
        (timedelta(minutes=30), 3, ),
    ),
}
SPAM_BLACKLIST = set()

####################
# Privacy settings #
####################
USER_LOGENTRY_EXPIRES = timedelta(days=31)

try:
    from .localsettings import *  # NOQA
except ImportError:
    pass

# Make sure some required settings are set
if not XMPP_HOSTS:
    raise ImproperlyConfigured("The XMPP_HOSTS setting is undefined.")
if not CONTACT_ADDRESS:
    raise ImproperlyConfigured("The CONTACT_ADDRESS setting is undefined.")
if not DEFAULT_XMPP_HOST:
    raise ImproperlyConfigured("The DEFAULT_XMPP_HOST setting is undefined.")
elif DEFAULT_XMPP_HOST not in XMPP_HOSTS:
    raise ImproperlyConfigured("Host named by DEFAULT_XMPP_HOST is not defined in XMPP_HOSTS.")
if not DEFAULT_FROM_EMAIL:
    raise ImproperlyConfigured("The DEFAULT_FROM_EMAIL setting is undefined.")

if CELERYD_LOG_FORMAT is None:
    CELERYD_LOG_FORMAT = LOG_FORMAT
if CELERYD_TASK_LOG_FORMAT is None:
    # The default includes the task_name
    CELERYD_TASK_LOG_FORMAT = '[%(asctime).19s %(levelname)-8s] [%(task_name)s] %(message)s'

SPAM_BLACKLIST = set([ipaddress.ip_network(addr) for addr in SPAM_BLACKLIST])

# Make sure GPG home directories exist
for backend, config in GPG_BACKENDS.items():
    if config.get('HOME') and not os.path.exists(config['HOME']):
        os.makedirs(config['HOME'])
if not os.path.exists(GPG_KEYDIR):
    os.makedirs(GPG_KEYDIR)

# set some defaults for XMPP_HOSTS
for key, config in XMPP_HOSTS.items():
    config['NAME'] = key
    config.setdefault('ALLOWED_HOSTS', [])
    config.setdefault('ALLOW_EMAIL', False)
    config.setdefault('BRAND', key)
    config.setdefault('CANONICAL_BASE_URL', 'https://%s' % key)
    config.setdefault('CONTACT_ADDRESS', CONTACT_ADDRESS)
    config.setdefault('DEFAULT_FROM_EMAIL', DEFAULT_FROM_EMAIL)
    config.setdefault('REGISTRATION', True)

if not ALLOWED_HOSTS:
    for config in XMPP_HOSTS.values():
        ALLOWED_HOSTS += XMPP_HOSTS.get('ALLOWED_HOSTS', [])


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'simple': {
            'format': LOG_FORMAT,
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'account': {'level': LOG_LEVEL, },
        'bootstrap': {'level': LOG_LEVEL, },
        'core': {'level': LOG_LEVEL, },
        'jsxc': {'level': LOG_LEVEL, },
        'gpgmime': {'level': LOG_LEVEL, },
    },
    'root': {
        'handlers': ['console', ],
        'level': LIBRARY_LOG_LEVEL,
    },
}
