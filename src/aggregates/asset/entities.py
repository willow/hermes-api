from src.aggregates.user.events import UserCreated1
from src.libs.common_domain.aggregate_base import AggregateBase


class Asset(AggregateBase):
  def __init__(self, id, path, content_type, original_name, system_created_date):
    super().__init__()

    if not id:
      raise TypeError("id is required")

    if not path:
      raise TypeError("path is required")

    if not content_type:
      raise TypeError("content_type is required")

    if not original_name:
      raise TypeError("original_name is required")

    if not path:
      raise TypeError("path is required")

    self._raise_event(id, path, content_type, original_name, system_created_date)

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.path = event.path
    self.content_type = event.content_type
    self.original_name = event.original_name
    self.system_created_date = event.system_created_date

  def __str__(self):
    return 'Asset {id}: {name}'.format(id=self.id, name=self.name)
