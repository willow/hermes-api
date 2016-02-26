# from django.dispatch import receiver
# from src.libs.common_domain.decorators import event_idempotent

#
# from src.apps.read_model.agreement import created, updated_attrs, expiration_alert_sent, outcome_notice_alert_sent
# from src.apps.realtime.agreement.services import agreement_tasks
#
#
# @event_idempotent
# @receiver(created)
# @receiver(updated_attrs)
# def agreement_updated_callback(**kwargs):
#   agreement_id = kwargs['aggregate_id']
#
#   agreement_tasks.save_agreement_edit_in_firebase_task.delay(agreement_id)
#   agreement_tasks.save_agreement_detail_in_firebase_task.delay(agreement_id)
#   agreement_tasks.save_user_agreement_in_firebase_task.delay(agreement_id)
#
#
# @event_idempotent
# @receiver(outcome_notice_alert_sent)
# @receiver(expiration_alert_sent)
# def potential_agreement_alerts_callback(**kwargs):
#   agreement_id = kwargs['aggregate_id']
#
#   agreement_tasks.save_agreement_alerts_in_firebase_task.delay(agreement_id)
#
#
from django.dispatch import receiver

from src.aggregates.agreement_type.events import AgreementTypeCreated1
from src.apps.read_model.agreement_type import tasks

from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(AgreementTypeCreated1.event_signal)
def execute_user_created_1(**kwargs):
  event = kwargs['event']
  version = kwargs['version']
  at_id = kwargs['aggregate_id']

  tasks.create_agreement_type_task.delay(
    at_id, event.name, event.is_global, event.user_id, event.system_created_date, version
  )