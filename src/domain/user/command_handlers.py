from django.dispatch import receiver

from src.domain.user.commands import CreateUser, SubscribeUser
from src.domain.user.entities import User
from src.libs.common_domain import aggregate_repository


@receiver(CreateUser.command_signal)
def create_user(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  user = User.from_attrs(**command.data)
  _aggregate_repository.save(user, -1)


@receiver(SubscribeUser.command_signal)
def subscribe_user(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  id = kwargs['aggregate_id']

  command = kwargs['command']

  user = _aggregate_repository.get(User, id)

  version = user.version

  user.subscribe(command.payment_token)

  _aggregate_repository.save(user, version)
