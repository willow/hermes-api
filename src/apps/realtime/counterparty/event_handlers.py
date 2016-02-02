from django.dispatch import receiver

from src.aggregates.potential_agreement.signals import completed, updated_attrs
from src.apps.realtime.counterparty.services import counterparty_tasks
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(completed)
@receiver(updated_attrs)
def potential_agreement_completed_callback(**kwargs):
  potential_agreement_id = kwargs.pop('potential_agreement_id')

  counterparty_tasks.save_counterparty_in_firebase_task.delay(potential_agreement_id)
