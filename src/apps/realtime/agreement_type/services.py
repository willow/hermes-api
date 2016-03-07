from src.domain.agreement_type import services as at_service
from src.libs.firebase_utils.services import firebase_provider


def save_global_agreement_types_in_firebase(user_id, _at_service=None, _firebase_provider=None):
  if not _at_service: _at_service = at_service
  if not _firebase_provider: _firebase_provider = firebase_provider
  client = _firebase_provider.get_firebase_client()

  global_agreement_type = _at_service.get_global_agreement_types()
  agreement_types = {a.id: {'name': a.name} for a in global_agreement_type}

  result = client.put('users-agreement-types', user_id, agreement_types)

  return result


def save_user_agreement_types_in_firebase(agreement_type_id, name, user_id, _firebase_provider=None):
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  data = {'name': name}

  result = client.put('users-agreement-types/{0}/'.format(user_id), agreement_type_id, data)

  return result
