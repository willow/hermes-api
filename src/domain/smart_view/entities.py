from src.domain.smart_view.events import SmartViewCreated1, SmartViewNameChanged1, SmartViewQueryChanged1
from src.libs.common_domain.aggregate_base import AggregateBase


class SmartView(AggregateBase):
  @classmethod
  def from_attrs(cls, id, name, query, user_id, system_created_date):
    ret_val = cls()

    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    if not query:
      raise TypeError("query is required")

    if not user_id:
      raise TypeError("user_id is required")

    ret_val._raise_event(SmartViewCreated1(id, name, query, user_id, system_created_date))

    return ret_val

  def update_attrs(self, name, query):
    if not name:
      raise TypeError("name is required")
    else:
      if name != self.name:
        self._raise_event(SmartViewNameChanged1(name, query, self.user_id))

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name
    self.query = event.query
    self.user_id = event.user_id
    self.system_created_date = event.system_created_date

  def _handle_name_changed_1_event(self, event):
    self.name = event.name

  def _handle_query_changed_1_event(self, event):
    self.query = event.query

  def __str__(self):
    class_name = self.__class__.__name__
    return '{class_name} {id}: {name}'.format(class_name=class_name, id=self.id, name=self.name)
