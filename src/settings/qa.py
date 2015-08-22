"""Production settings and globals."""

import os
import sys

import dj_database_url
from src.libs.text_utils.text_parser import str2bool
from .common import *


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False
########## END DEBUG CONFIGURATION

########## ALLOWED HOSTS CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.herokuapp.com', 'qa.api.startwillow.com']
########## END ALLOWED HOST CONFIGURATION

# ######### DATABASE CONFIGURATION
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

LOGGING['handlers']['console_handler'] = {
  'level': APP_LOG_LEVEL,
  'class': 'rq.utils.ColorizingStreamHandler',
  'stream': sys.stdout,  # http://stackoverflow.com/questions/11866322/heroku-logs-for-django-projects-missing-errors
  'formatter': 'standard',
}

LOGGING['handlers']['exception_handler'] = {
  'level': 'ERROR',
  'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
}

app_logger = {
  'handlers': ['console_handler', 'exception_handler'],
  'level': APP_LOG_LEVEL,
  'propagate': False
}

LOGGING['loggers'] = {
  '': app_logger
}

########## END LOGGING CONFIGURATION

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = os.environ['SECRET_KEY']
########## END SECRET CONFIGURATION

########### FIREBASE CONFIGURATION
FIREBASE_SECRET = os.environ['FIREBASE_SECRET']
FIREBASE_APP = os.environ['FIREBASE_APP']
FIREBASE_DEBUG = str2bool(os.environ['FIREBASE_DEBUG'])
########## END FIREBASE CONFIGURATION
