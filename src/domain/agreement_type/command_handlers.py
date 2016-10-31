from django.dispatch import receiver
from django.utils import timezone

from src.domain.agreement_type.commands import CreateAgreementType
from src.domain.agreement_type.entities import AgreementType
from src.libs.common_domain import aggregate_repository
from src.libs.python_utils.id.id_utils import generate_id


@receiver(CreateAgreementType.command_signal)
def create_agreement_type(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  system_created_date = timezone.now()
  id = command.id
  data = dict({'system_created_date': system_created_date, 'id': id}, **command.__dict__)

  at = AgreementType.from_attrs(**data)
  _aggregate_repository.save(at, -1)
