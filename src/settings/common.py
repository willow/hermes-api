"""Common settings and globals."""
from os.path import abspath, dirname
from sys import path
# http://stackoverflow.com/questions/21631878/celery-is-there-a-way-to-write-custom-json-encoder-decoder

# ######### PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:

DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
# ######### END PATH CONFIGURATION

# ######### GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# ######### END GENERAL CONFIGURATION

########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
  # Use GZip compression to reduce bandwidth.
  'django.middleware.gzip.GZipMiddleware',
)
########## END MIDDLEWARE CONFIGURATION

########## APP CONFIGURATION
DJANGO_APPS = (
  # Default Django apps:

  # Useful template tags:

  # Admin panel and documentation:
)

THIRD_PARTY_APPS = (
  # Static file management:

  # Asynchronous task queue:
  'django_rq',

  # Database

  # Analytics

  # Rest API

  # Headers
)

LOCAL_APPS = (
  # AGGREGATES

  # APPS

  # LIBS
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
########## END APP CONFIGURATION


########## LOGGING CONFIGURATION

LOGGING = {
  'version': 1,
  'disable_existing_loggers': True,
  'handlers': {}
}
########## END LOGGING CONFIGURATION

########### EXTERNAL API CONFIGURATION
HTTP_TIMEOUT = 10  # seconds
########## END EXTERNAL API CONFIGURATION
