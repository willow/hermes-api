from src.domain.asset.events import AssetCreated1
from src.libs.common_domain.aggregate_base import AggregateBase


class Asset(AggregateBase):
  @classmethod
  def from_attrs(cls, id, path, content_type, original_name, system_created_date):
    ret_val = cls()
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

    ret_val._raise_event(AssetCreated1(id, path, content_type, original_name, system_created_date))

    return ret_val

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.path = event.path
    self.content_type = event.content_type
    self.original_name = event.original_name

    self.system_created_date = event.system_created_date

  def __str__(self):
    return 'Asset {id}: {name}'.format(id=self.id, name=self.original_name)
