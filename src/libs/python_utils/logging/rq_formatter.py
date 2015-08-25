import logging
from rq import get_current_job


class RqFormatter(logging.Formatter):
  # http://celery.readthedocs.org/en/latest/_modules/celery/app/log.html
  # http://python-rq.org/docs/jobs/
  # https://github.com/nvie/rq/blob/02c6df6a45b4afb025bc635eb289424b60ddf1ec/rq/worker.py#L615

  def __init__(self, job_format=None, no_job_format=None, datefmt=None, style='%'):
    super().__init__(job_format, datefmt, style)
    self._no_job_style = self._style.__class__(no_job_format)

  def format(self, record):
    job = get_current_job()

    if job:
      record.__dict__.update(job_name=job.func_name, job_queue=job.origin, job_id=job.id)

    return super().format(record)

  def formatMessage(self, record):

    if hasattr(record, 'job_name'):
      ret_val = super().formatMessage(record)
    else:
      ret_val = self._no_job_style.format(record)

    return ret_val
