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
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
  }
}

########## END CACHE CONFIGURATION

########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging

LOGGING['handlers']['console_handler'] = {
  'level': 'DEBUG',
  'class': 'logging.StreamHandler'
}

LOGGING['handlers']['file_handler'] = {
  'level': 'DEBUG',
  'class': 'logging.handlers.RotatingFileHandler',
  'filename': 'logs/app.log',
  'maxBytes': 1024 * 1024 * 5,  # 5 MB
  'backupCount': 5,
  'encoding': 'UTF-8',
}

LOGGING['handlers']['request_handler'] = {
  'level': 'DEBUG',
  'class': 'logging.handlers.RotatingFileHandler',
  'filename': 'logs/django_request.log',
  'maxBytes': 1024 * 1024 * 5,  # 5 MB
  'backupCount': 5,
  'encoding': 'UTF-8',
}

LOGGING['handlers']['exception_handler'] = {
  'level': 'ERROR',
  'class': 'logging.handlers.RotatingFileHandler',
  'filename': 'logs/error.log',
  'maxBytes': 1024 * 1024 * 5,  # 5 MB
  'backupCount': 5,
  'encoding': 'UTF-8',
}

app_logger = {
  'handlers': ['console_handler', 'file_handler', 'exception_handler'],
  'level': 'DEBUG',
  'propagate': False
}

LOGGING['loggers'] = {
  '': {
    'handlers': ['console_handler', 'file_handler', 'exception_handler'],
    'level': 'DEBUG',
    'propagate': True
  },
  'django.request': {
    'handlers': ['request_handler', 'exception_handler', 'console_handler'],
    'level': 'DEBUG',
    'propagate': False
  },
  'django.db.backends': {
    'level': 'INFO',
  },
  'src.aggregates': app_logger,
  'src.apps': app_logger,
  'src.libs': app_logger,
}
########## END LOGGING CONFIGURATION
