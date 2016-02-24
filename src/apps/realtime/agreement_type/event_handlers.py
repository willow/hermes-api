from django.dispatch import receiver
from src.aggregates.agreement_type.services import agreement_type_service

from src.aggregates.user.signals import created as user_created
from src.aggregates.agreement_type.signals import created as agreement_type_created
from src.apps.realtime.agreement_type.services import agreement_type_tasks
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(user_created)
def user_created_callback(**kwargs):
  user_id = kwargs.pop('id')

  agreement_type_tasks.save_agreement_types_in_firebase_task.delay(user_id)


@event_idempotent
@receiver(agreement_type_created)
def agreement_type_created_callback(**kwargs):
  agreement_type_id = kwargs.pop('id')

  agreement_type = agreement_type_service.get_agreement_type(agreement_type_id)
  if not agreement_type.is_global:
    agreement_type_user_id = agreement_type.agreement_type_user_id
    agreement_type_tasks.save_agreement_types_in_firebase_task.delay(agreement_type_user_id)
