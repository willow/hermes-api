from django.utils import timezone

from src.aggregates.asset.services import asset_service
from src.apps.agreement.enums import DurationTypeEnum
from src.libs.datetime_utils.datetime_utils import get_timestamp_from_datetime
from src.libs.firebase_utils.services import firebase_provider


def save_agreement_edit_in_firebase(agreement, _firebase_provider=None):
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  if agreement.execution_date:
    execution_date = get_timestamp_from_datetime(agreement.execution_date)
  else:
    execution_date = None

  if agreement.outcome_notice_time_type:
    outcome_notice_type = DurationTypeEnum(agreement.outcome_notice_time_type).name
  else:
    outcome_notice_type = None

  if agreement.term_length_time_amount:
    term_length_type = DurationTypeEnum(agreement.term_length_time_type).name
  else:
    term_length_type = None

  if agreement.outcome_notice_alert_time_type:
    outcome_notice_alert_time_type = DurationTypeEnum(
      agreement.outcome_notice_alert_time_type).name
  else:
    outcome_notice_alert_time_type = None

  if agreement.expiration_alert_time_type:
    expiration_alert_time_type = DurationTypeEnum(
      agreement.expiration_alert_time_type).name
  else:
    expiration_alert_time_type = None

  agreement_type_id = None
  agreement_type = agreement.agreement_type
  if agreement_type:
    agreement_type_id = agreement_type.uid

  data = {
    'auto-renew': agreement.auto_renew,
    'counterparty': agreement.counterparty,
    'description': agreement.description,
    'duration-details': agreement.duration_details,
    'execution-date': execution_date,
    'name': agreement.name,
    'outcome-notice-time-amount': agreement.outcome_notice_time_amount,
    'outcome-notice-time-type': outcome_notice_type,
    'outcome-notice-alert-enabled': agreement.outcome_notice_alert_enabled,
    'outcome-notice-alert-time-amount': agreement.outcome_notice_alert_time_amount,
    'outcome-notice-alert-time-type': outcome_notice_alert_time_type,
    'expiration-alert-enabled': agreement.expiration_alert_enabled,
    'expiration-alert-time-amount': agreement.expiration_alert_time_amount,
    'expiration-alert-time-type': expiration_alert_time_type,
    'term-length-time-amount': agreement.term_length_time_amount,
    'term-length-time-type': term_length_type,
    'type-id': agreement_type_id,
    'viewers': {agreement.user_id: True}
  }

  result = client.put('/agreement-edits', agreement.uid, data)

  return result


def save_agreement_detail_in_firebase(agreement, _asset_service=None, _firebase_provider=None):
  if not _asset_service: _asset_service = asset_service
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  # this task is only fired after a potential agreement is complete, so it's safe to assume an execution date is present
  execution_date = get_timestamp_from_datetime(agreement.execution_date)

  if agreement.term_length_time_amount:
    term_length_type = DurationTypeEnum(agreement.term_length_time_type).name
  else:
    term_length_type = None

  agreement_type_name = None
  agreement_type = agreement.agreement_type
  if agreement_type:
    agreement_type_name = agreement_type.name

  assets = _asset_service.get_assets(agreement.artifacts)

  artifacts = {a.uid: {'name': a.original_name} for a in assets}

  data = {
    'counterparty': agreement.counterparty,
    'description': agreement.description,
    'execution-date': execution_date,
    'name': agreement.name,
    'term-length-time-amount': agreement.term_length_time_amount,
    'term-length-time-type': term_length_type,
    'type-name': agreement_type_name,
    'artifacts': artifacts,
    'viewers': {agreement.user_id: True}
  }

  result = client.put('/agreement-details', agreement.uid, data)

  return result


def save_user_agreement_in_firebase(agreement, _firebase_provider=None):
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  # this task is only fired after a potential agreement is complete, so it's safe to assume an execution date is present
  execution_date = get_timestamp_from_datetime(agreement.execution_date)

  modification_date = get_timestamp_from_datetime(timezone.now())

  agreement_type_name = None
  agreement_type = agreement.agreement_type
  if agreement_type:
    agreement_type_name = agreement_type.name

  data = {
    'counterparty': agreement.counterparty,
    'artifact-count': len(agreement.artifacts),
    'execution-date': execution_date,
    'modification-date': modification_date,
    'name': agreement.name,
    'type-name': agreement_type_name,
  }

  result = client.put(
    'users-agreements/{user_id}'.format(user_id=agreement.user_id),
    agreement.uid, data)

  return result


def save_agreement_alerts_in_firebase(agreement, _firebase_provider=None):
  if not _firebase_provider: _firebase_provider = firebase_provider
  client = _firebase_provider.get_firebase_client()

  data = {}

  if agreement.expiration_alert_created:
    exp_alert_key = '{0}-{1}'.format(agreement.id, 'expiration-alert')
    exp_date = get_timestamp_from_datetime(agreement.outcome_date)
    data[exp_alert_key] = {
      'due-date': exp_date,
      'agreement-id': agreement.id,
      'agreement-name': agreement.name,
      'alert-type': 'expiration'
    }

  if agreement.outcome_notice_alert_created:
    outcome_notice_alert_key = '{0}-{1}'.format(agreement.id, 'outcome-notice-alert')
    outcome_notice_date = get_timestamp_from_datetime(agreement.outcome_notice_date)
    data[outcome_notice_alert_key] = {
      'due-date': outcome_notice_date,
      'agreement-id': agreement.id,
      'agreement-name': agreement.name,
      'alert-type': 'outcomeNotice'
    }

  result = client.patch('users-alerts/{user_id}'.format(user_id=agreement.user_id), data)

  return result
