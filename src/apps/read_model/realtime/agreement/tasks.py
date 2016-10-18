import logging

from django_rq import job

from src.apps.read_model.realtime.agreement import services as realtime_agreement_service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def save_agreement_edit_in_firebase_task(agreement_id, **kwargs):
  log_message = (
    "Update agreement edit in firebase. agreement_id: %s ", agreement_id
  )

  with log_wrapper(logger.info, *log_message):
    return realtime_agreement_service.save_agreement_edit_in_firebase(agreement_id, **kwargs)


@job('high')
def save_agreement_detail_in_firebase_task(agreement_id, **kwargs):
  log_message = (
    "Update agreement detail in firebase. agreement_id: %s ", agreement_id
  )

  with log_wrapper(logger.info, *log_message):
    return realtime_agreement_service.save_agreement_detail_in_firebase(agreement_id, **kwargs)


@job('high')
def save_user_agreement_in_firebase_task(agreement_id, **kwargs):
  log_message = (
    "Update user agreement in firebase. agreement_id: %s ", agreement_id
  )

  with log_wrapper(logger.info, *log_message):
    return realtime_agreement_service.save_user_agreement_in_firebase(agreement_id, **kwargs)


@job('default')
def save_agreement_alerts_in_firebase_task(agreement_id, **kwargs):
  log_message = (
    "Update agreement alerts in firebase. agreement_id: %s ", agreement_id
  )

  with log_wrapper(logger.info, *log_message):
    return realtime_agreement_service.save_agreement_alerts_in_firebase(agreement_id, **kwargs)


@job('default')
def delete_agreement_in_firebase_task(agreement_id, user_id, **kwargs):
  log_message = (
    "Delete agreement alerts in firebase. agreement_id: %s ", agreement_id
  )

  with log_wrapper(logger.info, *log_message):
    return realtime_agreement_service.delete_agreements_in_firebase(agreement_id, user_id, **kwargs)
