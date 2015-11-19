import logging

from django_rq import job

from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job
def test_error_task(name='Hello'):
  log_message = (
    "Test error task for parameter: name: %s",
    name
  )
  try:
    raise Exception('This is an error!')
  except:
    logger.exception('this is an error log: %s', name)

  rq_logger = logging.getLogger('rq.worker')
  print('rq logger disabled = %s ' % rq_logger.disabled)
  try:
    raise Exception('This is an rq worker error!')
  except:
    rq_logger.exception('this is an rq worker error log: %s', name)

  with log_wrapper(logger.info, *log_message):
    raise Exception('ERRORR!@!@#!@# %s' % name)
