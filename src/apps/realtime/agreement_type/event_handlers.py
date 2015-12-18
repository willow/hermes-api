from django.dispatch import receiver

from src.aggregates.user.signals import created
from src.apps.realtime.agreement_type.services import agreement_type_tasks
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(created)
def user_completed_callback(**kwargs):
  user_id = kwargs.pop('user_id')

  agreement_type_tasks.save_agreement_types_in_firebase_task.delay(user_id)
