from src.aggregates.agreement.services import agreement_factory


def save_or_update(agreement):
  agreement.save(internal=True)


def create_agreement(agreement_name):
  agreement = agreement_factory.create_agreement(agreement_name)
  save_or_update(agreement)
  return agreement
