from django.dispatch import receiver

from src.apps.read_model.realtime.agreement import tasks
from src.domain.agreement.events import AgreementCreated1, AgreementAttrsUpdated1, AgreementOutcomeNoticeAlertSent1, \
  AgreementOutcomeAlertSent1, AgreementDeleted1, ArtifactDeleted1, ArtifactCreated1
from src.domain.potential_agreement.events import PotentialAgreementCreated1
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

  tasks.save_agreement_edit_in_firebase_task.delay(agreement_id, **event.data)
  tasks.save_agreement_detail_in_firebase_task.delay(agreement_id, **event.data)
  tasks.save_user_agreement_in_firebase_task.delay(agreement_id, **event.data)


@event_idempotent
@receiver(AgreementOutcomeNoticeAlertSent1.event_signal)
@receiver(AgreementOutcomeAlertSent1.event_signal)
def agreement_alerts_callback(**kwargs):
  agreement_id = kwargs['aggregate_id']
  event = kwargs['event']
  tasks.save_agreement_alerts_in_firebase_task.delay(agreement_id, **event.data)


@event_idempotent
@receiver(AgreementDeleted1.event_signal)
def agreement_delete_callback(**kwargs):
  agreement_id = kwargs['aggregate_id']
  event = kwargs['event']
  user_id = event.user_id
  tasks.delete_agreement_in_firebase_task.delay(agreement_id, user_id)


@event_idempotent
@receiver(ArtifactDeleted1.event_signal)
def artifact_delete_callback(**kwargs):
  agreement_id = kwargs['aggregate_id']
  event = kwargs['event']

  remaining_artifact_ids = event.remaining_artifact_ids
  data = dict({'artifact_ids': remaining_artifact_ids}, **event.data)

  tasks.save_agreement_detail_in_firebase_task.delay(agreement_id, **data)
  tasks.save_user_agreement_in_firebase_task.delay(agreement_id, **data)


@event_idempotent
@receiver(ArtifactCreated1.event_signal)
def artifact_create_callback(**kwargs):
  agreement_id = kwargs['aggregate_id']
  event = kwargs['event']

  tasks.save_agreement_detail_in_firebase_task.delay(agreement_id, **event.data)
  tasks.save_user_agreement_in_firebase_task.delay(agreement_id, **event.data)
