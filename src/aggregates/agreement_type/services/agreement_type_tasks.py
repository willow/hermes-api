from src.aggregates.agreement_type.services import agreement_type_service
import logging
from django_rq import job
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def create_agreement_type_task(agreement_type_name):
  log_message = (
    "Create agreement_type task for agreement_type_name: %s",
    agreement_type_name
  )

  with log_wrapper(logger.info, *log_message):
    return agreement_type_service.create_agreement_type(agreement_type_name).agreement_type_id
