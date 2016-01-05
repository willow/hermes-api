from django.utils import timezone

from src.aggregates.asset.services import asset_service
from src.aggregates.potential_agreement.services import potential_agreement_service
from src.apps.agreement.enums import DurationTypeEnum
from src.libs.datetime_utils.datetime_utils import get_timestamp_from_datetime
from src.libs.firebase_utils.services import firebase_provider


def save_agreement_edit_in_firebase(potential_agreement_id, _potential_agreement_service=None, _firebase_provider=None):
  if not _potential_agreement_service: _potential_agreement_service = potential_agreement_service
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  potential_agreement = _potential_agreement_service.get_potential_agreement(potential_agreement_id)

  if potential_agreement.potential_agreement_execution_date:
    execution_date = get_timestamp_from_datetime(potential_agreement.potential_agreement_execution_date)
  else:
    execution_date = None

  if potential_agreement.potential_agreement_renewal_notice_type:
    renewal_notice_type = DurationTypeEnum(potential_agreement.potential_agreement_renewal_notice_type).name
  else:
    renewal_notice_type = None

  if potential_agreement.potential_agreement_term_length_amount:
    term_length_type = DurationTypeEnum(potential_agreement.potential_agreement_term_length_type).name
  else:
    term_length_type = None

  agreement_type_id = None
  potential_agreement_type = potential_agreement.potential_agreement_type
  if potential_agreement_type:
    agreement_type_id = potential_agreement_type.agreement_type_id

  data = {
    'auto-renew': potential_agreement.potential_agreement_auto_renew,
    'counterparty': potential_agreement.potential_agreement_counterparty,
    'description': potential_agreement.potential_agreement_description,
    'duration-details': potential_agreement.potential_agreement_duration_details,
    'execution-date': execution_date,
    'name': potential_agreement.potential_agreement_name,
    'renewal-notice-amount': potential_agreement.potential_agreement_renewal_notice_amount,
    'renewal-notice-type': renewal_notice_type,
    'term-length-amount': potential_agreement.potential_agreement_term_length_amount,
    'term-length-type': term_length_type,
    'type-id': agreement_type_id,
    'viewers': {potential_agreement.potential_agreement_user_id: True}
  }

  result = client.put('/agreement-edits', potential_agreement_id, data)

  return result


def save_agreement_detail_in_firebase(potential_agreement_id, _potential_agreement_service=None, _asset_service=None,
                                      _firebase_provider=None):
  if not _potential_agreement_service: _potential_agreement_service = potential_agreement_service
  if not _asset_service: _asset_service = asset_service
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  potential_agreement = _potential_agreement_service.get_potential_agreement(potential_agreement_id)

  # this task is only fired after a potential agreement is complete, so it's safe to assume an execution date is present
  execution_date = get_timestamp_from_datetime(potential_agreement.potential_agreement_execution_date)

  if potential_agreement.potential_agreement_term_length_amount:
    term_length_type = DurationTypeEnum(potential_agreement.potential_agreement_term_length_type).name
  else:
    term_length_type = None

  agreement_type_name = None
  potential_agreement_type = potential_agreement.potential_agreement_type
  if potential_agreement_type:
    agreement_type_name = potential_agreement_type.agreement_type_name

  assets = _asset_service.get_assets(potential_agreement.potential_agreement_artifacts)

  artifacts = {a.asset_id: {'name': a.asset_original_name} for a in
               assets}

  data = {
    'counterparty': potential_agreement.potential_agreement_counterparty,
    'description': potential_agreement.potential_agreement_description,
    'execution-date': execution_date,
    'name': potential_agreement.potential_agreement_name,
    'term-length-amount': potential_agreement.potential_agreement_term_length_amount,
    'term-length-type': term_length_type,
    'type-name': agreement_type_name,
    'artifacts': artifacts,
    'viewers': {potential_agreement.potential_agreement_user_id: True}
  }

  result = client.put('/agreement-details', potential_agreement_id, data)

  return result


def save_dashboard_agreement_in_firebase(potential_agreement_id, _potential_agreement_service=None,
                                         _firebase_provider=None):
  if not _potential_agreement_service: _potential_agreement_service = potential_agreement_service
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  potential_agreement = _potential_agreement_service.get_potential_agreement(potential_agreement_id)

  # this task is only fired after a potential agreement is complete, so it's safe to assume an execution date is present
  execution_date = get_timestamp_from_datetime(potential_agreement.potential_agreement_execution_date)

  modification_date = get_timestamp_from_datetime(timezone.now())

  agreement_type_name = None
  potential_agreement_type = potential_agreement.potential_agreement_type
  if potential_agreement_type:
    agreement_type_name = potential_agreement_type.agreement_type_name

  data = {
    'counterparty': potential_agreement.potential_agreement_counterparty,
    'artifact-count': len(potential_agreement.potential_agreement_artifacts),
    'execution-date': execution_date,
    'modification-date': modification_date,
    'name': potential_agreement.potential_agreement_name,
    'type-name': agreement_type_name,
  }

  result = client.put(
    'users-dashboard-agreements/{user_id}'.format(user_id=potential_agreement.potential_agreement_user_id),
    potential_agreement_id, data)

  return result
