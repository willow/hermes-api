from dateutil.relativedelta import relativedelta
from django.utils import timezone

from src.aggregates.agreement.events import AgreementCreated1, AgreementAttrsUpdated1, AgreementExpirationAlertSent1, \
  AgreementOutcomeNoticeAlertSent1
from src.aggregates.common.enums import DurationTypeDict
from src.libs.common_domain.aggregate_base import AggregateBase


class PotentialAgreement(AggregateBase):
  def __init__(self, id, name, artifacts, user_id, system_created_date):
    super().__init__()

    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    if not artifacts:
      raise TypeError("artifacts is required")

    if not user_id:
      raise TypeError("user_id is required")

    if not system_created_date:
      raise TypeError("system_created_date is required")

    self._raise_event(PotentialAgreementCreated1(**created_data))

  def complete(self, **kwargs):

    if self.completed:
      raise Exception("potential agreement {0} already completed".format(self.id))

    if not kwargs.get('name'):
      raise ValueError("name is required")

    if not kwargs.get('counterparty'):
      raise ValueError("counterparty is required")

    if not kwargs.get('execution_date'):
      raise ValueError("execution_date is required")

    self._raise_event(PotentialAgreementCompleted(**kwargs))

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name

    self.completed = False

  def _handle_attrs_updated_1_event(self, event):
    data = event.data

    self.name = data['name']
    self.counterparty = data['counterparty']
    self.description = data['description']
    self.execution_date = data['execution_date']
    self.agreement_type_id = data['agreement_type_id']
    self.counterparty = data['counterparty']
    self.term_length_time_amount = data['term_length_time_amount']
    self.term_length_time_type = data['term_length_time_type']
    self.auto_renew = data['auto_renew']
    self.outcome_notice_time_amount = data['outcome_notice_time_amount']
    self.outcome_notice_time_type = data['outcome_notice_time_type']
    self.duration_details = data['duration_details']
    self.outcome_notice_alert_enabled = data['outcome_notice_alert_enabled']
    self.outcome_notice_alert_time_amount = data[
      'outcome_notice_alert_time_amount']
    self.outcome_notice_alert_time_type = data[
      'outcome_notice_alert_time_type']
    self.expiration_alert_enabled = data['expiration_alert_enabled']
    self.expiration_alert_time_amount = data['expiration_alert_time_amount']
    self.expiration_alert_time_type = data['expiration_alert_time_type']

  def __str__(self):
    class_name = self.__class__.__name__
    return '{class_name} {id}: {name}'.format(class_name=class_name, id=self.id, name=self.name)
