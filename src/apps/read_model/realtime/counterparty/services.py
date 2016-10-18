from src.libs.firebase_utils.services import firebase_provider
from src.libs.text_utils.text_formatter import make_alnum


def save_counterparty_in_firebase(user_id, counterparty, _firebase_provider=None):
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  counterparty_key = make_alnum(counterparty)
  data = {counterparty_key: {'name': counterparty}}

  result = client.patch('users-counterparties/{0}'.format(user_id), data)

  return result
