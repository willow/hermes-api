from src.libs.common_domain.domain_event import DomainEvent
from src.libs.common_domain.event_signal import EventSignal
from src.libs.python_utils.objects.object_utils import initializer


class UserCreated1(DomainEvent):
  event_func_name = 'created_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, name, nickname, email, picture, meta):
    super().__init__()


class UserSubscribed1(DomainEvent):
  event_func_name = 'subscribed_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, plan_name, charged_amount):
    super().__init__()
