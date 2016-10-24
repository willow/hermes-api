import logging

from django_rq import job

from src.apps.read_model.realtime.smart_view import services
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def save_smart_view_in_firebase_task(smart_view_id, name, query, user_id):
  log_message = (
    "Save smart view in firebase. smart_view_id: %s", smart_view_id
  )

  with log_wrapper(logger.info, *log_message):
    return services.save_smart_view_in_firebase(smart_view_id, name, query, user_id)
