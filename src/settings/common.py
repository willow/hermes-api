"""Common settings and globals."""
from os.path import abspath, dirname
# http://stackoverflow.com/questions/21631878/celery-is-there-a-way-to-write-custom-json-encoder-decoder

########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:

DJANGO_ROOT = dirname(dirname(abspath(__file__)))
########## END PATH CONFIGURATION

########## GENERAL CONFIGURATION
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

APP_NAME = 'hermes'
########## END GENERAL CONFIGURATION

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
  'src.aggregates.agreement',
  'src.aggregates.user',

  # APPS
  'src.apps.auth',
  'src.apps.read_model',

  # LIBS
  'src.libs.common_domain',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
########## END APP CONFIGURATION

########## LOGGING CONFIGURATION
LOGGING = {
  'version': 1,
  'disable_existing_loggers': True,
  'formatters': {
    'local_standard': {
      'format': '[%(asctime)s - %(name)s.%(funcName)s - %(levelname)s] %(message)s',
      # the 'Xs' is used for padding. To include the bracket in the string, I think we'll need a custom formatter.
      'datefmt': '%Y-%m-%d %H:%M:%S'
      # timezone is utc. I believe this is because django overrides the localtime to use TIME_ZONE = 'UTC'
    },
    'standard': {
      'format': '[%(name)s.%(funcName)s - %(levelname)s] %(message)s',
    },
  },
  'handlers': {}
}
########## END LOGGING CONFIGURATION

########### EXTERNAL API CONFIGURATION
HTTP_TIMEOUT = 10  # seconds
########## END EXTERNAL API CONFIGURATION

########### REDIS QUEUE CONFIGURATION
# The actual config of the redis cache location is env-specific. However, the queues themselves are app specific.
# Within our app, we'll decide whether to use high, default, low.
RQ_QUEUES = {
  'high': {
    'USE_REDIS_CACHE': 'default',
  },
  'default': {
    'USE_REDIS_CACHE': 'default',
  }
}
########## END REDIS QUEUE CONFIGURATION
