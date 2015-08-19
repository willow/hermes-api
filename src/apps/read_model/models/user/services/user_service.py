from src.libs.firebase_utils.services import firebase_provider


def save_user_info_in_firebase(user_uid, user_name, user_nickname, user_email, user_picture, _firebase_provider=None):
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  identity = {'email': user_email, 'name': user_name, 'nickname': user_nickname, 'picture': user_picture}
  result = client.put('/users', user_uid, {'identity': identity})
  return result
