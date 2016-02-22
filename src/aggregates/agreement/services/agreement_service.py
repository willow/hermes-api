from src.aggregates.agreement.models import Agreement
from src.aggregates.agreement.services import agreement_factory


def save_or_update(agreement):
  agreement.save(internal=True)


def get_agreement(agreement_id):
  return Agreement.objects.get(uid=agreement_id)


def create_agreement(**kwargs):
  agreement = agreement_factory.create_agreement(**kwargs)
  save_or_update(agreement)
  return agreement
