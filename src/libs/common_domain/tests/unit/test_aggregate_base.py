from src.libs.common_domain.tests.aggregate_test_obj import DummyAggregate
from src.libs.common_domain.tests.event_test_obj import DummyChangedName1


def test_aggregate_base_handles_event():
  event = DummyChangedName1('hello')

  aggregate_test = DummyAggregate.from_attrs('12345', 'test')

  aggregate_test.apply_event(event)

  assert aggregate_test.name == 'hello'


def test_aggregate_base_sends_events():
  aggregate_test = DummyAggregate.from_attrs('12345', 'test')

  aggregate_test.change_name('hello')

  assert aggregate_test.name == 'hello'
