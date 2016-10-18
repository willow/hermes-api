import logging

from django_rq import job

from src.apps.read_model.realtime.agreement_type import services
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def save_global_agreement_types_in_firebase_task(user_id):
  log_message = (
    "Save global agreement types in firebase for user_id: %s", user_id
  )

  with log_wrapper(logger.info, *log_message):
    return services.save_global_agreement_types_in_firebase(user_id)


@job('high')
def save_user_agreement_types_in_firebase_task(agreement_type_id, name, user_id):
  log_message = (
    "Save user agreement types in firebase. agreement_type_id: %s", agreement_type_id
  )

  with log_wrapper(logger.info, *log_message):
    return services.save_user_agreement_types_in_firebase(agreement_type_id, name, user_id)
