from django.dispatch import receiver

from src.aggregates.potential_agreement.signals import completed, updated_attrs, expiration_alert_sent, \
  outcome_notice_alert_sent
from src.apps.realtime.agreement.services import agreement_tasks
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(completed)
@receiver(updated_attrs)
def potential_agreement_completed_callback(**kwargs):
  potential_agreement_id = kwargs.pop('potential_agreement_id')

  agreement_tasks.save_agreement_edit_in_firebase_task.delay(potential_agreement_id)
  agreement_tasks.save_agreement_detail_in_firebase_task.delay(potential_agreement_id)
  agreement_tasks.save_user_agreement_in_firebase_task.delay(potential_agreement_id)


@event_idempotent
@receiver(outcome_notice_alert_sent)
@receiver(expiration_alert_sent)
def potential_agreement_alerts_callback(**kwargs):
  potential_agreement_id = kwargs.pop('potential_agreement_id')

  agreement_tasks.save_agreement_alerts_in_firebase_task.delay(potential_agreement_id)
