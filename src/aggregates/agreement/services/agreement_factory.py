from django.utils import timezone

from src.libs.python_utils.id.id_utils import generate_id

from src.aggregates.agreement.models import Agreement


def create_agreement(agreement_name):
  agreement_id = generate_id()
  system_created_date = timezone.now()

  agreement = Agreement._from_attrs(agreement_id, agreement_name, system_created_date)

  return agreement
