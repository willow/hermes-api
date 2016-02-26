from src.libs.common_domain import event_store
from src.libs.common_domain.services import event_service


def save(aggregate, expected_version, _event_store=None):
  if not _event_store: _event_store = event_store
  _event_store.save_events(aggregate.id, expected_version, aggregate.uncommitted_events)
  aggregate.mark_events_as_committed()


def get(aggregate_class, aggregate_id, _event_store=None, _event_service=None):
  if not _event_store: _event_store = event_store
  if not _event_service: _event_service = event_service

  events = _event_store.load_events(aggregate_id)

  aggregate_instance = aggregate_class()

  for event in events:
    domain_event = _event_service.load_domain_event_from_event_record(event)
    aggregate_instance.apply_event(domain_event)

  return aggregate_instance
