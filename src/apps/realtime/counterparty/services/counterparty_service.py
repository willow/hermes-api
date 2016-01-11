from src.aggregates.potential_agreement.services import potential_agreement_service
from src.libs.firebase_utils.services import firebase_provider


def save_counterparty_in_firebase(potential_agreement_id, _potential_agreement_service=None, _firebase_provider=None):
  if not _potential_agreement_service: _potential_agreement_service = potential_agreement_service
  if not _firebase_provider: _firebase_provider = firebase_provider

  potential_agreement = _potential_agreement_service.get_potential_agreement(potential_agreement_id)

  user_id = potential_agreement.potential_agreement_user_id
  counterparty = potential_agreement.potential_agreement_counterparty

  client = _firebase_provider.get_firebase_client()

  data = {counterparty: True}

  result = client.patch('users-counterparties/{0}'.format(user_id), data)

  return result
