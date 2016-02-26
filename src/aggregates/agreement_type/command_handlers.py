from django.dispatch import receiver
from django.utils import timezone

from src.aggregates.user.commands import CreateUser
from src.aggregates.user.entities import User
from src.libs.common_domain import aggregate_repository
from src.libs.python_utils.id.id_utils import generate_id


@receiver(CreateUser.command_signal)
def create_user(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  system_created_date = timezone.now()
  id = generate_id()
  data = dict({'system_created_date': system_created_date, 'id': id}, **command.__dict__)

  user = User(**data)
  _aggregate_repository.save(user, -1)

  # commands typically shouldn't return an object but we're explicitly calling this function from the API
  # and need the return aggregate
  return user
