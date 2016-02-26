import logging

from django_rq import job

from src.apps.read_model.user import services
from src.apps.read_model.user.models import AuthUser
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def create_auth_user_task(version, id, email, system_created_date):
  # check if already exists - idempotent
  try:
    user = services.get_auth_user_from_email(email)

    logger.debug('User already exists: %s', email)

    return user.id

  except AuthUser.DoesNotExist:

    log_message = ("Create user task for email: %s", email)

    with log_wrapper(logger.debug, *log_message):
      return services.create_auth_user(id, email, system_created_date, version).id
