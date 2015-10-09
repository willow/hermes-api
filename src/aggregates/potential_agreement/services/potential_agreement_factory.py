from django.utils import timezone
from src.aggregates.potential_agreement.models import PotentialAgreement

from src.libs.python_utils.id.id_utils import generate_id

from src.aggregates.agreement.models import Agreement


def create_potential_agreement(potential_agreement_name, potential_agreement_artifacts, user_id):
  potential_agreement_id = generate_id()
  system_created_date = timezone.now()

  agreement = PotentialAgreement._from_attrs(potential_agreement_id, potential_agreement_name,
                                             potential_agreement_artifacts,
                                             user_id,
                                             system_created_date)

  return agreement
