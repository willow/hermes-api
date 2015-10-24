from src.aggregates.potential_agreement.models import PotentialAgreement
from src.aggregates.potential_agreement.services import potential_agreement_factory


def get_potential_agreement(potential_agreement_id):
  return PotentialAgreement.objects.get(potential_agreement_id=potential_agreement_id)


def save_or_update(agreement):
  agreement.save(internal=True)


def create_potential_agreement(potential_agreement_name, potential_agreement_artifacts, potential_agreement_user_id):
  agreement = potential_agreement_factory.create_potential_agreement(potential_agreement_name,
                                                                     potential_agreement_artifacts,
                                                                     potential_agreement_user_id)
  save_or_update(agreement)
  return agreement
