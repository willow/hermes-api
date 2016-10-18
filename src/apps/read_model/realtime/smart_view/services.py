from src.libs.firebase_utils.services import firebase_provider


def save_smart_view_in_firebase(smart_view_id, name, query, user_id, _firebase_provider=None):
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  data = {
    'name': name,
    'query': query,
  }

  result = client.put('users-smart-views/{user_id}'.format(user_id=user_id), smart_view_id, data)

  return result
