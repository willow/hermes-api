"""Development settings and globals."""

from os.path import join, normpath

from .common import *


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
from src.libs.text_utils.encoding.encoding_utils import base64decode

DEBUG = True
########## END DEBUG CONFIGURATION

########## AUTH CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = r"yfs9ltn_k(^z3%o2rh=bnn5z-midcr4q52bz&jg!b^&jtxf$gk"

JWT_SECRET = 'JWT Secret+++++++++++'  # this string prevent padding exception
JWT_SECRET = base64decode(JWT_SECRET)
JWT_AUDIENCE = 'JWT Audience'
########## END AUTH CONFIGURATION

########## DRF CONFIGURATION
JWT_AUTH = {
  'JWT_SECRET_KEY': JWT_SECRET,
  'JWT_AUDIENCE': JWT_AUDIENCE,
}
########## END DRF CONFIGURATION

########## CORS CONFIGURATION
CORS_ORIGIN_REGEX_WHITELIST = (
  '^http://localhost:\d{1,4}/?',
)
########## END CORS CONFIGURATION

########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': normpath(join(DJANGO_ROOT, 'default.db')),
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
  }
}

########## END DATABASE CONFIGURATION

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
  'default': {
    'BACKEND': 'django_redis.cache.RedisCache',
    'LOCATION': 'localhost:6379',
    'OPTIONS': {
      'DB': 0,
    }
  }
}
########## END CACHE CONFIGURATION

########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging

LOGGING['handlers']['console_handler'] = {
  'level': 'DEBUG',
  'class': 'rq.utils.ColorizingStreamHandler',
  # the diff between '()' and 'class' is that '()' could be a class OR some func. Refer to logging/config.py#695
  # http://stackoverflow.com/questions/9212228/using-custom-formatter-classes-with-pythons-logging-config-module
  'formatter': 'local_standard',
}

LOGGING['handlers']['file_handler'] = {
  'level': 'DEBUG',
  'class': 'logging.handlers.RotatingFileHandler',
  'filename': 'logs/app.log',
  'maxBytes': 1024 * 1024 * 5,  # 5 MB
  'backupCount': 5,
  'encoding': 'UTF-8',
  'formatter': 'local_standard'
}

LOGGING['handlers']['exception_handler'] = {
  'level': 'ERROR',
  'class': 'logging.handlers.RotatingFileHandler',
  'filename': 'logs/error.log',
  'maxBytes': 1024 * 1024 * 5,  # 5 MB
  'backupCount': 5,
  'encoding': 'UTF-8',
  'formatter': 'local_standard'
}

app_logger = {
  'handlers': ['console_handler', 'file_handler', 'exception_handler'],
  'level': 'DEBUG',
  'propagate': False
}

LOGGING['loggers'] = {
  '': app_logger,
  'django.request': app_logger,
  # django.request doesn't propagate by default https://docs.djangoproject.com/en/dev/topics/logging/#django-request
}
########## END LOGGING CONFIGURATION

########### FIREBASE CONFIGURATION
FIREBASE_SECRET = 'Firebase Secret'
FIREBASE_APP = 'Firebase App'
FIREBASE_DEBUG = True
########## END FIREBASE CONFIGURATION

########### AWS CONFIGURATION
AWS_ACCESS_KEY_ID = 'AWS_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY'
AWS_STORAGE_BUCKET_NAME = 'AWS_STORAGE_BUCKET_NAME'
########## END AWS CONFIGURATION
