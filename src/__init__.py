import logging
from django_rq import job
import rq
import django_rq

@job('high')
def test(a=None):
  log = logging.getLogger(__name__)
  log.warn('hi. i am running now')
  log.info('hi. i am running now')
  return 'hiello there {0}'.format(a)
