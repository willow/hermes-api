from django.dispatch import receiver
from src.aggregates.user.signals import created
from src.apps.auth.providers.auth0.services import auth0_tasks
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(created)
def user_created_callback(**kwargs):
  user_id = kwargs.pop('user_id')
  user_attrs = kwargs.pop('user_attrs')

  auth0_id = user_attrs['auth0']['user_id']
  auth0_tasks.save_user_id_in_auth0_task.delay(auth0_id, user_id)
