"""Common settings and globals."""
from src.apps.auth.providers.auth0.utils import get_user_id_from_jwt
import src.settings.constants as constants

from os.path import abspath, dirname, basename
# http://stackoverflow.com/questions/21631878/celery-is-there-a-way-to-write-custom-json-encoder-decoder

########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
from src.libs.python_utils.logging.rq_formatter import RqFormatter

DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Site name:
SITE_NAME = basename(DJANGO_ROOT)
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

CONSTANTS = constants
########## END GENERAL CONFIGURATION

########## STORAGE CONFIGURATION
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_HEADERS = {
  'Cache-Control': 'max-age=31536000',  # 1 year
}

AWS_DEFAULT_ACL = None  # Not public by default
########## END STORAGE CONFIGURATION

########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION

########## AUTH CONFIGURATION
AUTH_USER_MODEL = 'user.User'
########## END AUTH CONFIGURATION

########## CORS CONFIGURATION
CORS_ALLOW_HEADERS = (
  'x-requested-with',
  'content-type',
  'accept',
  'origin',
  'authorization',
  'x-csrftoken',
  'user-agent',
  'accept-encoding',
  'Cache-Control'  # dropzone requires this header
)
########## END CORS CONFIGURATION

########## DRF CONFIGURATION
REST_FRAMEWORK = {
  'DEFAULT_PERMISSION_CLASSES': (
    'rest_framework.permissions.IsAuthenticated',
  ),
  'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
  ),
}

JWT_AUTH = {
  'JWT_PAYLOAD_GET_USERNAME_HANDLER': get_user_id_from_jwt
}
########## END DRF CONFIGURATION

########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
  # Use GZip compression to reduce bandwidth.
  'django.middleware.gzip.GZipMiddleware',
  'corsheaders.middleware.CorsMiddleware',
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

  # Storage
  'storages',

  # Database

  # Analytics

  # Rest API
  'rest_framework',

  # Headers
  'corsheaders',
)

LOCAL_APPS = (
  # AGGREGATES
  'src.aggregates.agreement',
  'src.aggregates.agreement_type',
  'src.aggregates.alert',
  'src.aggregates.asset',
  'src.aggregates.potential_agreement',
  'src.aggregates.smart_view',
  'src.aggregates.user',

  # APPS
  'src.apps.agreement_translation',
  'src.apps.api',
  'src.apps.auth',
  'src.apps.realtime',

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
      '()': RqFormatter,
      'job_format': '[%(asctime)s - %(name)s - %(job_name)s - %(job_queue)s - %(job_id)s - %(levelname)s] %(message)s',
      'no_job_format': '[%(asctime)s - %(name)s - %(levelname)s] %(message)s',
      # the 'Xs' is used for padding. To include the bracket in the string, I think we'll need a custom formatter.
      'datefmt': '%Y-%m-%d %H:%M:%S'
      # timezone is utc. I believe this is because django overrides the localtime to use TIME_ZONE = 'UTC'
    },
    'standard': {
      '()': RqFormatter,
      'job_format': '[%(name)s - %(job_name)s - %(job_queue)s - %(job_id)s - %(levelname)s] %(message)s',
      'no_job_format': '[%(name)s - %(levelname)s] %(message)s',
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

########## EMAIL CONFIGURATION
DEV_EMAIL_ADDRESS = 'dev@startwillow.com'
########## END EMAIL CONFIGURATION
