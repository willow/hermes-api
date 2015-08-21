from django_rq import job
from src.apps.read_model.models.user.services import user_service
from src.libs.python_utils.logging.logging_utils import log_wrapper
import logging

logger = logging.getLogger(__name__)


@job('high')
def save_user_info_in_firebase_task(user_id, user_name, user_nickname,
                                    user_email, user_picture):
  log_message = (
    "Update Firebase user info. user_id: %s ", user_id
  )

  with log_wrapper(logger.info, *log_message):
    return user_service.save_user_info_in_firebase(
      user_id, user_name, user_nickname,
      user_email, user_picture,
    )
