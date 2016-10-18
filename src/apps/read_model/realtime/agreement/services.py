from django.utils import timezone

from src.domain.agreement_type import services as agreement_type_service
from src.domain.asset import services as asset_service
from src.libs.datetime_utils.datetime_utils import get_timestamp_from_datetime
from src.libs.firebase_utils.services import firebase_provider
from src.libs.firebase_utils.value.value_utils import _provide_params


def save_agreement_edit_in_firebase(agreement_id, _firebase_provider=None, **kwargs):
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  data = {}

  _provide_params('user_id', 'viewers', data, lambda user_id: {user_id: True}, **kwargs)

  _provide_params('execution_date', 'execution-date', data, lambda v: get_timestamp_from_datetime(v), **kwargs)
  _provide_params('auto_renew', 'auto-renew', data, **kwargs)
  _provide_params('counterparty', 'counterparty', data, **kwargs)
  _provide_params('duration_details', 'duration-details', data, **kwargs)
  _provide_params('name', 'name', data, **kwargs)
  _provide_params('description', 'description', data, **kwargs)

  _provide_params('outcome_alert_enabled', 'outcome-alert-enabled', data, **kwargs)
  _provide_params('outcome_alert_time_amount', 'outcome-alert-time-amount', data, **kwargs)
  _provide_params('outcome_alert_time_type', 'outcome-alert-time-type', data, **kwargs)

  _provide_params('outcome_notice_time_amount', 'outcome-notice-time-amount', data, **kwargs)
  _provide_params('outcome_notice_time_type', 'outcome-notice-time-type', data, **kwargs)

  _provide_params('outcome_notice_alert_time_type', 'outcome-notice-alert-time-type', data, **kwargs)
  _provide_params('outcome_notice_alert_enabled', 'outcome-notice-alert-enabled', data, **kwargs)
  _provide_params('outcome_notice_alert_time_amount', 'outcome-notice-alert-time-amount', data, **kwargs)

  _provide_params('term_length_time_amount', 'term-length-time-amount', data, **kwargs)
  _provide_params('term_length_time_type', 'term-length-time-type', data, **kwargs)

  _provide_params('agreement_type_id', 'type-id', data, **kwargs)

  result = client.patch('/agreement-edits/{0}'.format(agreement_id), data)

  return result


def save_agreement_detail_in_firebase(agreement_id, _agreement_type_service=None, _asset_service=None,
                                      _firebase_provider=None, **kwargs):
  if not _agreement_type_service: _agreement_type_service = agreement_type_service
  if not _asset_service: _asset_service = asset_service
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  data = {}

  _provide_params('execution_date', 'execution-date', data, lambda v: get_timestamp_from_datetime(v), **kwargs)
  _provide_params('term_length_time_amount', 'term-length-time-amount', data, **kwargs)
  _provide_params('agreement_type_id', 'type-name', data,
                  lambda v: _agreement_type_service.get_agreement_type_lookup(v).name, **kwargs)

  artifact_ids = kwargs.get('artifact_ids')

  if artifact_ids is not None:
    assets = (_asset_service.get_asset_lookup(artifact_id) for artifact_id in artifact_ids)
    artifacts = {a.id: {'name': a.name} for a in assets}
    data['artifacts'] = artifacts

  _provide_params('user_id', 'viewers', data, lambda user_id: {user_id: True}, **kwargs)

  _provide_params('term_length_time_amount', 'term-length-time-amount', data, **kwargs)
  _provide_params('term_length_time_type', 'term-length-time-type', data, **kwargs)
  _provide_params('name', 'name', data, **kwargs)
  _provide_params('counterparty', 'counterparty', data, **kwargs)
  _provide_params('description', 'description', data, **kwargs)

  result = client.patch('/agreement-details/{0}'.format(agreement_id), data)

  return result


def save_user_agreement_in_firebase(agreement_id, _agreement_type_service=None, _firebase_provider=None, **kwargs):
  if not _agreement_type_service: _agreement_type_service = agreement_type_service
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()
  data = {}

  user_id = kwargs['user_id']

  _provide_params('execution_date', 'execution-date', data, lambda v: get_timestamp_from_datetime(v), **kwargs)

  modification_date = get_timestamp_from_datetime(timezone.now())
  data['modification-date'] = modification_date

  _provide_params('agreement_type_id', 'type-name', data,
                  lambda v: _agreement_type_service.get_agreement_type_lookup(v).name, **kwargs)

  _provide_params('counterparty', 'counterparty', data, **kwargs)
  _provide_params('name', 'name', data, **kwargs)

  artifact_ids = kwargs.get('artifact_ids')
  if artifact_ids is not None:
    data['artifact-count'] = len(artifact_ids)

  result = client.patch('users-agreements/{user_id}/{agreement_id}'.format(user_id=user_id, agreement_id=agreement_id),
                        data)

  return result


def save_agreement_alerts_in_firebase(agreement_id, name,
                                      user_id,
                                      outcome_alert_created=None,
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

  if outcome_alert_created:
    outcome_alert_key = '{0}-{1}'.format(agreement_id, 'outcome-alert')
    outcome_date = get_timestamp_from_datetime(outcome_date)
    data[outcome_alert_key] = {
      'due-date': outcome_date,
      'agreement-id': agreement_id,
      'agreement-name': name,
      'alert-type': 'outcome'
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
