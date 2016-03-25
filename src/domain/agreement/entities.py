from dateutil.relativedelta import relativedelta
from django.utils import timezone

from src.domain.agreement.events import AgreementCreated1, AgreementAttrsUpdated1, AgreementOutcomeAlertSent1, \
  AgreementOutcomeNoticeAlertSent1, AgreementDeleted1, ArtifactDeleted1, ArtifactCreated1
from src.domain.common.value_objects.time_type import TimeType
from src.libs.common_domain.aggregate_base import AggregateBase


class Agreement(AggregateBase):
  @classmethod
  def from_attrs(cls, **kwargs):
    ret_val = cls()
    if not kwargs.get('id'):
      raise TypeError("id is required")

    if not kwargs.get('artifact_ids'):
      raise TypeError("artifact_ids is required")

    if not kwargs.get('user_id'):
      raise TypeError("user_id is required")

    if not kwargs.get('system_created_date'):
      raise TypeError("system_created_date is required")

    execution_date = kwargs.get('execution_date')

    ret_val._validate_args(**kwargs)

    outcome_date = ret_val._get_outcome_date(
      execution_date,
      kwargs.get('term_length_time_type'),
      kwargs.get('term_length_time_amount')
    )

    outcome_alert_date = ret_val._get_outcome_alert_date(
      outcome_date,
      kwargs.get('outcome_alert_enabled'),
      kwargs.get('outcome_alert_time_amount'),
      kwargs.get('outcome_alert_time_type')
    )

    outcome_notice_date = ret_val._get_outcome_notice_date(
      outcome_date,
      kwargs.get('outcome_notice_alert_time_type'),
      kwargs.get('outcome_notice_time_amount')
    )

    outcome_notice_alert_date = ret_val._get_outcome_notice_alert_date(
      outcome_notice_date,
      kwargs.get('outcome_notice_alert_enabled'),
      kwargs.get('outcome_notice_alert_time_amount'),
      kwargs.get('outcome_notice_alert_time_type')
    )

    created_data = dict({
      'outcome_date': outcome_date,
      'outcome_alert_created': False,
      'outcome_alert_expired': False,
      'outcome_alert_date': outcome_alert_date,
      'outcome_notice_alert_created': False,
      'outcome_notice_alert_expired': False,
      'outcome_notice_date': outcome_notice_date,
      'outcome_notice_alert_date': outcome_notice_alert_date,
    }, **kwargs)

    ret_val._raise_event(AgreementCreated1(**created_data))

    return ret_val

  def update_attrs(self, **kwargs):

    self._validate_args(**kwargs)

    execution_date = kwargs.get('execution_date')

    outcome_date = self._get_outcome_date(
      execution_date,
      kwargs.get('term_length_time_type'),
      kwargs.get('term_length_time_amount')
    )

    outcome_alert_date = self._get_outcome_alert_date(
      outcome_date,
      kwargs.get('outcome_alert_enabled'),
      kwargs.get('outcome_alert_time_amount'),
      kwargs.get('outcome_alert_time_type')
    )

    outcome_notice_date = self._get_outcome_notice_date(
      outcome_date,
      kwargs.get('outcome_notice_alert_time_type'),
      kwargs.get('outcome_notice_time_amount')
    )

    outcome_notice_alert_date = self._get_outcome_notice_alert_date(
      outcome_notice_date,
      kwargs.get('outcome_notice_alert_enabled'),
      kwargs.get('outcome_notice_alert_time_amount'),
      kwargs.get('outcome_notice_alert_time_type')
    )

    new_attrs = dict({
      'user_id': self.user_id,
      'outcome_date': outcome_date,
      'outcome_alert_date': outcome_alert_date,
      'outcome_notice_date': outcome_notice_date,
      'outcome_notice_alert_date': outcome_notice_alert_date,
    }, **kwargs)

    self._raise_event(AgreementAttrsUpdated1(**new_attrs))

  def send_outcome_alert_if_due(self):
    past_due = timezone.now() >= self.outcome_alert_date

    if past_due and self.outcome_alert_enabled and not self.outcome_alert_created:
      self._raise_event(
        AgreementOutcomeAlertSent1(
          self.name, self.user_id,
          self.outcome_date, True, self.outcome_notice_date,
          self.outcome_notice_alert_created,
        )
      )

  def send_outcome_notice_alert_if_due(self):
    past_due = timezone.now() >= self.outcome_notice_alert_date

    if past_due and self.outcome_notice_alert_enabled and not self.outcome_notice_alert_created:
      self._raise_event(
        AgreementOutcomeNoticeAlertSent1(
          self.name, self.user_id, self.outcome_date, self.outcome_alert_created,
          self.outcome_notice_date, True,
        )
      )

  def mark_deleted(self):
    if self.is_deleted:
      raise Exception("agreement {0} is already deleted".format(self.id))

    self._raise_event(AgreementDeleted1(self.user_id))

  def delete_artifact(self, artifact_id):
    if artifact_id not in self.artifact_ids:
      raise Exception("artifact {0} doesn't exists".format(artifact_id))
    else:
      remaining_artifact_ids = [aid for aid in self.artifact_ids if aid != artifact_id]
      self._raise_event(ArtifactDeleted1(artifact_id, remaining_artifact_ids, self.user_id))

  def create_artifact(self, artifact_id):
    if artifact_id in self.artifact_ids:
      raise Exception("artifact {0} already exists".format(artifact_id))
    else:
      artifact_ids = self.artifact_ids + [artifact_id]
      self._raise_event(ArtifactCreated1(artifact_id, artifact_ids, self.user_id))

  def _validate_args(self, **kwargs):
    if not kwargs.get('name'):
      raise ValueError("name is required")

    if not kwargs.get('counterparty'):
      raise ValueError("counterparty is required")

    if not kwargs.get('execution_date'):
      raise ValueError("execution_date is required")

  def _update_attrs(self, event):
    data = event.data

    # these fields correspond to AgreementAttrsUpdated event.
    # so it doesn't container user_id, artifacts, alert created, etc.
    self.name = data['name']
    self.counterparty = data['counterparty']
    self.description = data['description']
    self.execution_date = data['execution_date']
    self.outcome_date = data['outcome_date']
    self.agreement_type_id = data['agreement_type_id']
    self.counterparty = data['counterparty']
    self.term_length_time_amount = data['term_length_time_amount']
    self.term_length_time_type = TimeType(data['term_length_time_type'])
    self.auto_renew = data['auto_renew']
    self.outcome_notice_time_amount = data['outcome_notice_time_amount']
    self.outcome_notice_time_type = TimeType(data['outcome_notice_time_type'])
    self.outcome_notice_date = data['outcome_notice_date']
    self.duration_details = data['duration_details']
    self.outcome_alert_enabled = data['outcome_alert_enabled']
    self.outcome_alert_time_amount = data['outcome_alert_time_amount']
    self.outcome_alert_time_type = TimeType(data['outcome_alert_time_type'])
    self.outcome_alert_date = data['outcome_alert_date']
    self.outcome_notice_alert_enabled = data['outcome_notice_alert_enabled']
    self.outcome_notice_alert_time_amount = data['outcome_notice_alert_time_amount']
    self.outcome_notice_alert_time_type = TimeType(data['outcome_notice_alert_time_type'])
    self.outcome_notice_alert_date = data['outcome_notice_alert_date']

  def _get_outcome_date(self, execution_date, term_length_time_type,
                        term_length_time_amount):
    # what is the next outcome date?
    # execution date + term length.
    # it's probably safe to assume time_type is always specified.
    if term_length_time_amount:
      outcome_relative_time_modifier = TimeType(term_length_time_type).time_type_date_format
      kwargs = {outcome_relative_time_modifier: term_length_time_amount}
      outcome_date = execution_date + relativedelta(**kwargs)
    else:
      outcome_date = None

    return outcome_date

  def _get_outcome_alert_date(self, outcome_date, outcome_alert_enabled,
                              outcome_alert_time_amount,
                              outcome_alert_time_type):
    # if outcome alert enabled
    # if we have an outcome date specified
    # it's probably safe to assume time_type is always specified
    if outcome_alert_enabled and outcome_date:
      outcome_relative_time_modifier = TimeType(outcome_alert_time_type).time_type_date_format
      kwargs = {outcome_relative_time_modifier: outcome_alert_time_amount}
      outcome_alert_date = outcome_date - relativedelta(**kwargs)
    else:
      outcome_alert_date = None

    return outcome_alert_date

  def _get_outcome_notice_alert_date(self, outcome_notice_date,
                                     outcome_notice_alert_enabled,
                                     outcome_notice_alert_time_amount,
                                     outcome_notice_alert_time_type):
    # if outcome_notice alert enabled
    # if we have an outcome_notice date specified
    # it's probably safe to assume time_type is always specified
    if outcome_notice_alert_enabled and outcome_notice_date:
      outcome_notice_relative_time_modifier = TimeType(outcome_notice_alert_time_type).time_type_date_format
      kwargs = {outcome_notice_relative_time_modifier: outcome_notice_alert_time_amount}
      outcome_notice_alert_date = outcome_notice_date - relativedelta(**kwargs)
    else:
      outcome_notice_alert_date = None

    return outcome_notice_alert_date

  def _get_outcome_notice_date(self, outcome_date,
                               outcome_notice_alert_time_type,
                               outcome_notice_time_amount):
    # it's probably safe to assume time_type is always specified.
    if outcome_notice_time_amount and outcome_date:
      outcome_notice_relative_time_modifier = TimeType(outcome_notice_alert_time_type).time_type_date_format
      kwargs = {outcome_notice_relative_time_modifier: outcome_notice_time_amount}
      outcome_notice_date = outcome_date - relativedelta(**kwargs)
    else:
      outcome_notice_date = None

    return outcome_notice_date

  def _handle_created_1_event(self, event):
    self.is_deleted = False

    self.outcome_alert_created = event.outcome_alert_created
    self.outcome_alert_expired = event.outcome_alert_expired
    self.outcome_notice_alert_created = event.outcome_notice_alert_created
    self.outcome_notice_alert_expired = event.outcome_notice_alert_expired

    self.id = event.id
    self.system_created_date = event.system_created_date
    self.user_id = event.user_id
    self.artifact_ids = event.artifact_ids

    self._update_attrs(event)

  def _handle_attrs_updated_1_event(self, event):
    self._update_attrs(event)

  def _handle_outcome_alert_sent_1_event(self, event):
    self.outcome_alert_created = event.outcome_alert_created

  def _handle_outcome_notice_alert_sent_1_event(self, event):
    self.outcome_notice_alert_created = event.outcome_notice_alert_created

  def _handle_deleted_1_event(self, event):
    self.is_deleted = True

  def _handle_artifact_created_1_event(self, event):
    self.artifact_ids = event.artifact_ids

  def _handle_artifact_deleted_1_event(self, event):
    self.artifact_ids = event.remaining_artifact_ids

  def method_name(self, artifact_id):
    return [aid for aid in self.artifact_ids if aid != artifact_id]

  def __str__(self):
    return 'Agreement {id}: {name}'.format(id=self.id, name=self.name)
