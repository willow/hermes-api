"""Development settings and globals."""

from os.path import join, normpath

from .common import *


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
########## END DEBUG CONFIGURATION

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = r"yfs9ltn_k(^z3%o2rh=bnn5z-midcr4q52bz&jg!b^&jtxf$gk"
########## END SECRET CONFIGURATION

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
