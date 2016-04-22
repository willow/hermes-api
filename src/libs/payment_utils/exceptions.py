class ChargeError(Exception):
  """Some kind of problem with charging a payment."""
  pass


class InvalidCardError(Exception):
  """Invalid card information prevent successful payment."""
  pass
