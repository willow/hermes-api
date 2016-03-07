from src.domain.user.models import User
from src.domain.user.services import user_service
import logging
from django_rq import job
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def create_user_task(user_id, user_name, user_nickname, user_email, user_picture, user_attrs):
  # check if already exists - idempotent
  try:
    user_service.get_user_from_email(user_email)

    logger.debug('User already exists: %s', user_email)

  except User.DoesNotExist:

    log_message = (
      "Create user task for user_name: %s",
      user_name
    )

    with log_wrapper(logger.debug, *log_message):
      return user_service.create_user(user_id, user_name, user_nickname, user_email, user_picture, user_attrs).user_id
