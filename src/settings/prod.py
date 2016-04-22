"""Production settings and globals."""

import os
import sys

import dj_database_url
from src.libs.text_utils.encoding.encoding_utils import base64decode
from src.libs.text_utils.text_parser import str2bool
from .common import *


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False
########## END DEBUG CONFIGURATION

########## ALLOWED HOSTS CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.herokuapp.com', 'api.startwillow.com']
########## END ALLOWED HOST CONFIGURATION

########## CORS CONFIGURATION
CORS_ORIGIN_REGEX_WHITELIST = (
  '^https:\/\/app\.startwillow\.com\/?',
)
########## END CORS CONFIGURATION

########## DATABASE CONFIGURATION
DATABASES = {'default': dj_database_url.config()}

# See: https://docs.djangoproject.com/en/dev/ref/databases/#persistent-database-connections
CONN_MAX_AGE = 60
########## END DATABASE CONFIGURATION

########## CACHE CONFIGURATION
CACHES = {
  'default': {
    'BACKEND': 'django_redis.cache.RedisCache',
    'LOCATION': os.environ['REDISCLOUD_URL'],
  }
}
########## END CACHE CONFIGURATION

########## LOGGING CONFIGURATION
APP_LOG_LEVEL = os.environ.get('APP_LOG_LEVEL', 'INFO')

RAYGUN_APIKEY = os.environ['RAYGUN_APIKEY']

LOGGING['handlers']['console_handler'] = {
  'level': APP_LOG_LEVEL,
  'class': 'rq.utils.ColorizingStreamHandler',
  'stream': sys.stdout,  # http://stackoverflow.com/questions/11866322/heroku-logs-for-django-projects-missing-errors
  'formatter': 'standard',
}

LOGGING['handlers']['exception_handler'] = {
  'level': 'ERROR',
  'class': 'raygun4py.raygunprovider.RaygunHandler',
  'apiKey': RAYGUN_APIKEY
}

app_logger = {
  'handlers': ['console_handler', 'exception_handler'],
  'level': APP_LOG_LEVEL,
  'propagate': False
}

LOGGING['loggers'] = {
  '': app_logger,
  'django.request': app_logger,
  # django.request doesn't propagate by default https://docs.djangoproject.com/en/dev/topics/logging/#django-request
  'rq.worker': app_logger,
  # rq.worker is explicitly defined here because it's imported in common.py before logging is configured and is
  # subsequently disabled (disable_existing_loggers=True) so we need to provide an entry here to enable it.
}
########## END LOGGING CONFIGURATION

########## AUTH CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = os.environ['SECRET_KEY']
JWT_SECRET = os.environ['JWT_SECRET']
JWT_SECRET = base64decode(JWT_SECRET)
JWT_AUDIENCE = os.environ['JWT_AUDIENCE']
########## END AUTH CONFIGURATION

########## DRF CONFIGURATION
JWT_AUTH['JWT_SECRET_KEY'] = JWT_SECRET
JWT_AUTH['JWT_AUDIENCE'] = JWT_AUDIENCE
########## END DRF CONFIGURATION

########### FIREBASE CONFIGURATION
FIREBASE_SECRET = os.environ['FIREBASE_SECRET']
FIREBASE_APP = os.environ['FIREBASE_APP']
FIREBASE_DEBUG = str2bool(os.environ['FIREBASE_DEBUG'])
########## END FIREBASE CONFIGURATION

########### AWS CONFIGURATION
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
########## END AWS CONFIGURATION

########## PAYMENT CONFIGURATION
STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']
########## END PAYMENT CONFIGURATION
