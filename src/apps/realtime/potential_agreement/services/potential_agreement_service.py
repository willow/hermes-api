from src.libs.firebase_utils.services import firebase_provider


def save_potential_agreement_in_firebase(potential_agreement_id, potential_agreement_name, user_id,
                                         _firebase_provider=None):
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  data = {'agreement_name': potential_agreement_name, 'viewers': {user_id: True}}
  result = client.put('/agreement-edits', potential_agreement_id, data)
  return result
