from django.dispatch import receiver

from src.apps.read_model.realtime.counterparty import tasks
from src.domain.agreement.events import AgreementAttrsUpdated1
from src.domain.agreement.events import AgreementCreated1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(AgreementCreated1.event_signal)
@receiver(AgreementAttrsUpdated1.event_signal)
def execute_pa_created_1(**kwargs):
  event = kwargs['event']
  agreement_id = kwargs['aggregate_id']

  user_id = event.user_id
  counterparty = event.counterparty

  tasks.save_counterparty_in_firebase_task.delay(agreement_id, user_id, counterparty)
