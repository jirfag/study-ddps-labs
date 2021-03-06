"""
Django settings for oauth_provider project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&x@z^)cv15(m5=zu@ops3jyerd8#atcjco9zm#g0gcpwg2+^#p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth_provider',
    'accounts',
    'api',
    'bootstrap3',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oauth_provider.auth_middleware.OauthMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'oauth_provider.auth_backend.OauthBackend',
)

ROOT_URLCONF = 'oauth_provider.urls'

WSGI_APPLICATION = 'oauth_provider.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'templates', 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

LOGIN_URL = '/accounts/login'
AFTER_REG_REDIRECT_URL = '/'
DEFAULT_LOGIN_REDIRECT_URL = '/'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
AUTH_USER_MODEL = 'accounts.User'
ACCESS_TOKEN_EXPIRATION_TIME = 2000 #secs
AUTHORIZATION_CODE_EXPIRATION_TIME = 20 #secs
REFRESH_TOKEN_EXPIRATION_TIME = 180000 #secs

LOGGING = {
  'version': 1,
  'formatters': {
    'simple': {
      'format': '%(levelname)s %(message)s'
    },
  },
  'handlers': {
    'console':{
      'level': 'DEBUG',
      'class': 'logging.StreamHandler',
      'formatter': 'simple'
    },
  },
  'loggers': {
    'django': {
      'handlers': ['console'],
      'propagate': True,
      'level': 'DEBUG',
    },
    'django.request': {
      'handlers': ['console'],
      'level': 'DEBUG',
      'propagate': False,
    },
  }
}

IMAGES_PER_PAGE = 2
TAGS_PER_PAGE = 3
