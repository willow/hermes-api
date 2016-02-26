import logging

from django.core.exceptions import ObjectDoesNotExist
from django_rq import job

from src.apps.read_model.agreement import services
from src.aggregates.potential_agreement.services import potential_agreement_service
from src.apps.realtime.agreement.services import agreement_service as realtime_agreement_service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


def _get_agreement(agreement_id):
  try:
    agreement = services.get_agreement(agreement_id)
  except ObjectDoesNotExist:
    try:
      agreement = potential_agreement_service.get_potential_agreement(agreement_id)
    except ObjectDoesNotExist as e:
      raise Exception('Agreement with id: {0} does not exist.'.format(agreement_id)).with_traceback(e.__traceback__)

  return agreement


@job('high')
def save_agreement_edit_in_firebase_task(agreement_id):
  log_message = (
    "Update agreement edit in firebase. agreement_id: %s ", agreement_id
  )

  with log_wrapper(logger.info, *log_message):
    agreement = _get_agreement(agreement_id)
    return realtime_agreement_service.save_agreement_edit_in_firebase(agreement)


@job('high')
def save_agreement_detail_in_firebase_task(agreement_id):
  log_message = (
    "Update agreement detail in firebase. agreement_id: %s ", agreement_id
  )

  with log_wrapper(logger.info, *log_message):
    agreement = services.get_agreement(agreement_id)
    return realtime_agreement_service.save_agreement_detail_in_firebase(agreement)


@job('high')
def save_user_agreement_in_firebase_task(agreement_id):
  log_message = (
    "Update user agreement in firebase. agreement_id: %s ", agreement_id
  )

  with log_wrapper(logger.info, *log_message):
    agreement = services.get_agreement(agreement_id)
    return realtime_agreement_service.save_user_agreement_in_firebase(agreement)


@job('default')
def save_agreement_alerts_in_firebase_task(agreement_id):
  log_message = (
    "Update agreement alerts in firebase. agreement_id: %s ", agreement_id
  )

  with log_wrapper(logger.info, *log_message):
    agreement = services.get_agreement(agreement_id)
    return realtime_agreement_service.save_agreement_alerts_in_firebase(agreement)
