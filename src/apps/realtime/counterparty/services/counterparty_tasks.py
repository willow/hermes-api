import logging

from django_rq import job

from src.apps.realtime.counterparty.services import counterparty_service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def save_counterparty_in_firebase_task(potential_agreement_id):
  log_message = (
    "Save counterparty in firebase. potential_agreement_id: %s", potential_agreement_id
  )

  with log_wrapper(logger.info, *log_message):
    return counterparty_service.save_counterparty_in_firebase(potential_agreement_id)
