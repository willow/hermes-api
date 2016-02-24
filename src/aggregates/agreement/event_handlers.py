from django.dispatch import receiver

from src.aggregates.agreement.services import agreement_tasks
from src.aggregates.potential_agreement.signals import completed
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(completed)
def potential_agreement_completed_callback(**kwargs):
  potential_agreement_id = kwargs['aggregate_id']
  agreement_tasks.create_agreement_task_from_potential_agreement.delay(potential_agreement_id)
