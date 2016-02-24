from django.utils import timezone
from src.aggregates.potential_agreement.models import PotentialAgreement
from src.aggregates.potential_agreement.services import potential_agreement_factory


def get_potential_agreement(id):
  return PotentialAgreement.objects.get(id=id)


def save_or_update(agreement):
  agreement.save(internal=True)


def create_potential_agreement(**kwargs):
  potential_agreement = potential_agreement_factory.create_potential_agreement(**kwargs)
  save_or_update(potential_agreement)
  return potential_agreement
