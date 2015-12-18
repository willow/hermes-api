import logging

from django_rq import job

from src.apps.realtime.agreement_type.services import agreement_type_service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def save_agreement_types_in_firebase_task(user_id):
  log_message = (
    "Save agreement types in firebase. user_id: %s", user_id
  )

  with log_wrapper(logger.info, *log_message):
    return agreement_type_service.save_agreement_types_in_firebase(user_id)
