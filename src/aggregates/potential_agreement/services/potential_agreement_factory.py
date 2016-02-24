from django.utils import timezone

from src.aggregates.potential_agreement.models import PotentialAgreement
from src.libs.python_utils.id.id_utils import generate_id


def create_potential_agreement(**kwargs):
  id = generate_id()
  system_created_date = timezone.now()

  data = dict({'id': id, 'system_created_date': system_created_date}, **kwargs)

  agreement = PotentialAgreement._from_attrs(**data)

  return agreement
