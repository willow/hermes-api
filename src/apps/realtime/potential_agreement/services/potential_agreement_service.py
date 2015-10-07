from src.libs.firebase_utils.services import firebase_provider


def save_potential_agreement_in_firebase(potential_agreement_id, potential_agreement_name, _firebase_provider=None):
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  data = {'agreement_name': potential_agreement_name, }
  result = client.put('/agreement-overviews', potential_agreement_id, data)
  return result
