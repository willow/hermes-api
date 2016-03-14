from django.utils import timezone

from src.domain.common.enums import DurationTypeEnum
from src.domain.agreement_type import services as agreement_type_service
from src.domain.asset import services as asset_service
from src.libs.datetime_utils.datetime_utils import get_timestamp_from_datetime
from src.libs.firebase_utils.services import firebase_provider


def save_agreement_edit_in_firebase(agreement_id,
                                    name=None,
                                    user_id=None,
                                    counterparty=None,
                                    description=None,
                                    execution_date=None,
                                    agreement_type_id=None,
                                    term_length_time_amount=None,
                                    term_length_time_type=None,
                                    auto_renew=None,
                                    outcome_notice_time_amount=None,
                                    outcome_notice_time_type=None,
                                    duration_details=None,
                                    outcome_notice_alert_enabled=None,
                                    outcome_notice_alert_time_amount=None,
                                    outcome_notice_alert_time_type=None,
                                    expiration_alert_enabled=None,
                                    expiration_alert_time_amount=None,
                                    expiration_alert_time_type=None,
                                    _firebase_provider=None,
                                    **kwargs
                                    ):
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  if execution_date:
    execution_date = get_timestamp_from_datetime(execution_date)
  else:
    execution_date = None

  if outcome_notice_time_type:
    outcome_notice_type = DurationTypeEnum(outcome_notice_time_type).name
  else:
    outcome_notice_type = None

  if term_length_time_type:
    term_length_type = DurationTypeEnum(term_length_time_type).name
  else:
    term_length_type = None

  if outcome_notice_alert_time_type:
    outcome_notice_alert_time_type = DurationTypeEnum(outcome_notice_alert_time_type).name
  else:
    outcome_notice_alert_time_type = None

  if expiration_alert_time_type:
    expiration_alert_time_type = DurationTypeEnum(expiration_alert_time_type).name
  else:
    expiration_alert_time_type = None

  data = {
    'auto-renew': auto_renew,
    'counterparty': counterparty,
    'description': description,
    'duration-details': duration_details,
    'execution-date': execution_date,
    'name': name,
    'outcome-notice-time-amount': outcome_notice_time_amount,
    'outcome-notice-time-type': outcome_notice_type,
    'outcome-notice-alert-enabled': outcome_notice_alert_enabled,
    'outcome-notice-alert-time-amount': outcome_notice_alert_time_amount,
    'outcome-notice-alert-time-type': outcome_notice_alert_time_type,
    'expiration-alert-enabled': expiration_alert_enabled,
    'expiration-alert-time-amount': expiration_alert_time_amount,
    'expiration-alert-time-type': expiration_alert_time_type,
    'term-length-time-amount': term_length_time_amount,
    'term-length-time-type': term_length_type,
    'type-id': agreement_type_id,
    'viewers': {user_id: True},
  }

  result = client.put('/agreement-edits', agreement_id, data)

  return result


def save_agreement_detail_in_firebase(agreement_id,
                                      name,
                                      user_id,
                                      counterparty,
                                      description,
                                      execution_date,
                                      agreement_type_id,
                                      artifact_ids,
                                      term_length_time_amount,
                                      term_length_time_type,
                                      _agreement_type_service=None,
                                      _asset_service=None,
                                      _firebase_provider=None,
                                      **kwargs):
  if not _agreement_type_service: _agreement_type_service = agreement_type_service
  if not _asset_service: _asset_service = asset_service
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  # this task is only fired after a potential agreement is complete, so it's safe to assume an execution date is present
  execution_date = get_timestamp_from_datetime(execution_date)

  if term_length_time_amount:
    term_length_type = DurationTypeEnum(term_length_time_type).name
  else:
    term_length_type = None

  agreement_type_name = None
  if agreement_type_id:
    agreement_type_name = _agreement_type_service.get_agreement_type_lookup(agreement_type_id).name

  assets = (_asset_service.get_asset_lookup(artifact_id) for artifact_id in artifact_ids)
  artifacts = {a.id: {'name': a.name} for a in assets}
  data = {
    'counterparty': counterparty,
    'description': description,
    'execution-date': execution_date,
    'name': name,
    'term-length-time-amount': term_length_time_amount,
    'term-length-time-type': term_length_type,
    'type-name': agreement_type_name,
    'artifacts': artifacts,
    'viewers': {user_id: True}
  }

  result = client.put('/agreement-details', agreement_id, data)

  return result


def save_user_agreement_in_firebase(agreement_id,
                                    name,
                                    user_id,
                                    counterparty,
                                    execution_date,
                                    agreement_type_id,
                                    artifact_ids,
                                    _agreement_type_service=None,
                                    _firebase_provider=None,
                                    **kwargs):
  if not _agreement_type_service: _agreement_type_service = agreement_type_service
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  # this task is only fired after a potential agreement is complete, so it's safe to assume an execution date is present
  execution_date = get_timestamp_from_datetime(execution_date)

  modification_date = get_timestamp_from_datetime(timezone.now())

  agreement_type_name = None
  if agreement_type_id:
    agreement_type_name = _agreement_type_service.get_agreement_type_lookup(agreement_type_id).name

  data = {
    'counterparty': counterparty,
    'artifact-count': len(artifact_ids),
    'execution-date': execution_date,
    'modification-date': modification_date,
    'name': name,
    'type-name': agreement_type_name,
  }

  result = client.put('users-agreements/{user_id}'.format(user_id=user_id), agreement_id, data)

  return result


def save_agreement_alerts_in_firebase(agreement_id, name,
                                      user_id,
                                      expiration_alert_created=None,
                                      outcome_date=None,
                                      outcome_notice_alert_created=None,
                                      outcome_notice_date=None,
                                      _firebase_provider=None):
  if not _firebase_provider: _firebase_provider = firebase_provider
  client = _firebase_provider.get_firebase_client()

  data = {}

  if outcome_notice_alert_created:
    outcome_notice_alert_key = '{0}-{1}'.format(agreement_id, 'outcome-notice-alert')
    outcome_notice_date = get_timestamp_from_datetime(outcome_notice_date)
    data[outcome_notice_alert_key] = {
      'due-date': outcome_notice_date,
      'agreement-id': agreement_id,
      'agreement-name': name,
      'alert-type': 'outcomeNotice'
    }

  if expiration_alert_created:
    exp_alert_key = '{0}-{1}'.format(agreement_id, 'expiration-alert')
    exp_date = get_timestamp_from_datetime(outcome_date)
    data[exp_alert_key] = {
      'due-date': exp_date,
      'agreement-id': agreement_id,
      'agreement-name': name,
      'alert-type': 'expiration'
    }

  result = client.patch('users-alerts/{user_id}'.format(user_id=user_id), data)

  return result


def delete_agreements_in_firebase(agreement_id, user_id, _firebase_provider=None):
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  result = []
  result.append(client.delete('users-agreements/{user_id}'.format(user_id=user_id), agreement_id))
  result.append(client.delete('/agreement-edits', agreement_id))
  result.append(client.delete('/agreement-details', agreement_id))

  return result
