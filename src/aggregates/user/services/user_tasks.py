from src.aggregates.user.services import user_service
import logging
from django_rq import job
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def create_user_task(user_name, user_nickname, user_email, user_picture, user_attrs):
  log_message = (
    "Create user task for user_name: %s",
    user_name
  )

  with log_wrapper(logger.debug, *log_message):
    return user_service.create_user(user_name, user_nickname, user_email, user_picture, user_attrs).user_uid
