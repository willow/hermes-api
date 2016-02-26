import logging

from django_rq import job

from src.apps.realtime.user import services
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def save_user_info_in_firebase_task(user_id, name, nickname, email, picture):
  log_message = (
    "Update Firebase user info. user_id: %s ", user_id
  )

  with log_wrapper(logger.info, *log_message):
    return services.save_user_info_in_firebase(user_id, name, nickname, email, picture)
