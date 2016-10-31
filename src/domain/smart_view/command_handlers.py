from django.dispatch import receiver
from django.utils import timezone

from src.domain.smart_view.commands import UpdateSmartViewAttrs, CreateSmartView
from src.domain.smart_view.entities import SmartView
from src.libs.common_domain import aggregate_repository
from src.libs.python_utils.id.id_utils import generate_id


@receiver(CreateSmartView.command_signal)
def create_smart_view(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  system_created_date = timezone.now()
  id = command.id
  data = dict({'system_created_date': system_created_date, 'id': id}, **command.__dict__)

  sv = SmartView.from_attrs(**data)
  _aggregate_repository.save(sv, -1)


@receiver(UpdateSmartViewAttrs.command_signal)
def update_smart_view(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  command = kwargs['command']
  id = kwargs['aggregate_id']

  data = command.__dict__

  sv = _aggregate_repository.get(SmartView, id)
  version = sv.version
  sv.update_attrs(**data)
  _aggregate_repository.save(sv, version)
