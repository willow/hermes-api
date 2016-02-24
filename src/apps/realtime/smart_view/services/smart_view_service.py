from src.aggregates.smart_view.services import smart_view_service
from src.libs.firebase_utils.services import firebase_provider


def save_smart_view_in_firebase(smart_view_id, _smart_view_service=None, _firebase_provider=None):
  if not _smart_view_service: _smart_view_service = smart_view_service
  if not _firebase_provider: _firebase_provider = firebase_provider

  smart_view = _smart_view_service.get_smart_view(smart_view_id)

  user_id = smart_view.user_id

  client = _firebase_provider.get_firebase_client()

  data = {
    'name': smart_view.name,
    'query': smart_view.query
  }

  result = client.put(
    'users-smart-views/{user_id}'.format(user_id=user_id),
    smart_view.id, data)

  return result
