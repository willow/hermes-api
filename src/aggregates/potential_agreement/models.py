from dateutil.relativedelta import relativedelta

from django.db import models, transaction
from django.utils import timezone
from jsonfield import JSONField
from src.aggregates.potential_agreement.signals import created, completed, updated_attrs, expiration_alert_sent, \
  outcome_notice_alert_sent
from src.apps.agreement.enums import DurationTypeDict
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import Event
from simplejson.encoder import JSONEncoder


class PotentialAgreement(models.Model, AggregateBase):
  potential_agreement_id = models.CharField(max_length=8, unique=True)
  potential_agreement_name = models.CharField(max_length=2400)

  potential_agreement_artifacts = JSONField(default=list,
                                            dump_kwargs={'cls': JSONEncoder})  # simplejson encodes namedtuples

  potential_agreement_user = models.ForeignKey('user.User', 'user_id', related_name='potential_agreements')

  potential_agreement_counterparty = models.CharField(max_length=2400, blank=True, null=True)

  potential_agreement_type = models.ForeignKey('agreement_type.AgreementType', 'agreement_type_id',
                                               related_name='potential_agreements', blank=True, null=True)

  potential_agreement_description = models.TextField(blank=True, null=True)

  potential_agreement_execution_date = models.DateTimeField(blank=True, null=True)
  potential_agreement_outcome_date = models.DateTimeField(blank=True, null=True)

  potential_agreement_term_length_time_amount = models.PositiveSmallIntegerField(blank=True, null=True)
  potential_agreement_term_length_time_type = models.PositiveSmallIntegerField(blank=True, null=True)

  potential_agreement_auto_renew = models.NullBooleanField(blank=True, null=True)
  potential_agreement_outcome_notice_time_amount = models.PositiveSmallIntegerField(blank=True, null=True)
  potential_agreement_outcome_notice_time_type = models.PositiveSmallIntegerField(blank=True, null=True)
  potential_agreement_outcome_notice_date = models.DateTimeField(blank=True, null=True)

  potential_agreement_outcome_notice_alert_enabled = models.NullBooleanField(blank=True, null=True)
  potential_agreement_outcome_notice_alert_time_amount = models.PositiveSmallIntegerField(blank=True, null=True)
  potential_agreement_outcome_notice_alert_time_type = models.PositiveSmallIntegerField(blank=True, null=True)
  potential_agreement_outcome_notice_alert_created = models.BooleanField()
  potential_agreement_outcome_notice_alert_expired = models.BooleanField()
  potential_agreement_outcome_notice_alert_date = models.DateTimeField(blank=True, null=True)

  potential_agreement_expiration_alert_enabled = models.NullBooleanField(blank=True, null=True)
  potential_agreement_expiration_alert_time_amount = models.PositiveSmallIntegerField(blank=True, null=True)
  potential_agreement_expiration_alert_time_type = models.PositiveSmallIntegerField(blank=True, null=True)
  potential_agreement_expiration_alert_created = models.BooleanField()
  potential_agreement_expiration_alert_expired = models.BooleanField()
  potential_agreement_expiration_alert_date = models.DateTimeField(blank=True, null=True)

  potential_agreement_duration_details = models.TextField(blank=True, null=True)

  potential_agreement_completed = models.BooleanField()

  potential_agreement_system_created_date = models.DateTimeField()

  @classmethod
  def _from_attrs(cls, potential_agreement_id, potential_agreement_name, potential_agreement_artifacts,
                  potential_agreement_user_id, potential_agreement_system_created_date):
    ret_val = cls()

    if not potential_agreement_id:
      raise TypeError("potential_agreement_id is required")

    if not potential_agreement_name:
      raise TypeError("potential_agreement_name is required")

    if not potential_agreement_artifacts:
      raise TypeError("potential_agreement_artifacts is required")

    if not potential_agreement_user_id:
      raise TypeError("potential_agreement_user_id is required")

    if not potential_agreement_system_created_date:
      raise TypeError("potential_agreement_system_created_date is required")

    ret_val._raise_event(
      created,
      potential_agreement_id=potential_agreement_id,
      potential_agreement_name=potential_agreement_name,
      potential_agreement_artifacts=potential_agreement_artifacts,
      potential_agreement_user_id=potential_agreement_user_id,
      potential_agreement_system_created_date=potential_agreement_system_created_date,
    )

    return ret_val

  def complete(self, potential_agreement_name, potential_agreement_counterparty, potential_agreement_description,
               potential_agreement_execution_date, potential_agreement_type_id,
               potential_agreement_term_length_time_amount, potential_agreement_term_length_time_type,
               potential_agreement_auto_renew, potential_agreement_outcome_notice_time_amount,
               potential_agreement_outcome_notice_time_type, potential_agreement_duration_details,
               potential_agreement_outcome_notice_alert_enabled,
               potential_agreement_outcome_notice_alert_time_amount,
               potential_agreement_outcome_notice_alert_time_type,
               potential_agreement_expiration_alert_enabled,
               potential_agreement_expiration_alert_time_amount,
               potential_agreement_expiration_alert_time_type,
               ):

    if not potential_agreement_name:
      raise ValueError("potential_agreement_name is required")

    if not potential_agreement_counterparty:
      raise ValueError("potential_agreement_counterparty is required")

    if not potential_agreement_execution_date:
      raise ValueError("potential_agreement_execution_date is required")

    potential_agreement_outcome_date = self._get_outcome_date(
      potential_agreement_execution_date,
      potential_agreement_term_length_time_type,
      potential_agreement_term_length_time_amount
    )

    potential_agreement_outcome_notice_date = self._get_outcome_notice_date(
      potential_agreement_outcome_date,
      potential_agreement_outcome_notice_alert_time_type,
      potential_agreement_outcome_notice_time_amount
    )

    potential_agreement_outcome_notice_alert_date = self._get_outcome_notice_alert_date(
      potential_agreement_outcome_notice_date,
      potential_agreement_outcome_notice_alert_enabled,
      potential_agreement_outcome_notice_alert_time_amount,
      potential_agreement_outcome_notice_alert_time_type
    )

    potential_agreement_expiration_alert_date = self._get_expiration_alert_date(
      potential_agreement_outcome_date,
      potential_agreement_expiration_alert_enabled,
      potential_agreement_expiration_alert_time_amount,
      potential_agreement_expiration_alert_time_type
    )

    # https://app.asana.com/0/10235149247655/87787298394920
    event = updated_attrs if self.potential_agreement_completed else completed

    self._raise_event(
      event,
      potential_agreement_id=self.potential_agreement_id,
      potential_agreement_name=potential_agreement_name,
      potential_agreement_counterparty=potential_agreement_counterparty,
      potential_agreement_description=potential_agreement_description,
      potential_agreement_execution_date=potential_agreement_execution_date,
      potential_agreement_outcome_date=potential_agreement_outcome_date,
      potential_agreement_type_id=potential_agreement_type_id,
      potential_agreement_term_length_time_amount=potential_agreement_term_length_time_amount,
      potential_agreement_term_length_time_type=potential_agreement_term_length_time_type,
      potential_agreement_auto_renew=potential_agreement_auto_renew,
      potential_agreement_outcome_notice_time_amount=potential_agreement_outcome_notice_time_amount,
      potential_agreement_outcome_notice_time_type=potential_agreement_outcome_notice_time_type,
      potential_agreement_outcome_notice_date=potential_agreement_outcome_notice_date,
      potential_agreement_duration_details=potential_agreement_duration_details,
      potential_agreement_outcome_notice_alert_enabled=potential_agreement_outcome_notice_alert_enabled,
      potential_agreement_outcome_notice_alert_time_amount=potential_agreement_outcome_notice_alert_time_amount,
      potential_agreement_outcome_notice_alert_time_type=potential_agreement_outcome_notice_alert_time_type,
      potential_agreement_outcome_notice_alert_date=potential_agreement_outcome_notice_alert_date,
      potential_agreement_expiration_alert_enabled=potential_agreement_expiration_alert_enabled,
      potential_agreement_expiration_alert_time_amount=potential_agreement_expiration_alert_time_amount,
      potential_agreement_expiration_alert_time_type=potential_agreement_expiration_alert_time_type,
      potential_agreement_expiration_alert_date=potential_agreement_expiration_alert_date
    )

  def send_outcome_notice_alert_if_due(self):
    past_due = timezone.now() >= self.potential_agreement_outcome_notice_alert_date
    if past_due and self.potential_agreement_outcome_notice_alert_enabled and not self.potential_agreement_outcome_notice_alert_created:
      self._raise_event(outcome_notice_alert_sent, potential_agreement_id=self.potential_agreement_id)

  def send_expiration_alert_if_due(self):
    past_due = timezone.now() >= self.potential_agreement_expiration_alert_date
    if past_due and self.potential_agreement_expiration_alert_enabled and not self.potential_agreement_expiration_alert_created:
      self._raise_event(expiration_alert_sent, potential_agreement_id=self.potential_agreement_id)

  def _get_outcome_date(self, potential_agreement_execution_date, potential_agreement_term_length_time_type,
                        potential_agreement_term_length_time_amount):
    # what is the next outcome date?
    # execution date + term length.
    # it's probably safe to assume time_type is always specified.
    if potential_agreement_term_length_time_amount:
      outcome_relative_time_modifier = DurationTypeDict[potential_agreement_term_length_time_type].lower()
      kwargs = {outcome_relative_time_modifier: potential_agreement_term_length_time_amount}
      potential_agreement_outcome_date = potential_agreement_execution_date + relativedelta(**kwargs)
    else:
      potential_agreement_outcome_date = None

    return potential_agreement_outcome_date

  def _get_outcome_notice_alert_date(self, potential_agreement_outcome_notice_date,
                                     potential_agreement_outcome_notice_alert_enabled,
                                     potential_agreement_outcome_notice_alert_time_amount,
                                     potential_agreement_outcome_notice_alert_time_type):
    # if outcome_notice alert enabled
    # if we have an outcome_notice date specified
    # it's probably safe to assume time_type is always specified
    if potential_agreement_outcome_notice_alert_enabled and potential_agreement_outcome_notice_date:
      outcome_notice_relative_time_modifier = DurationTypeDict[
        potential_agreement_outcome_notice_alert_time_type].lower()

      kwargs = {outcome_notice_relative_time_modifier: potential_agreement_outcome_notice_alert_time_amount}
      potential_agreement_outcome_notice_alert_date = potential_agreement_outcome_notice_date - relativedelta(**kwargs)
    else:
      potential_agreement_outcome_notice_alert_date = None

    return potential_agreement_outcome_notice_alert_date

  def _get_expiration_alert_date(self, potential_agreement_outcome_date, potential_agreement_expiration_alert_enabled,
                                 potential_agreement_expiration_alert_time_amount,
                                 potential_agreement_expiration_alert_time_type):
    # if expiration alert enabled
    # if we have an expiration date specified
    # it's probably safe to assume time_type is always specified
    if potential_agreement_expiration_alert_enabled and potential_agreement_outcome_date:
      expiration_relative_time_modifier = DurationTypeDict[potential_agreement_expiration_alert_time_type].lower()
      kwargs = {expiration_relative_time_modifier: potential_agreement_expiration_alert_time_amount}
      potential_agreement_expiration_alert_date = potential_agreement_outcome_date - relativedelta(**kwargs)
    else:
      potential_agreement_expiration_alert_date = None

    return potential_agreement_expiration_alert_date

  def _get_outcome_notice_date(self, potential_agreement_outcome_date,
                               potential_agreement_outcome_notice_alert_time_type,
                               potential_agreement_outcome_notice_time_amount):

    # it's probably safe to assume time_type is always specified.
    if potential_agreement_outcome_notice_time_amount and potential_agreement_outcome_date:
      outcome_notice_relative_time_modifier = DurationTypeDict[
        potential_agreement_outcome_notice_alert_time_type].lower()
      kwargs = {outcome_notice_relative_time_modifier: potential_agreement_outcome_notice_time_amount}
      potential_agreement_outcome_notice_date = potential_agreement_outcome_date - relativedelta(**kwargs)
    else:
      potential_agreement_outcome_notice_date = None

    return potential_agreement_outcome_notice_date

  def _handle_created_event(self, **kwargs):
    self.potential_agreement_id = kwargs['potential_agreement_id']
    self.potential_agreement_name = kwargs['potential_agreement_name']
    self.potential_agreement_artifacts = kwargs['potential_agreement_artifacts']
    self.potential_agreement_user_id = kwargs['potential_agreement_user_id']
    self.potential_agreement_system_created_date = kwargs['potential_agreement_system_created_date']

    self.potential_agreement_outcome_notice_alert_created = False
    self.potential_agreement_outcome_notice_alert_expired = False
    self.potential_agreement_expiration_alert_created = False
    self.potential_agreement_expiration_alert_expired = False

    self.potential_agreement_completed = False

  def _handle_updated_attrs_event(self, **kwargs):
    # https://app.asana.com/0/10235149247655/87787298394920
    self._handle_completed_event(**kwargs)

  def _handle_completed_event(self, **kwargs):
    self.potential_agreement_name = kwargs['potential_agreement_name']
    self.potential_agreement_counterparty = kwargs['potential_agreement_counterparty']
    self.potential_agreement_description = kwargs['potential_agreement_description']
    self.potential_agreement_execution_date = kwargs['potential_agreement_execution_date']
    self.potential_agreement_outcome_date = kwargs['potential_agreement_outcome_date']
    self.potential_agreement_type_id = kwargs['potential_agreement_type_id']
    self.potential_agreement_counterparty = kwargs['potential_agreement_counterparty']
    self.potential_agreement_term_length_time_amount = kwargs['potential_agreement_term_length_time_amount']
    self.potential_agreement_term_length_time_type = kwargs['potential_agreement_term_length_time_type']
    self.potential_agreement_auto_renew = kwargs['potential_agreement_auto_renew']
    self.potential_agreement_outcome_notice_time_amount = kwargs['potential_agreement_outcome_notice_time_amount']
    self.potential_agreement_outcome_notice_time_type = kwargs['potential_agreement_outcome_notice_time_type']
    self.potential_agreement_outcome_notice_date = kwargs['potential_agreement_outcome_notice_date']
    self.potential_agreement_duration_details = kwargs['potential_agreement_duration_details']
    self.potential_agreement_outcome_notice_alert_enabled = kwargs['potential_agreement_outcome_notice_alert_enabled']
    self.potential_agreement_outcome_notice_alert_time_amount = kwargs[
      'potential_agreement_outcome_notice_alert_time_amount']
    self.potential_agreement_outcome_notice_alert_time_type = kwargs[
      'potential_agreement_outcome_notice_alert_time_type']
    self.potential_agreement_outcome_notice_alert_date = kwargs['potential_agreement_outcome_notice_alert_date']
    self.potential_agreement_expiration_alert_enabled = kwargs['potential_agreement_expiration_alert_enabled']
    self.potential_agreement_expiration_alert_time_amount = kwargs['potential_agreement_expiration_alert_time_amount']
    self.potential_agreement_expiration_alert_time_type = kwargs['potential_agreement_expiration_alert_time_type']
    self.potential_agreement_expiration_alert_date = kwargs['potential_agreement_expiration_alert_date']
    self.potential_agreement_completed = True

  def _handle_outcome_notice_alert_sent_event(self, **kwargs):
    self.potential_agreement_outcome_notice_alert_created = True

  def _handle_expiration_alert_sent_event(self, **kwargs):
    self.potential_agreement_expiration_alert_created = True

  def __str__(self):
    return 'PotentialAgreement #' + str(self.potential_agreement_id) + ': ' + self.potential_agreement_name

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)

        for event in self._uncommitted_events:
          Event.objects.create(
            aggregate_name=self.__class__.__name__, aggregate_id=self.potential_agreement_id,
            event_name=event.event_fq_name, event_version=event.version, event_data=event.kwargs
          )

      # don't send events until successful commit
      self.send_events()
    else:
      from src.aggregates.potential_agreement.services import potential_agreement_service

      potential_agreement_service.save_or_update(self)
