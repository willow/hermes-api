from django.db import models, transaction
from jsonfield import JSONField
from src.aggregates.potential_agreement.signals import created, completed
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

  potential_agreement_type = models.PositiveSmallIntegerField(blank=True, null=True)

  potential_agreement_description = models.TextField(blank=True, null=True)

  potential_agreement_execution_date = models.DateTimeField(blank=True, null=True)

  potential_agreement_term_length_amount = models.PositiveSmallIntegerField(blank=True, null=True)
  potential_agreement_term_length_type = models.PositiveSmallIntegerField(blank=True, null=True)

  potential_agreement_auto_renew = models.NullBooleanField(blank=True, null=True)
  potential_agreement_renewal_notice_amount = models.PositiveSmallIntegerField(blank=True, null=True)
  potential_agreement_renewal_notice_type = models.PositiveSmallIntegerField(blank=True, null=True)

  potential_agreement_duration_details = models.TextField(blank=True, null=True)

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
               potential_agreement_execution_date, potential_agreement_type,
               potential_agreement_term_length_amount, potential_agreement_term_length_type,
               potential_agreement_auto_renew, potential_agreement_renewal_notice_amount,
               potential_agreement_renewal_notice_type, potential_agreement_duration_details):

    if not potential_agreement_name:
      raise ValueError("potential_agreement_name is required")

    if not potential_agreement_counterparty:
      raise ValueError("potential_agreement_counterparty is required")

    if not potential_agreement_execution_date:
      raise ValueError("potential_agreement_execution_date is required")

    self._raise_event(completed,
                      potential_agreement_id=self.potential_agreement_id,
                      potential_agreement_name=potential_agreement_name,
                      potential_agreement_counterparty=potential_agreement_counterparty,
                      potential_agreement_description=potential_agreement_description,
                      potential_agreement_execution_date=potential_agreement_execution_date,
                      potential_agreement_type=potential_agreement_type,
                      potential_agreement_term_length_amount=potential_agreement_term_length_amount,
                      potential_agreement_term_length_type=potential_agreement_term_length_type,
                      potential_agreement_auto_renew=potential_agreement_auto_renew,
                      potential_agreement_renewal_notice_amount=potential_agreement_renewal_notice_amount,
                      potential_agreement_renewal_notice_type=potential_agreement_renewal_notice_type,
                      potential_agreement_duration_details=potential_agreement_duration_details)

  def _handle_created_event(self, **kwargs):
    self.potential_agreement_id = kwargs['potential_agreement_id']
    self.potential_agreement_name = kwargs['potential_agreement_name']
    self.potential_agreement_artifacts = kwargs['potential_agreement_artifacts']
    self.potential_agreement_user_id = kwargs['potential_agreement_user_id']
    self.potential_agreement_system_created_date = kwargs['potential_agreement_system_created_date']

  def _handle_completed_event(self, **kwargs):
    self.potential_agreement_name = kwargs['potential_agreement_name']
    self.potential_agreement_counterparty = kwargs['potential_agreement_counterparty']
    self.potential_agreement_description = kwargs['potential_agreement_description']
    self.potential_agreement_execution_date = kwargs['potential_agreement_execution_date']
    self.potential_agreement_type = kwargs['potential_agreement_type']
    self.potential_agreement_term_length_amount = kwargs['potential_agreement_term_length_amount']
    self.potential_agreement_counterparty = kwargs['potential_agreement_counterparty']
    self.potential_agreement_term_length_type = kwargs['potential_agreement_term_length_type']
    self.potential_agreement_auto_renew = kwargs['potential_agreement_auto_renew']
    self.potential_agreement_renewal_notice_amount = kwargs['potential_agreement_renewal_notice_amount']
    self.potential_agreement_renewal_notice_type = kwargs['potential_agreement_renewal_notice_type']
    self.potential_agreement_duration_details = kwargs['potential_agreement_duration_details']

  def __str__(self):
    return 'PotentialAgreement #' + str(self.potential_agreement_id) + ': ' + self.potential_agreement_name

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)

        for event in self._uncommitted_events:
          Event.objects.create(name=event.event_fq_name, version=event.version, data=event.kwargs)

      # don't send events until successful commit
      self.send_events()
    else:
      from src.aggregates.potential_agreement.services import potential_agreement_service

      potential_agreement_service.save_or_update(self)
