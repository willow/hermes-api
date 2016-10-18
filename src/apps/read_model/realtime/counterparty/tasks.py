import logging

from django_rq import job

from src.apps.read_model.realtime.counterparty import services
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def save_counterparty_in_firebase_task(agreement_id, user_id, counterparty):
  log_message = (
    "Save counterparty in firebase. agreement_id: %s", agreement_id
  )

  with log_wrapper(logger.info, *log_message):
    return services.save_counterparty_in_firebase(user_id, counterparty)
