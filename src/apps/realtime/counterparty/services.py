from src.libs.firebase_utils.services import firebase_provider


def save_counterparty_in_firebase(user_id, counterparty, _firebase_provider=None):
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  data = {counterparty: True}

  result = client.patch('users-counterparties/{0}'.format(user_id), data)

  return result
