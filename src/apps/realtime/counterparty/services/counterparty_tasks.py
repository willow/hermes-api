import logging

from django_rq import job
from src.aggregates.agreement.services import agreement_service

from src.apps.realtime.counterparty.services import counterparty_service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def save_counterparty_in_firebase_task(agreement_id):
  log_message = (
    "Save counterparty in firebase. agreement_id: %s", agreement_id
  )

  with log_wrapper(logger.info, *log_message):
    agreement = agreement_service.get_agreement(agreement_id)

    return counterparty_service.save_counterparty_in_firebase(agreement)
