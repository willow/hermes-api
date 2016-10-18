from src.apps.read_model.relational.agreement_type.models import GlobalAgreementType, AgreementTypeLookup
from src.apps.read_model.relational.agreement_type.models import UserAgreementType


def create_global_agreement_type(id, name, system_created_date):
  at = GlobalAgreementType(id=id, name=name, system_created_date=system_created_date)

  at.save()

  return at


def create_user_agreement_type(id, name, user_id, system_created_date):
  at = UserAgreementType(id=id, name=name, user_id=user_id, system_created_date=system_created_date)

  at.save()

  return at


def create_agreement_type_lookup(id, name):
  at = AgreementTypeLookup(id=id, name=name)

  at.save()

  return at


def get_user_agreement_type(agreement_type_id):
  return UserAgreementType.objects.get(id=agreement_type_id)


def get_global_agreement_type(agreement_type_id):
  return GlobalAgreementType.objects.get(id=agreement_type_id)


def get_global_agreement_types():
  return GlobalAgreementType.objects.all()


def get_agreement_type_lookup(agreement_type_id):
  return AgreementTypeLookup.objects.get(id=agreement_type_id)
