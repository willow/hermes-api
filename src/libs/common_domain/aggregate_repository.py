from django.core.exceptions import ObjectDoesNotExist

from src.libs.common_domain import event_store


def save(aggregate, expected_version, _event_store=None):
  if not _event_store: _event_store = event_store

  uncommitted_events = aggregate.uncommitted_events

  if uncommitted_events:
    # could happen if someone calls `.save` on an aggregate that performed no commands

    if expected_version >= aggregate.version:
      raise Exception(
        'Invalid version number. Make sure to capture the version of the aggregate before acting upon it.')

    event_type = _get_event_type_from_instance(aggregate)

    _event_store.save_events(aggregate.id, expected_version, event_type, uncommitted_events)

    aggregate.mark_events_as_committed()


def get(aggregate_class, aggregate_id, _event_store=None):
  if not _event_store: _event_store = event_store

  events = _event_store.load_events(_get_event_type_from_class(aggregate_class), aggregate_id)

  # the @classmethod from_attrs allows us to call this empty constructor
  aggregate_instance = aggregate_class()

  if not events:
    raise ObjectDoesNotExist("aggregate doesn't exist: {0}".format(aggregate_id))

  for event in events:
    domain_event = _event_store.load_domain_event_from_event_record(event)
    aggregate_instance.apply_event(domain_event)

  return aggregate_instance


def _get_event_type_from_instance(aggregate):
  return aggregate.__class__.__name__


def _get_event_type_from_class(aggregate_type):
  return aggregate_type.__name__
