from src.aggregates.user.services import user_service
from src.libs.firebase_utils.services import firebase_provider


def save_agreement_types_in_firebase(user_id, _user_service=None, _firebase_provider=None):
  if not _user_service: _user_service = user_service

  if not _firebase_provider: _firebase_provider = firebase_provider

  user = _user_service.get_user(user_id)

  user_agreement_types = user.agreement_types

  client = _firebase_provider.get_firebase_client()

  agreement_types = {a.uid: {'name': a.name} for a in user_agreement_types}

  result = client.put('users-agreement-types', user_id, agreement_types)

  return result
