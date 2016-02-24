from django.utils import timezone

from src.libs.python_utils.id.id_utils import generate_id

from src.aggregates.agreement_type.models import AgreementType


def create_agreement_type(name, is_global, user_id):
  id = generate_id()
  system_created_date = timezone.now()

  agreement_type = AgreementType._from_attrs(id, name, is_global, user_id, system_created_date)

  return agreement_type
