# from django.dispatch import receiver
#
# from src.apps.read_model.agreement import created, updated_attrs
# from src.apps.realtime.counterparty.services import counterparty_tasks
# from src.libs.common_domain.decorators import event_idempotent
#
#
# @event_idempotent
# @receiver(created)
# @receiver(updated_attrs)
# def agreement_completed_callback(**kwargs):
#   agreement_id = kwargs['aggregate_id']
#
#   counterparty_tasks.save_counterparty_in_firebase_task.delay(agreement_id)
