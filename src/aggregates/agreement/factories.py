from src.aggregates.agreement.models import Agreement


def create_agreement(agreement_name):
  agreement = Agreement._from_attrs(agreement_name)

  return agreement
