from src.aggregates.user.events import UserCreated1
from src.libs.common_domain.aggregate_base import AggregateBase


class User(AggregateBase):
  def __init__(self, id, name, nickname, email, picture, meta, system_created_date):
    super().__init__()

    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    if not nickname:
      raise TypeError("nickname is required")

    if not email:
      raise TypeError("email is required")

    if not picture:
      raise TypeError("picture is required")

    auth0_attrs = meta.get('auth0', {})
    auth0_user_id = auth0_attrs.get('user_id')
    if not auth0_user_id:
      raise TypeError("auth0_user_id is required")

    if not system_created_date:
      raise TypeError("system_created_date is required")

    self._raise_event(UserCreated1(id, name, nickname, email, picture, meta, system_created_date))

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name
    self.nickname = event.nickname
    self.email = event.email
    self.picture = event.picture
    self.meta = event.meta
    self.system_created_date = event.system_created_date

  def __str__(self):
    return 'User {id}: {name}'.format(id=self.id, name=self.name)
