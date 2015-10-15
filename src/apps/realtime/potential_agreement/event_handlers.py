from django.dispatch import receiver

from src.aggregates.potential_agreement.signals import created
from src.apps.realtime.potential_agreement.services import potential_agreement_tasks
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(created)
def user_created_callback(**kwargs):
  potential_agreement_id = kwargs.pop('potential_agreement_id')
  potential_agreement_name = kwargs.pop('potential_agreement_name')
  user_id = kwargs.pop('user_id')

  potential_agreement_tasks.save_potential_agreement_in_firebase_task.delay(
    potential_agreement_id, potential_agreement_name, user_id
  )
