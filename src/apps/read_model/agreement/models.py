from django.db import models, transaction
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from jsonfield import JSONField
from simplejson.encoder import JSONEncoder

from src.aggregates.agreement.signals import created, updated_attrs, outcome_notice_alert_sent, \
  expiration_alert_sent
from src.aggregates.common.enums import DurationTypeDict
from src.libs.common_domain.models import Event, AggregateModelBase


class Agreement(AggregateModelBase):
  name = models.CharField(max_length=2400)

  artifacts = JSONField(default=list, dump_kwargs={'cls': JSONEncoder})  # simplejson encodes namedtuples

  user = models.ForeignKey('user.User', 'id', related_name='agreements')

  counterparty = models.CharField(max_length=2400)

  agreement_type = models.ForeignKey('agreement_type.AgreementType', 'id', related_name='agreements', blank=True,
                                     null=True)

  description = models.TextField(blank=True, null=True)

  execution_date = models.DateTimeField()
  outcome_date = models.DateTimeField(blank=True, null=True)

  term_length_time_amount = models.PositiveSmallIntegerField(blank=True, null=True)
  term_length_time_type = models.PositiveSmallIntegerField(blank=True, null=True)

  auto_renew = models.BooleanField()
  outcome_notice_time_amount = models.PositiveSmallIntegerField(blank=True, null=True)
  outcome_notice_time_type = models.PositiveSmallIntegerField(blank=True, null=True)
  outcome_notice_date = models.DateTimeField(blank=True, null=True)

  outcome_notice_alert_enabled = models.BooleanField()
  outcome_notice_alert_time_amount = models.PositiveSmallIntegerField(blank=True, null=True)
  outcome_notice_alert_time_type = models.PositiveSmallIntegerField(blank=True, null=True)
  outcome_notice_alert_created = models.BooleanField()
  outcome_notice_alert_expired = models.BooleanField()
  outcome_notice_alert_date = models.DateTimeField(blank=True, null=True)

  expiration_alert_enabled = models.BooleanField()
  expiration_alert_time_amount = models.PositiveSmallIntegerField(blank=True, null=True)
  expiration_alert_time_type = models.PositiveSmallIntegerField(blank=True, null=True)
  expiration_alert_created = models.BooleanField()
  expiration_alert_expired = models.BooleanField()
  expiration_alert_date = models.DateTimeField(blank=True, null=True)

  duration_details = models.TextField(blank=True, null=True)

  system_created_date = models.DateTimeField()

  @classmethod
  def _from_attrs(cls, **kwargs):
    ret_val = cls()

    ret_val._validate_args(**kwargs)

    execution_date = kwargs.get('execution_date')

    outcome_date = ret_val._get_outcome_date(
      execution_date,
      kwargs.get('term_length_time_type'),
      kwargs.get('term_length_time_amount')
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

    expiration_alert_date = ret_val._get_expiration_alert_date(
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

    ret_val._raise_event(created, **created_data)

    return ret_val

  def update_attrs(self, **kwargs):

    self._validate_args(**kwargs)

    execution_date = kwargs.get('execution_date')

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

    new_attrs = dict({
      'outcome_date': outcome_date,
      'outcome_notice_date': outcome_notice_date,
      'outcome_notice_alert_date': outcome_notice_alert_date,
      'expiration_alert_date': expiration_alert_date,
    }, **kwargs)

    self._raise_event(updated_attrs, **new_attrs)

  def send_outcome_notice_alert_if_due(self):
    past_due = timezone.now() >= self.outcome_notice_alert_date
    if past_due and self.outcome_notice_alert_enabled and not self.outcome_notice_alert_created:
      self._raise_event(outcome_notice_alert_sent, id=self.id)

  def send_expiration_alert_if_due(self):
    past_due = timezone.now() >= self.expiration_alert_date
    if past_due and self.expiration_alert_enabled and not self.expiration_alert_created:
      self._raise_event(expiration_alert_sent, id=self.id)

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

  def _handle_created_event(self, **kwargs):
    self.id = kwargs['id']
    self.artifacts = kwargs['artifacts']
    self.user_id = kwargs['user_id']
    self.system_created_date = kwargs['system_created_date']

    self.outcome_notice_alert_created = False
    self.outcome_notice_alert_expired = False
    self.expiration_alert_created = False
    self.expiration_alert_expired = False

    self._update_attrs(**kwargs)

  def _handle_updated_attrs_event(self, **kwargs):
    self._update_attrs(**kwargs)

  def _validate_args(self, **kwargs):
    if not kwargs.get('name'):
      raise ValueError("name is required")

    if not kwargs.get('counterparty'):
      raise ValueError("counterparty is required")

    if not kwargs.get('execution_date'):
      raise ValueError("execution_date is required")

  def _handle_outcome_notice_alert_sent_event(self, **kwargs):
    self.outcome_notice_alert_created = True

  def _handle_expiration_alert_sent_event(self, **kwargs):
    self.expiration_alert_created = True

  def __str__(self):
    return 'Agreement {id}: {name}'.format(id=self.id, name=self.name)

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)

        for event in self._uncommitted_events:
          Event.objects.create(
            aggregate_name=self.__class__.__name__, aggregate_id=self.id,
            event_name=event.event_fq_name, event_version=event.version, event_data=event
          )

      # don't send events until successful commit
      self.send_events()
    else:
      from src.apps.read_model.agreement.services import service

      service.save_or_update(self)
