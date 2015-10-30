import logging

from django_rq import job

from src.apps.realtime.agreement.services import agreement_service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def save_agreement_edit_in_firebase_task(potential_agreement_id):
  log_message = (
    "Update agreement edit in firebase. potential_agreement_id: %s ", potential_agreement_id
  )

  with log_wrapper(logger.info, *log_message):
    return agreement_service.save_agreement_edit_in_firebase(potential_agreement_id)


@job('high')
def save_dashboard_agreement_in_firebase_task(potential_agreement_id):
  log_message = (
    "Update dashboard agreement in firebase. potential_agreement_id: %s ", potential_agreement_id
  )

  with log_wrapper(logger.info, *log_message):
    return agreement_service.save_dashboard_agreement_in_firebase(potential_agreement_id)
