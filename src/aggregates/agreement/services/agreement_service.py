from src.aggregates.agreement import factories


def save_or_update(agreement):
  agreement.save(internal=True)


def create_agreement(agreement_name):
  agreement = factories.create_agreement(agreement_name)
  save_or_update(agreement)
  return agreement
