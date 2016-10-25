import logging

logger = logging.getLogger(__name__)


# these two methods should probably be split. their signatures may change throughout the future.
def send_command(aggregate_id, command):
  command_data = {'aggregate_id': aggregate_id, 'command': command}
  command.__class__.command_signal.send(None, **command_data)


def publish_event(aggregate_id, event, version, allow_non_idempotent, send_to_app_names):
  event_data = {'aggregate_id': aggregate_id, 'event': event, 'version': version}
  event.__class__.event_signal.send(None, allow_non_idempotent, send_to_app_names, **event_data)
