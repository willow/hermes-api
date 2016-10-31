from django.dispatch import receiver
from django.utils import timezone

from src.domain.potential_agreement.commands import CreatePotentialAgreement, CompletePotentialAgreement
from src.domain.potential_agreement.entities import PotentialAgreement
from src.libs.common_domain import aggregate_repository
from src.libs.python_utils.id.id_utils import generate_id


@receiver(CreatePotentialAgreement.command_signal)
def create_potential_agreement(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  system_created_date = timezone.now()
  id = generate_id()
  data = dict({'system_created_date': system_created_date, 'id': id}, **command.__dict__)

  pa = PotentialAgreement.from_attrs(**data)
  _aggregate_repository.save(pa, -1)


@receiver(CompletePotentialAgreement.command_signal)
def complete_potential_agreement(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  command = kwargs['command']
  id = kwargs['aggregate_id']

  data = command.__dict__

  pa = _aggregate_repository.get(PotentialAgreement, id)
  version = pa.version
  pa.complete(**data)
  _aggregate_repository.save(pa, version)
