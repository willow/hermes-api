from django.db import transaction

from src.libs.common_domain.models import Event
from src.libs.python_utils.types.type_utils import load_object


def get_events():
  return Event.objects.order_by("pk")


def get_events_for_stream(stream_id):
  return get_events().filter(stream_id=stream_id)


def _get_event_fqn(event):
  return event.__module__ + '.' + event.__class__.__name__


def create_events(stream_id, starting_sequence, events):
  version = starting_sequence

  with transaction.atomic():
    # the event store had a unique constraint on stream_id and version
    # which handles concurrency conflicts

    event_data = [
      Event(stream_id=stream_id, event_name=_get_event_fqn(e), event_sequence=version + i, event_data=e.data)
      for i, e in enumerate(events, 1)
      ]

  events = Event.objects.bulk_create(event_data)

  return events


def load_domain_event_from_event_record(event_record):
  event_name = event_record.event_name
  event_data = event_record.event_data

  domain_event_class = load_object(event_name)
  event_obj = domain_event_class(**event_data)

  return event_obj
