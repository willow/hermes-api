# from django.dispatch import receiver
#
# from src.aggregates.user.events import UserCreated1
# from src.apps.read_model.user import tasks
# from src.libs.common_domain.decorators import event_idempotent
#
#
# @event_idempotent
# @receiver(UserCreated1.event_signal)
# def execute_user_created_1(**kwargs):
#   event = kwargs['event']
#   version = kwargs['version']
#
#   # event has the id
#   tasks.create_auth_user_task.delay(version, event.id, event.email, event.system_created_date)
