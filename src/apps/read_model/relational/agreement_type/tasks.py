import logging

from django_rq import job

from src.apps.read_model.relational.agreement_type import service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def save_topic_lookup_task(id, name, stem, collapsed_stem):
  log_message = ("topic_id: %s name: %s, stem: %s", id, name, stem)

  with log_wrapper(logger.info, *log_message):
    return service.save_topic_lookup(id, name, stem, collapsed_stem)
