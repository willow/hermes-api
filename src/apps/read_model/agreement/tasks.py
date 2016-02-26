import logging

from django.forms.models import model_to_dict
from django_rq import job

from src.aggregates.agreement.models import Agreement
from src.apps.read_model.agreement import services
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def create_agreement_task_from_potential_agreement(potential_agreement_id):
  # check if already exists - idempotent

  try:
    # pa and agreements share same id
    services.get_agreement(potential_agreement_id)

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

      user_id = data.pop('user')
      data['user_id'] = user_id

      agreement_type_id = data.pop('agreement_type')
      data['agreement_type_id'] = agreement_type_id

      return services.create_agreement(**data).id


from django_rq import job
from src.aggregates.potential_agreement.services import potential_agreement_service


@job('default')
def send_alerts_for_agreements_task():
  # get list of agreements where the flag is enabled, not created, and date has passed
  agreement_ids_with_due_expiration_alerts = (
    services
      .get_agreements_with_due_expiration_alert()
      .values_list('id', flat=True)
    # putting values_list here and not in service becuase my thinking is if the service returns a django object list
    # then we can just return them. if you look at search_service, the service layer actually calls values_list but
    # this layer is returning a custom object (it includes count, results, etc).
  )

  agreement_ids_with_due_outcome_notice_alerts = (
    services
      .get_agreements_with_due_outcome_notice_alert()
      .values_list('id', flat=True)
  )

  exp_set = set(agreement_ids_with_due_expiration_alerts)
  outcome_set = set(agreement_ids_with_due_outcome_notice_alerts)
  ids = exp_set.union(outcome_set)

  # the reason i'm doing this in one task is that i'm worried about concurrency conflicts.
  # if we have a bunch of simultaneous tasks modifying the same instances, we could potentially overwrite bool flags
  # which would result in multiple emails going out.
  for ag_id in ids:
    send_alert_for_agreement_task.delay(ag_id)


@job('default')
def send_alert_for_agreement_task(agreement_id):
  ag = services.get_agreement(agreement_id)
  ag.send_expiration_alert_if_due()
  ag.send_outcome_notice_alert_if_due()
  services.save_or_update(ag)
