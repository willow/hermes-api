import logging

from django_rq import job

from src.apps.read_model.realtime.user import services
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def save_user_identity_in_firebase_task(user_id, name, nickname, email, picture):
  log_message = (
    "Update Firebase user identity. user_id: %s ", user_id
  )

  with log_wrapper(logger.info, *log_message):
    return services.save_user_identity_in_firebase(user_id, name, nickname, email, picture)


@job('high')
def save_user_subscription_in_firebase_task(user_id, is_subscribed):
  log_message = (
    "Update Firebase user subscription. user_id: %s ", user_id
  )

  with log_wrapper(logger.info, *log_message):
    return services.save_user_subscription_in_firebase(user_id, is_subscribed)
