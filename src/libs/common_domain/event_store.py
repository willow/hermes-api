import logging

from src.libs.common_domain import dispatcher, event_service
from src.libs.common_domain import event_repository
from src.libs.django_utils.query.query_utils import batch_qs

logger = logging.getLogger(__name__)


def save_events(stream_id, starting_sequence, event_type, events, _event_repository=None, _event_dispatcher=None):
  if not _event_repository:    _event_repository = event_repository
  if not _event_dispatcher:    _event_dispatcher = dispatcher

  event_records = _event_repository.create_events(stream_id, starting_sequence, event_type, events)
  event_objs = zip(events, event_records)

  for e in event_objs:
    _event_dispatcher.publish_event(stream_id, e[0], e[1].event_sequence)


def load_events(event_type, stream_id, _event_repository=None):
  if not _event_repository:    _event_repository = event_repository

  events = _event_repository.get_events_for_stream(event_type, stream_id)
  return events


def load_domain_event_from_event_record(event_record, _event_service=None):
  if not _event_service:    _event_service = event_service

  domain_event = _event_service.load_domain_event_from_event_record(event_record)
  return domain_event


def replay_events(_event_repository=None, _event_service=None, _event_dispatcher=None):
  counter = 0
  if not _event_repository:    _event_repository = event_repository
  if not _event_service:    _event_service = event_service

  if not _event_dispatcher:    _event_dispatcher = dispatcher

  events = _event_repository.get_events()

  logger.debug("Replay %i events", events.count())

  for event_batch in batch_qs(events):
    logger.debug("starting batch : %s", event_batch[0])

    events = event_batch[3]

    for event in events:

      event_name = event.event_name
      event_data = event.event_data
      event_version = event.event_sequence

      domain_event = _event_service.load_domain_event_from_event_record(event)

      try:
        _event_dispatcher.publish_event(event.stream_id, domain_event, event_version)
      except Exception:
        logger.warn("Error sending signal for: %s Data: %s", event_name, event_data, exc_info=True)

      counter += 1
      logger.debug("Sending signal #%i: %s : %s", counter, event_name, event.stream_id)
