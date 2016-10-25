from django.dispatch import receiver

from src.apps.read_model.relational.user import tasks
from src.domain.user.events import UserCreated1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(UserCreated1.event_signal)
def execute_user_created_1(**kwargs):
  event = kwargs['event']

  # event has the id
  tasks.create_auth_user_task.delay(event.id, event.email)
