from unittest.mock import MagicMock

from src.libs.common_domain import event_store
from src.libs.common_domain import aggregate_repository
from src.libs.common_domain.tests.aggregate_test_obj import DummyAggregate


def test_aggregate_repository_marks_events_as_committed():
  aggregate_test = DummyAggregate.from_attrs('12345', 'hello')
  aggregate_test.change_name('hello')
  event_store_mock = MagicMock(spec=event_store)

  aggregate_repository.save(aggregate_test, -1, event_store_mock)

  assert len(aggregate_test._uncommitted_events) == 0
