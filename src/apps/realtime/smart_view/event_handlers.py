# from django.dispatch import receiver
#
# from src.aggregates.smart_view.signals import created, updated_attrs
# from src.apps.realtime.smart_view.services import smart_view_tasks
# from src.libs.common_domain.decorators import event_idempotent
#
#
# @event_idempotent
# @receiver(created)
# @receiver(updated_attrs)
# def smart_view_created_callback(**kwargs):
#   smart_view_id = kwargs['aggregate_id']
#
#   smart_view_tasks.save_smart_view_in_firebase_task.delay(smart_view_id)
