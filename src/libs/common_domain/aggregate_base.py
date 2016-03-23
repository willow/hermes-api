from abc import ABC, abstractmethod


class AggregateBase(ABC):
  def __init__(self):
    self._uncommitted_events = []
    self.version = -1

  def _raise_event(self, event):
    self.apply_event(event)
    # important to apply the event before appending the event as it's possible the event handler will throw an ex.
    # we wouldn't want that event to be added to the uncommitted list.
    self._uncommitted_events.append(event)

  def mark_events_as_committed(self):
    self._uncommitted_events.clear()

  @property
  def uncommitted_events(self):
    return self._uncommitted_events

  def apply_event(self, event):
    try:
      event_name = event.__class__.event_func_name
    except:
      raise Exception('The domain event is missing the `event_name` class attr')

    event_func_name = "_handle_{0}_event".format(event_name)

    handle_func = getattr(self, event_func_name, None)

    if not handle_func: raise NotImplementedError("{0} must implement {1}".format(
      self.__class__.__name__, event_func_name))

    handle_func(event)

    self.version += 1

  @classmethod
  @abstractmethod
  def from_attrs(cls, **kwargs):
    pass
