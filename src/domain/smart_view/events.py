from src.libs.common_domain.domain_event import DomainEvent
from src.libs.common_domain.event_signal import EventSignal
from src.libs.python_utils.objects.object_utils import initializer


class SmartViewCreated1(DomainEvent):
  event_func_name = 'created_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, name, query, user_id, system_created_date):
    super().__init__()


class SmartViewNameChanged1(DomainEvent):
  event_func_name = 'name_changed_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, name, query, user_id):
    super().__init__()


class SmartViewQueryChanged1(DomainEvent):
  event_func_name = 'query_changed_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, query):
    super().__init__()
