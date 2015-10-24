from django.dispatch import receiver

from src.aggregates.potential_agreement.signals import created, completed
from src.apps.realtime.agreement.services import agreement_tasks
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(created)
def potential_agreement_created_callback(**kwargs):
  potential_agreement_id = kwargs.pop('potential_agreement_id')

  agreement_tasks.save_agreement_edit_in_firebase_task.delay(potential_agreement_id)


@event_idempotent
@receiver(completed)
def potential_agreement_completed_callback(**kwargs):
  potential_agreement_id = kwargs.pop('potential_agreement_id')

  agreement_tasks.save_agreement_edit_in_firebase_task.delay(potential_agreement_id)
