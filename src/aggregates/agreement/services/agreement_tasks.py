from src.aggregates.agreement.services import agreement_service
import logging
from django_rq import job
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def create_agreement_task(agreement_name):
  log_message = (
    "Create agreement task for agreement_name: %s",
    agreement_name
  )

  with log_wrapper(logger.info, *log_message):
    return agreement_service.create_agreement(agreement_name).agreement_id
