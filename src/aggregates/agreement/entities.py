from dateutil.relativedelta import relativedelta
from django.utils import timezone

from src.aggregates.agreement.events import AgreementCreated1, AgreementAttrsUpdated1, AgreementExpirationAlertSent1, \
  AgreementOutcomeNoticeAlertSent1
from src.aggregates.common.enums import DurationTypeDict
from src.libs.common_domain.aggregate_base import AggregateBase


class Agreement(AggregateBase):
  def __init__(self, **kwargs):
    super().__init__()

    if not kwargs.get('id'):
      raise TypeError("id is required")

    if not kwargs.get('artifacts'):
      raise TypeError("artifacts is required")

    if not kwargs.get('user_id'):
      raise TypeError("user_id is required")

    if not kwargs.get('system_created_date'):
      raise TypeError("system_created_date is required")

    execution_date = kwargs.get('execution_date')

    self._validate_args(**kwargs)

    outcome_date = self._get_outcome_date(
      execution_date,
      kwargs.get('term_length_time_type'),
      kwargs.get('term_length_time_amount')
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

    expiration_alert_date = self._get_expiration_alert_date(
      outcome_date,
      kwargs.get('expiration_alert_enabled'),
      kwargs.get('expiration_alert_time_amount'),
      kwargs.get('expiration_alert_time_type')
    )

    created_data = dict({
      'outcome_date': outcome_date,
      'outcome_notice_date': outcome_notice_date,
      'outcome_notice_alert_date': outcome_notice_alert_date,
      'expiration_alert_date': expiration_alert_date,
    }, **kwargs)

    self._raise_event(AgreementCreated1(**created_data))

  def update_attrs(self, execution_date=None, term_length_time_amount=None, term_length_time_type=None,
                   outcome_notice_time_amount=None, outcome_notice_alert_time_type=None,
                   outcome_notice_alert_time_amount=None,
                   outcome_notice_alert_enabled=None,
                   expiration_alert_time_type=None,
                   expiration_alert_time_amount=None,
                   expiration_alert_enabled=None, **kwargs):

    self._validate_args(**kwargs)

    execution_date = execution_date

    outcome_date = self._get_outcome_date(
      execution_date,
      term_length_time_type,
      term_length_time_amount
    )

    outcome_notice_date = self._get_outcome_notice_date(
      outcome_date,
      outcome_notice_alert_time_type,
      outcome_notice_time_amount
    )

    outcome_notice_alert_date = self._get_outcome_notice_alert_date(
      outcome_notice_date,
      outcome_notice_alert_enabled,
      outcome_notice_alert_time_amount,
      outcome_notice_alert_time_type
    )

    expiration_alert_date = self._get_expiration_alert_date(
      outcome_date,
      expiration_alert_enabled,
      expiration_alert_time_amount,
      expiration_alert_time_type
    )

    new_attrs = dict({
      'outcome_date': outcome_date,
      'outcome_notice_date': outcome_notice_date,
      'outcome_notice_alert_date': outcome_notice_alert_date,
      'expiration_alert_date': expiration_alert_date,
    }, **kwargs)

    self._raise_event(AgreementAttrsUpdated1(**new_attrs))

  def send_outcome_notice_alert_if_due(self):
    past_due = timezone.now() >= self.outcome_notice_alert_date
    if past_due and self.outcome_notice_alert_enabled and not self.outcome_notice_alert_created:
      self._raise_event(AgreementOutcomeNoticeAlertSent1(self.id))

  def send_expiration_alert_if_due(self):
    past_due = timezone.now() >= self.expiration_alert_date
    if past_due and self.expiration_alert_enabled and not self.expiration_alert_created:
      self._raise_event(AgreementExpirationAlertSent1(self.id))

  def _validate_args(self, **kwargs):
    if not kwargs.get('name'):
      raise ValueError("name is required")

    if not kwargs.get('counterparty'):
      raise ValueError("counterparty is required")

    if not kwargs.get('execution_date'):
      raise ValueError("execution_date is required")

  def _update_attrs(self, event):
    data = event.data
    self.name = data['name']
    self.counterparty = data['counterparty']
    self.description = data['description']
    self.execution_date = data['execution_date']
    self.outcome_date = data['outcome_date']
    self.agreement_type_id = data['agreement_type_id']
    self.counterparty = data['counterparty']
    self.term_length_time_amount = data['term_length_time_amount']
    self.term_length_time_type = data['term_length_time_type']
    self.auto_renew = data['auto_renew']
    self.outcome_notice_time_amount = data['outcome_notice_time_amount']
    self.outcome_notice_time_type = data['outcome_notice_time_type']
    self.outcome_notice_date = data['outcome_notice_date']
    self.duration_details = data['duration_details']
    self.outcome_notice_alert_enabled = data['outcome_notice_alert_enabled']
    self.outcome_notice_alert_time_amount = data[
      'outcome_notice_alert_time_amount']
    self.outcome_notice_alert_time_type = data[
      'outcome_notice_alert_time_type']
    self.outcome_notice_alert_date = data['outcome_notice_alert_date']
    self.expiration_alert_enabled = data['expiration_alert_enabled']
    self.expiration_alert_time_amount = data['expiration_alert_time_amount']
    self.expiration_alert_time_type = data['expiration_alert_time_type']
    self.expiration_alert_date = data['expiration_alert_date']

  def _get_outcome_date(self, execution_date, term_length_time_type,
                        term_length_time_amount):
    # what is the next outcome date?
    # execution date + term length.
    # it's probably safe to assume time_type is always specified.
    if term_length_time_amount:
      outcome_relative_time_modifier = DurationTypeDict[term_length_time_type].lower()
      kwargs = {outcome_relative_time_modifier: term_length_time_amount}
      outcome_date = execution_date + relativedelta(**kwargs)
    else:
      outcome_date = None

    return outcome_date

  def _get_outcome_notice_alert_date(self, outcome_notice_date,
                                     outcome_notice_alert_enabled,
                                     outcome_notice_alert_time_amount,
                                     outcome_notice_alert_time_type):
    # if outcome_notice alert enabled
    # if we have an outcome_notice date specified
    # it's probably safe to assume time_type is always specified
    if outcome_notice_alert_enabled and outcome_notice_date:
      outcome_notice_relative_time_modifier = DurationTypeDict[
        outcome_notice_alert_time_type].lower()

      kwargs = {outcome_notice_relative_time_modifier: outcome_notice_alert_time_amount}
      outcome_notice_alert_date = outcome_notice_date - relativedelta(**kwargs)
    else:
      outcome_notice_alert_date = None

    return outcome_notice_alert_date

  def _get_expiration_alert_date(self, outcome_date, expiration_alert_enabled,
                                 expiration_alert_time_amount,
                                 expiration_alert_time_type):
    # if expiration alert enabled
    # if we have an expiration date specified
    # it's probably safe to assume time_type is always specified
    if expiration_alert_enabled and outcome_date:
      expiration_relative_time_modifier = DurationTypeDict[expiration_alert_time_type].lower()
      kwargs = {expiration_relative_time_modifier: expiration_alert_time_amount}
      expiration_alert_date = outcome_date - relativedelta(**kwargs)
    else:
      expiration_alert_date = None

    return expiration_alert_date

  def _get_outcome_notice_date(self, outcome_date,
                               outcome_notice_alert_time_type,
                               outcome_notice_time_amount):
    # it's probably safe to assume time_type is always specified.
    if outcome_notice_time_amount and outcome_date:
      outcome_notice_relative_time_modifier = DurationTypeDict[
        outcome_notice_alert_time_type].lower()
      kwargs = {outcome_notice_relative_time_modifier: outcome_notice_time_amount}
      outcome_notice_date = outcome_date - relativedelta(**kwargs)
    else:
      outcome_notice_date = None

    return outcome_notice_date

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name
    self.system_created_date = event.system_created_date

    self.outcome_notice_alert_created = False
    self.outcome_notice_alert_expired = False
    self.expiration_alert_created = False
    self.expiration_alert_expired = False

    self._update_attrs(**event.data)

  def _handle_attrs_updated_1_event(self, event):
    self._update_attrs(**event.data)

  def __str__(self):
    return 'Agreement {id}: {name}'.format(id=self.id, name=self.name)
