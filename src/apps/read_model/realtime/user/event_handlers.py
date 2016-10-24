from django.dispatch import receiver

from src.apps.read_model.realtime.user import tasks
from src.domain.user.events import UserCreated1, UserSubscribed1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(UserCreated1.event_signal)
def execute_user_created_1(**kwargs):
  event = kwargs['event']
  aggregate_id = kwargs['aggregate_id']

  tasks.save_user_identity_in_firebase_task.delay(aggregate_id, event.name, event.nickname, event.email, event.picture)


@event_idempotent
@receiver(UserSubscribed1.event_signal)
def execute_user_subscribed_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']

  tasks.save_user_subscription_in_firebase_task.delay(aggregate_id, True)
