from unittest.mock import MagicMock

from django.dispatch import receiver

from src.libs.common_domain import event_store
from src.libs.common_domain.models import Event
from src.libs.common_domain.services import event_service
from src.libs.common_domain.tests.event_test_obj import DummyChangedName1


def test_event_store_sends_event_in_order():
  results = []

  @receiver(DummyChangedName1.event_signal)
  def side_effect(**kwargs):
    event = kwargs['event']
    results.append(event.name)

  event_id = '12345'
  expected_version = -1
  events = [DummyChangedName1('hello'), DummyChangedName1('world')]

  event_service_mock = MagicMock(spec=event_service)
  event_service_mock.create_events = MagicMock(return_value=[Event(event_sequence=0), Event(event_sequence=1)])
  event_store.save_events(event_id, expected_version, events, event_service_mock)

  assert results == ['hello', 'world']
