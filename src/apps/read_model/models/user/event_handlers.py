from django.dispatch import receiver
from src.aggregates.user.signals import created
from src.apps.read_model.models.user.services import user_tasks
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(created)
def user_created_callback(**kwargs):
  user_id = kwargs.pop('user_id')
  user_name = kwargs.pop('user_name')
  user_nickname = kwargs.pop('user_nickname')
  user_email = kwargs.pop('user_email')
  user_picture = kwargs.pop('user_picture')

  user_tasks.save_user_info_in_firebase_task.delay(
    user_id, user_name, user_nickname,
    user_email, user_picture
  )
