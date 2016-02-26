from django.dispatch import Signal
from django.dispatch.dispatcher import NO_RECEIVERS


class EventSignal(Signal):
  def send(self, sender, allow_non_idempotent=True, **named):
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

      response = receiver(signal=self, sender=sender, **named)
      responses.append((receiver, response))

    return responses
