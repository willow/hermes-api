from src.libs.common_domain.domain_event import DomainEvent
from src.libs.common_domain.event_signal import EventSignal


class DummyChangedName1(DomainEvent):
  event_func_name = 'changed_name_1'
  event_signal = EventSignal()

  def __init__(self, name):
    super().__init__()
    self.name = name


class DummyCreated1(DomainEvent):
  event_func_name = 'created_1'
  event_signal = EventSignal()

  def __init__(self, id, name):
    super().__init__()
    self.id = id
    self.name = name
