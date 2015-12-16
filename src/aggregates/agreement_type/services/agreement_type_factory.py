from django.utils import timezone

from src.libs.python_utils.id.id_utils import generate_id

from src.aggregates.agreement_type.models import AgreementType


def create_agreement_type(agreement_type_name, agreement_type_global, agreement_type_user_id):
  agreement_type_id = generate_id()
  agreement_type_system_created_date = timezone.now()

  agreement_type = AgreementType._from_attrs(agreement_type_id, agreement_type_name, agreement_type_global,
                                             agreement_type_user_id,
                                             agreement_type_system_created_date)

  return agreement_type
