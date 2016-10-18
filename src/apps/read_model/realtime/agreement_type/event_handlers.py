from django.dispatch import receiver

from src.apps.read_model.realtime.agreement_type import tasks
from src.domain.agreement_type.events import AgreementTypeCreated1
from src.domain.user.events import UserCreated1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(UserCreated1.event_signal)
def execute_user_created_1(**kwargs):
  user_id = kwargs['aggregate_id']
  tasks.save_global_agreement_types_in_firebase_task.delay(user_id)


@event_idempotent
@receiver(AgreementTypeCreated1.event_signal)
def agreement_type_created_callback(**kwargs):
  event = kwargs['event']
  at_id = kwargs['aggregate_id']

  if not event.is_global:
    tasks.save_user_agreement_types_in_firebase_task.delay(at_id, event.name, event.user_id)
