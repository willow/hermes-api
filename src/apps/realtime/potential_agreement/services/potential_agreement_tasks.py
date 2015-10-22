import logging

from django_rq import job
from src.apps.realtime.potential_agreement.services import potential_agreement_service

from src.apps.realtime.user.services import user_service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def save_potential_agreement_in_firebase_task(potential_agreement_id, potential_agreement_name,
                                              potential_agreement_user_id):
  log_message = (
    "Update Firebase potential_agreement. potential_agreement_id: %s ", potential_agreement_id
  )

  with log_wrapper(logger.info, *log_message):
    return potential_agreement_service.save_potential_agreement_in_firebase(potential_agreement_id,
                                                                            potential_agreement_name,
                                                                            potential_agreement_user_id)
