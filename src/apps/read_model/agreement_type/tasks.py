import logging
from django.core.exceptions import ObjectDoesNotExist

from django_rq import job
from src.apps.read_model.agreement_type import services

from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def create_agreement_type_task(id, name, is_global, user_id, system_created_date, version):
  # check if already exists - idempotent
  try:
    at = services.get_global_agreement_type(id)

    logger.debug('AgreementType already exists: %s', id)

    return at.id

  except ObjectDoesNotExist:
    log_message = ("Create agreement_type task for agreement_type_id: %s", id)

    with log_wrapper(logger.info, *log_message):
      return services.create_agreement_type(id, name, is_global, user_id, system_created_date, version).id
