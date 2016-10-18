from django.dispatch import receiver

from src.apps.read_model.relational.asset import tasks
from src.domain.prospect.events import EngagementOpportunityAddedToProfile1, ProspectAddedProfile1, ProspectDeleted1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(ProspectAddedProfile1.event_signal)
def execute_added_profile_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  event = kwargs['event']

  tasks.save_profile_lookup_by_provider_task.delay(
      event.id, event.external_id,
      event.provider_type, aggregate_id
  )


@event_idempotent
@receiver(ProspectDeleted1.event_signal)
def execute_deleted_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']

  tasks.delete_prospect_task.delay(aggregate_id)


@event_idempotent
@receiver(EngagementOpportunityAddedToProfile1.event_signal)
def execute_added_eo_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  event = kwargs['event']

  tasks.save_eo_lookup_by_provider_task.delay(
      event.id, event.external_id,
      event.provider_type, aggregate_id
  )
