import logging

from django_rq import job
from src.aggregates.potential_agreement.services import potential_agreement_service

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
def save_agreement_detail_in_firebase_task(potential_agreement_id):
  log_message = (
    "Update agreement detail in firebase. potential_agreement_id: %s ", potential_agreement_id
  )

  with log_wrapper(logger.info, *log_message):
    return agreement_service.save_agreement_detail_in_firebase(potential_agreement_id)


@job('high')
def save_user_agreement_in_firebase_task(potential_agreement_id):
  log_message = (
    "Update user agreement in firebase. potential_agreement_id: %s ", potential_agreement_id
  )

  with log_wrapper(logger.info, *log_message):
    return agreement_service.save_user_agreement_in_firebase(potential_agreement_id)


@job('default')
def save_agreement_alerts_in_firebase_task(potential_agreement_id):
  potential_agreement = potential_agreement_service.get_potential_agreement(potential_agreement_id)
  agreement_service.save_agreement_alerts_in_firebase(potential_agreement)
  return None
