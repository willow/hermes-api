from django.dispatch import receiver

from src.domain.asset.events import AssetCreated1
from src.domain.asset import tasks
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(AssetCreated1.event_signal)
def execute_asset_created_1(**kwargs):
  event = kwargs['event']
  asset_id = kwargs['aggregate_id']

  tasks.create_asset_lookup_task.delay(asset_id, event.original_name, event.path)
