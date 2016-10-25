from django.dispatch import Signal
from django.dispatch.dispatcher import NO_RECEIVERS


class CommandSignal(Signal):
  def send(self, sender, **named):
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
    if 'command' not in named: raise ValueError('command is required')

    responses = []

    receivers = self._live_receivers(sender)

    if len(receivers) != 1: raise Exception('command signal requires exactly 1 command handler')

    if not self.receivers or self.sender_receivers_cache.get(sender) is NO_RECEIVERS:
      return responses

    for receiver in receivers:
      response = receiver(signal=self, sender=sender, **named)
      responses.append((receiver, response))

    return responses
