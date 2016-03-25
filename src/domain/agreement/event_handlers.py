from django.dispatch import receiver

# from src.apps.read_model.agreement import created, updated_attrs, outcome_alert_sent, \
#   outcome_notice_alert_sent
# from src.apps.realtime.agreement.services import agreement_tasks
from src.domain.agreement.events import AgreementCreated1, AgreementAttrsUpdated1, AgreementDeleted1
from src.domain.potential_agreement.events import PotentialAgreementCompleted1
from src.domain.agreement import tasks
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(PotentialAgreementCompleted1.event_signal)
def execute_pa_completed_1(**kwargs):
  kwargs.pop('signal')
  kwargs.pop('sender')
  tasks.create_agreement_task.delay(**kwargs)


@event_idempotent
@receiver(AgreementCreated1.event_signal)
@receiver(AgreementAttrsUpdated1.event_signal)
def execute_save_agreement_search(**kwargs):
  agreement_id = kwargs['aggregate_id']
  event = kwargs['event']

  tasks.save_agreement_search_task.delay(
    agreement_id, event.user_id, event.name, event.counterparty, event.agreement_type_id
  )


@event_idempotent
@receiver(AgreementCreated1.event_signal)
@receiver(AgreementAttrsUpdated1.event_signal)
def execute_create_agreement_alerts(**kwargs):
  agreement_id = kwargs['aggregate_id']
  event = kwargs['event']

  # why is False hardcoded? see https://app.asana.com/0/10235149247655/100226819013310.
  tasks.save_agreement_alert_task.delay(
    agreement_id,
    event.outcome_alert_date, event.outcome_alert_enabled, False,
    event.outcome_notice_alert_date, event.outcome_notice_alert_enabled, False,
  )


@event_idempotent
@receiver(AgreementDeleted1.event_signal)
def agreement_delete_callback(**kwargs):
  agreement_id = kwargs['aggregate_id']
  tasks.delete_agreement_task.delay(agreement_id)
