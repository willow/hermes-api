from django_rq import job
from src.apps.auth.providers.auth0.services import auth0_service
from src.libs.python_utils.logging.logging_utils import log_wrapper
import logging

logger = logging.getLogger(__name__)


@job('high')
def save_user_id_in_auth0_task(auth0_user_id, user_id):
  log_message = (
    "Update Auth0 user_id. auth0_user_id: %s user_id: %s ", auth0_user_id, user_id
  )

  with log_wrapper(logger.info, *log_message):
    return auth0_service.save_user_id_in_auth0(auth0_user_id, user_id)['user_id']
