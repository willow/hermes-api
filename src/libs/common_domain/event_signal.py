import inspect
import os

from django.apps import apps
from django.dispatch import Signal
from django.dispatch.dispatcher import NO_RECEIVERS


class EventSignal(Signal):
  def send(self, sender, allow_non_idempotent=True, send_to_app_names=None, **named):
    """
    Send signal from sender to all connected receivers.

    If any receiver raises an error, the error propagates back through send,
    terminating the dispatch loop, so it is quite possible to not have all
    receivers called if a raises an error.

    Arguments:

        sender
            The sender of the signal Either a specific object or None.

        named
            Named arguments which will be passed to receivers.

    Returns a list of tuple pairs [(receiver, response), ... ].
    """
    if 'aggregate_id' not in named: raise ValueError('aggregate_id is required')
    if 'version' not in named: raise ValueError('version is required')
    if 'event' not in named: raise ValueError('event is required')

    responses = []

    if not self.receivers or self.sender_receivers_cache.get(sender) is NO_RECEIVERS:
      return responses

    for receiver in self._live_receivers(sender):

      if not allow_non_idempotent:
        if not getattr(receiver, 'is_idempotent', False):
          continue

      if send_to_app_names:
        for a in send_to_app_names:
          app_split = a.split('.', 1)
          app_name = app_split[0]
          try:
            handler_path = app_split[1]
          except:
            # this will happen if they just type in the name of an app 'myapp' without a subpath like 'myapp.path'
            handler_path = ''
          app = apps.get_app_config(app_name)
          path = os.path.join(app.path, handler_path)
          if path in inspect.getfile(receiver):
            break
        else:
          # nested loop control flow http://stackoverflow.com/questions/653509/breaking-out-of-nested-loops
          continue

      response = receiver(signal=self, sender=sender, **named)
      responses.append((receiver, response))

    return responses
