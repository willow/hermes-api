from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.tests.event_test_obj import DummyChangedName1, DummyCreated1


class DummyAggregate(AggregateBase):
  @classmethod
  def from_attrs(cls, id, name):
    ret_val = cls()
    ret_val._raise_event(DummyCreated1(id, name))

    return ret_val

  def change_name(self, name):
    self._raise_event(DummyChangedName1(name))

  def _handle_changed_name_1_event(self, event):
    self.name = event.name

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name
