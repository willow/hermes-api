from django.dispatch import receiver

from src.domain.agreement.events import AgreementCreated1, AgreementAttrsUpdated1, AgreementOutcomeNoticeAlertSent1, \
  AgreementExpirationAlertSent1
from src.domain.potential_agreement.events import PotentialAgreementCreated1
from src.apps.realtime.agreement import tasks
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(PotentialAgreementCreated1.event_signal)
def execute_save_agreement_edit_from_pa(**kwargs):
  event = kwargs['event']
  agreement_id = kwargs['aggregate_id']
  tasks.save_agreement_edit_in_firebase_task.delay(agreement_id, **event.data)


@event_idempotent
@receiver(AgreementCreated1.event_signal)
@receiver(AgreementAttrsUpdated1.event_signal)
def save_firebase_agreement(**kwargs):
  event = kwargs['event']
  agreement_id = kwargs['aggregate_id']

  # https://app.asana.com/0/10235149247655/100075573324021
  tasks.save_agreement_edit_in_firebase_task.delay(agreement_id, **event.data)
  tasks.save_agreement_detail_in_firebase_task.delay(agreement_id, **event.data)
  tasks.save_user_agreement_in_firebase_task.delay(agreement_id, **event.data)


@event_idempotent
@receiver(AgreementOutcomeNoticeAlertSent1.event_signal)
@receiver(AgreementExpirationAlertSent1.event_signal)
def agreement_alerts_callback(**kwargs):
  agreement_id = kwargs['aggregate_id']
  event = kwargs['event']
  tasks.save_agreement_alerts_in_firebase_task.delay(agreement_id, **event.data)
