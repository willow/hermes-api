from collections import deque
from src.libs.common_domain.event_record import EventRecord


class AggregateBase:
  def __init__(self):
    self._uncommitted_events = deque()

  def _raise_event(self, event, **kwargs):
    self._apply_event(event, **kwargs)

    event_name = event.name
    version = event.version
    # get the fq name - this is used for replaying events
    event_fq_name = event.module_name + "." + event.name

    self._uncommitted_events.append(EventRecord(event, event_name, event_fq_name, version, kwargs))

  def send_events(self):
    while self._uncommitted_events:
      event_record = self._uncommitted_events.popleft()
      event_data = dict({'aggregate_id': self.id}, **event_record.kwargs)
      event_record.event_obj.send(None, **event_data)

  def _apply_event(self, event, **kwargs):
    event_func_name = "_handle_{0}_event".format(event.name)

    handle_func = getattr(self, event_func_name, None)

    if not handle_func: raise NotImplementedError("{0} must implement {1}".format(
      self.__class__.__name__, event_func_name))

    handle_func(**kwargs)
