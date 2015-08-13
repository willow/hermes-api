"""Production settings and globals."""

import dj_database_url
import os

import sys
import urllib.parse

from .common import *

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False
########## END DEBUG CONFIGURATION

# ######### DATABASE CONFIGURATION
DATABASES = {'default': dj_database_url.config()}

# See: https://docs.djangoproject.com/en/dev/ref/databases/#persistent-database-connections
CONN_MAX_AGE = 60
########## END DATABASE CONFIGURATION

########## CACHE CONFIGURATION
redis_url = urllib.parse.urlparse(os.environ.get('REDISCLOUD_URL'))
CACHES = {
  'default': {
    'BACKEND': 'django_redis.cache.RedisCache',
    'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
    'OPTIONS': {
      'PASSWORD': redis_url.password,
      'DB': 0,
    }
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
  '': {
    'handlers': ['console_handler'],
    'level': 'WARNING',
    'propagate': True
  },
  'django.db.backends': {
    'level': APP_LOG_LEVEL,
  },
  'rq.worker': {
    'level': 'INFO'
  },
  'src.aggregates': app_logger,
  'src.apps': app_logger,
  'src.libs': app_logger,
}

########## END LOGGING CONFIGURATION

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = os.environ['SECRET_KEY']
########## END SECRET CONFIGURATION
