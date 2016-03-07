import logging

from django.core.exceptions import ObjectDoesNotExist

from django_rq import job

from src.domain.agreement_type import services
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def create_global_agreement_type_task(id, name, system_created_date):
  # check if already exists - idempotent
  try:
    at = services.get_global_agreement_type(id)

    logger.debug('GlobalAgreementType already exists: %s', id)

    return at.id

  except ObjectDoesNotExist:
    log_message = ("Create global agreement_type task for agreement_type_id: %s", id)

    with log_wrapper(logger.info, *log_message):
      return services.create_global_agreement_type(id, name, system_created_date).id


@job('high')
def create_user_agreement_type_task(id, name, user_id, system_created_date):
  # check if already exists - idempotent
  try:
    at = services.get_user_agreement_type(id)

    logger.debug('UserAgreementType already exists: %s', id)

    return at.id

  except ObjectDoesNotExist:
    log_message = ("Create user agreement_type task for agreement_type_id: %s", id)

    with log_wrapper(logger.info, *log_message):
      return services.create_user_agreement_type(id, name, user_id, system_created_date).id


@job('high')
def create_agreement_type_lookup_task(id, name):
  # check if already exists - idempotent
  try:
    at = services.get_agreement_type_lookup(id)

    logger.debug('AgreementTypeLookup already exists: %s', id)

    return at.id

  except ObjectDoesNotExist:
    log_message = ("Create agreement_type_lookup task for agreement_type_id: %s", id)

    with log_wrapper(logger.info, *log_message):
      return services.create_agreement_type_lookup(id, name).id
