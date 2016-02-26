from src.apps.read_model.agreement_type.models import UserAgreementType, GlobalAgreementType


def create_agreement_type(id, name, is_global, user_id, system_created_date, version):
  if is_global:
    at = GlobalAgreementType(id=id, name=name, system_created_date=system_created_date, version=version)
  else:
    at = UserAgreementType(id=id, name=name, user_id=user_id, system_created_date=system_created_date, version=version)

  at.save()

  return at


def get_user_agreement_type(agreement_type_id):
  return UserAgreementType.objects.get(id=agreement_type_id)


def get_global_agreement_type(agreement_type_id):
  return GlobalAgreementType.objects.get(id=agreement_type_id)


def get_global_agreement_types():
  return GlobalAgreementType.objects.all()
