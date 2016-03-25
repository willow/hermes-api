from src.domain.common.value_objects.time_type import TimeType
from src.domain.potential_agreement.events import PotentialAgreementCreated1, PotentialAgreementCompleted1
from src.libs.common_domain.aggregate_base import AggregateBase


class PotentialAgreement(AggregateBase):
  @classmethod
  def from_attrs(cls, id, name, artifact_ids, user_id, system_created_date):
    ret_val = cls()
    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    if not artifact_ids:
      raise TypeError("artifact_ids is required")

    if not user_id:
      raise TypeError("user_id is required")

    if not system_created_date:
      raise TypeError("system_created_date is required")

    ret_val._raise_event(PotentialAgreementCreated1(id, name, artifact_ids, user_id, system_created_date))

    return ret_val

  def complete(self, **kwargs):

    if self.completed:
      raise Exception("potential agreement {0} already completed".format(self.id))

    if not kwargs.get('name'):
      raise ValueError("name is required")

    if not kwargs.get('counterparty'):
      raise ValueError("counterparty is required")

    if not kwargs.get('execution_date'):
      raise ValueError("execution_date is required")

    kwargs['user_id'] = self.user_id
    kwargs['artifact_ids'] = self.artifact_ids

    self._raise_event(PotentialAgreementCompleted1(**kwargs))

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name
    self.user_id = event.user_id
    self.artifact_ids = event.artifact_ids

    self.completed = False

  def _handle_completed_1_event(self, event):
    data = event.data

    self.name = data['name']
    self.counterparty = data['counterparty']
    self.description = data['description']
    self.execution_date = data['execution_date']
    self.agreement_type_id = data['agreement_type_id']
    self.counterparty = data['counterparty']
    self.term_length_time_amount = data['term_length_time_amount']
    self.term_length_time_type = TimeType(data['term_length_time_type'])
    self.auto_renew = data['auto_renew']
    self.outcome_notice_time_amount = data['outcome_notice_time_amount']
    self.outcome_notice_time_type = TimeType(data['outcome_notice_time_type'])
    self.duration_details = data['duration_details']
    self.outcome_alert_enabled = data['outcome_alert_enabled']
    self.outcome_alert_time_amount = data['outcome_alert_time_amount']
    self.outcome_alert_time_type = TimeType(data['outcome_alert_time_type'])
    self.outcome_notice_alert_enabled = data['outcome_notice_alert_enabled']
    self.outcome_notice_alert_time_amount = data['outcome_notice_alert_time_amount']
    self.outcome_notice_alert_time_type = TimeType(data['outcome_notice_alert_time_type'])

    self.completed = True

  def __str__(self):
    class_name = self.__class__.__name__
    return '{class_name} {id}: {name}'.format(class_name=class_name, id=self.id, name=self.name)
