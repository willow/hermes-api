from django.utils import timezone

from src.aggregates.agreement.models import Agreement
from src.apps.read_model.agreement.services import agreement_factory


def save_or_update(agreement):
  agreement.save(internal=True)


def get_agreement(agreement_id):
  return Agreement.objects.get(id=agreement_id)


def create_agreement(**kwargs):
  agreement = agreement_factory.create_agreement(**kwargs)
  save_or_update(agreement)
  return agreement


def get_agreements_with_due_expiration_alert():
  ret_val = Agreement.objects.filter(
    expiration_alert_date__lte=timezone.now(),
    expiration_alert_enabled=True,
    expiration_alert_created=False
  )
  return ret_val


def get_agreements_with_due_outcome_notice_alert():
  ret_val = Agreement.objects.filter(
    outcome_notice_alert_date__lte=timezone.now(),
    outcome_notice_alert_enabled=True,
    outcome_notice_alert_created=False
  )
  return ret_val
