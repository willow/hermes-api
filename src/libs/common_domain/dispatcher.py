import logging

logger = logging.getLogger(__name__)


def send_command(command):
  command_data = {'command': command}
  command.__class__.command_signal.send(None, **command_data)


def publish_event(aggregate_id, event, version):
  event_data = {'aggregate_id': aggregate_id, 'event': event, 'version': version}
  event.__class__.event_signal.send(None, **event_data)
