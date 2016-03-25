from django.dispatch import receiver

from src.domain.agreement_type.events import AgreementTypeCreated1
from src.domain.agreement_type import tasks
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(AgreementTypeCreated1.event_signal)
def create_agreement_type(**kwargs):
  event = kwargs['event']
  at_id = kwargs['aggregate_id']

  if event.is_global:
    tasks.create_global_agreement_type_task.delay(at_id, event.name, event.system_created_date)
  else:
    tasks.create_user_agreement_type_task.delay(at_id, event.name, event.user_id, event.system_created_date)


@event_idempotent
@receiver(AgreementTypeCreated1.event_signal)
def create_agreement_type_lookup(**kwargs):
  event = kwargs['event']
  at_id = kwargs['aggregate_id']

  tasks.create_agreement_type_lookup_task.delay(at_id, event.name)
