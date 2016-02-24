from src.aggregates.user.models import User
from src.aggregates.user.services import user_service
import logging
from django_rq import job
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def create_user_task(id, name, nickname, email, picture, attrs):
  # check if already exists - idempotent
  try:
    user_service.get_user_from_email(email)

    logger.debug('User already exists: %s', email)

  except User.DoesNotExist:

    log_message = (
      "Create user task for name: %s",
      name
    )

    with log_wrapper(logger.debug, *log_message):
      return user_service.create_user(id, name, nickname, email, picture, attrs).id
