from django.db import models, transaction
from jsonfield import JSONField

from simplejson.encoder import JSONEncoder

from src.aggregates.potential_agreement.signals import created, completed
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import Event


class PotentialAgreement(models.Model, AggregateBase):
  uid = models.CharField(max_length=8, unique=True)
  name = models.CharField(max_length=2400)

  artifacts = JSONField(default=list, dump_kwargs={'cls': JSONEncoder})  # simplejson encodes namedtuples

  user = models.ForeignKey('user.User', 'uid', related_name='potential_agreements')

  counterparty = models.CharField(max_length=2400, blank=True, null=True)

  agreement_type = models.ForeignKey('agreement_type.AgreementType', 'uid', related_name='potential_agreements',
                                     blank=True, null=True)

  description = models.TextField(blank=True, null=True)

  execution_date = models.DateTimeField(blank=True, null=True)

  term_length_time_amount = models.PositiveSmallIntegerField(blank=True, null=True)
  term_length_time_type = models.PositiveSmallIntegerField(blank=True, null=True)

  auto_renew = models.NullBooleanField(blank=True, null=True)
  outcome_notice_time_amount = models.PositiveSmallIntegerField(blank=True, null=True)
  outcome_notice_time_type = models.PositiveSmallIntegerField(blank=True, null=True)

  outcome_notice_alert_enabled = models.NullBooleanField(blank=True, null=True)
  outcome_notice_alert_time_amount = models.PositiveSmallIntegerField(blank=True, null=True)
  outcome_notice_alert_time_type = models.PositiveSmallIntegerField(blank=True, null=True)

  expiration_alert_enabled = models.NullBooleanField(blank=True, null=True)
  expiration_alert_time_amount = models.PositiveSmallIntegerField(blank=True, null=True)
  expiration_alert_time_type = models.PositiveSmallIntegerField(blank=True, null=True)

  duration_details = models.TextField(blank=True, null=True)

  completed = models.BooleanField()

  system_created_date = models.DateTimeField()

  @classmethod
  def _from_attrs(cls, **kwargs):

    ret_val = cls()

    if not kwargs.get('uid'):
      raise TypeError("uid is required")

    if not kwargs.get('name'):
      raise TypeError("name is required")

    if not kwargs.get('artifacts'):
      raise TypeError("artifacts is required")

    if not kwargs.get('user_uid'):
      raise TypeError("user_uid is required")

    if not kwargs.get('system_created_date'):
      raise TypeError("system_created_date is required")

    ret_val._raise_event(
      created, **kwargs
    )

    return ret_val

  def _handle_created_event(self, **kwargs):
    self.uid = kwargs['uid']
    self.name = kwargs['name']
    self.artifacts = kwargs['artifacts']
    self.user_id = kwargs['user_uid']
    self.system_created_date = kwargs['system_created_date']

    self.completed = False

  def complete(self, **kwargs):

    if self.completed:
      raise Exception("potential agreement {0} already completed".format(self.uid))

    if not kwargs.get('name'):
      raise ValueError("name is required")

    if not kwargs.get('counterparty'):
      raise ValueError("counterparty is required")

    if not kwargs.get('execution_date'):
      raise ValueError("execution_date is required")

    self._raise_event(completed, **kwargs)

  def _handle_completed_event(self, **kwargs):
    self.name = kwargs['name']
    self.counterparty = kwargs['counterparty']
    self.description = kwargs['description']
    self.execution_date = kwargs['execution_date']
    self.agreement_type_id = kwargs['agreement_type_id']
    self.counterparty = kwargs['counterparty']
    self.term_length_time_amount = kwargs['term_length_time_amount']
    self.term_length_time_type = kwargs['term_length_time_type']
    self.auto_renew = kwargs['auto_renew']
    self.outcome_notice_time_amount = kwargs['outcome_notice_time_amount']
    self.outcome_notice_time_type = kwargs['outcome_notice_time_type']
    self.duration_details = kwargs['duration_details']
    self.outcome_notice_alert_enabled = kwargs['outcome_notice_alert_enabled']
    self.outcome_notice_alert_time_amount = kwargs[
      'outcome_notice_alert_time_amount']
    self.outcome_notice_alert_time_type = kwargs[
      'outcome_notice_alert_time_type']
    self.expiration_alert_enabled = kwargs['expiration_alert_enabled']
    self.expiration_alert_time_amount = kwargs['expiration_alert_time_amount']
    self.expiration_alert_time_type = kwargs['expiration_alert_time_type']

    self.completed = True

  def __str__(self):
    return 'PotentialAgreement #' + str(self.uid) + ': ' + self.name

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)

        for event in self._uncommitted_events:
          Event.objects.create(
            aggregate_name=self.__class__.__name__, aggregate_id=self.uid,
            event_name=event.event_fq_name, event_version=event.version, event_data=event.kwargs
          )

      # don't send events until successful commit
      self.send_events()
    else:
      from src.aggregates.potential_agreement.services import service

      service.save_or_update(self)
