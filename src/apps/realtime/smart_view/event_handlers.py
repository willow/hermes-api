from django.dispatch import receiver

from src.domain.smart_view.events import SmartViewCreated1, SmartViewNameChanged1
from src.apps.realtime.smart_view import tasks
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(SmartViewCreated1.event_signal)
@receiver(SmartViewNameChanged1.event_signal)
def smart_view_created_callback(**kwargs):
  event = kwargs['event']
  aggregate_id = kwargs['aggregate_id']

  tasks.save_smart_view_in_firebase_task.delay(aggregate_id, event.name, event.query, event.user_id)
