from src.aggregates.agreement_type.models import AgreementType
from src.aggregates.agreement_type.services import agreement_type_factory


def save_or_update(agreement_type):
  agreement_type.save(internal=True)


def create_agreement_type(name, is_global, user_uid):
  agreement_type = agreement_type_factory.create_agreement_type(name, is_global, user_uid)
  save_or_update(agreement_type)
  return agreement_type


def get_agreement_type(agreement_type_uid):
  return AgreementType.objects.get(uid=agreement_type_uid)


def get_global_agreement_types():
  return AgreementType.objects.filter(is_global=True)
