from django.dispatch import receiver

from src.apps.read_model.relational.agreement_type import tasks
from src.domain.topic.events import TopicCreated1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(TopicCreated1.event_signal)
def execute_topic_created_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  event = kwargs['event']
  name = event.name
  stem = event.stem
  collapsed_stem = event.collapsed_stem
  tasks.save_topic_lookup_task.delay(aggregate_id, name, stem, collapsed_stem)
