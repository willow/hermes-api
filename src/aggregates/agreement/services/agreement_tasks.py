from django.forms.models import model_to_dict
from src.aggregates.agreement.models import Agreement
from src.aggregates.agreement.services import agreement_service
import logging
from django_rq import job
from src.aggregates.potential_agreement.services import potential_agreement_service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def create_agreement_task_from_potential_agreement(potential_agreement_id):
  # check if already exists - idempotent

  try:
    # pa and agreements share same uid
    agreement_service.get_agreement(potential_agreement_id)

    logger.debug('Agreement already exists: %s', potential_agreement_id)

  except Agreement.DoesNotExist:

    log_message = (
      "Create agreement task for id: %s",
      potential_agreement_id
    )

    with log_wrapper(logger.debug, *log_message):
      potential_agreement = potential_agreement_service.get_potential_agreement(potential_agreement_id)

      # http://stackoverflow.com/questions/21925671/convert-django-model-object-to-dict-with-all-of-the-fields-intact
      data = model_to_dict(potential_agreement, fields=[field.name for field in potential_agreement._meta.fields])

      # for some reason model_to_dict converts a list to json
      # jsonfield.fields.JSONFieldBase#value_from_object calls json.dumps
      data['artifacts'] = potential_agreement.artifacts

      # don't need to pass in django id
      data.pop('id')

      user_id = data.pop('user')
      data['user_id'] = user_id

      agreement_type_id = data.pop('agreement_type')
      data['agreement_type_id'] = agreement_type_id

      return agreement_service.create_agreement(**data).uid
