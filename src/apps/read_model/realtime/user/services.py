from src.libs.firebase_utils.services import firebase_provider


def save_user_identity_in_firebase(user_id, name, nickname, email, picture, _firebase_provider=None):
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  identity = {'email': email, 'name': name, 'nickname': nickname, 'picture': picture}

  result = client.put('users/{id}'.format(id=user_id), 'identity', identity)
  return result


def save_user_subscription_in_firebase(user_id, is_subscribed, _firebase_provider=None):
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  subscriptions = {'is_subscribed': is_subscribed}

  result = client.put('users/{id}'.format(id=user_id), 'subscriptions', subscriptions)
  return result
