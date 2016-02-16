from django.db import models, transaction

from src.aggregates.agreement_type.signals import created
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import Event


class AgreementType(models.Model, AggregateBase):
  agreement_type_id = models.CharField(max_length=8, unique=True)
  agreement_type_name = models.CharField(max_length=2400)
  agreement_type_global = models.BooleanField()
  agreement_type_user = models.ForeignKey('user.User', 'user_id', blank=True, related_name='user_agreement_types',
                                          null=True)
  agreement_type_system_created_date = models.DateTimeField()

  class Meta:
    unique_together = ("agreement_type_name", "agreement_type_user")

  @classmethod
  def _from_attrs(cls, agreement_type_id, agreement_type_name, agreement_type_global, agreement_type_user_id,
                  agreement_type_system_created_date):
    ret_val = cls()

    if not agreement_type_id:
      raise TypeError("agreement_type_id is required")

    if not agreement_type_name:
      raise TypeError("agreement_type_name is required")

    if agreement_type_global is None:
      raise TypeError("agreement_type_global is required")

    if not agreement_type_system_created_date:
      raise TypeError("agreement_type_system_created_date is required")

    ret_val._raise_event(
      created,
      agreement_type_id=agreement_type_id,
      agreement_type_name=agreement_type_name,
      agreement_type_global=agreement_type_global,
      agreement_type_user_id=agreement_type_user_id,
      agreement_type_system_created_date=agreement_type_system_created_date,
    )

    return ret_val

  def _handle_created_event(self, **kwargs):
    self.agreement_type_id = kwargs['agreement_type_id']
    self.agreement_type_name = kwargs['agreement_type_name']
    self.agreement_type_global = kwargs['agreement_type_global']
    self.agreement_type_user_id = kwargs['agreement_type_user_id']
    self.agreement_type_system_created_date = kwargs['agreement_type_system_created_date']

  def __str__(self):
    return 'Agreement Type#' + self.agreement_type_id + ': ' + self.agreement_type_name

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)

        for event in self._uncommitted_events:
          Event.objects.create(name=event.event_fq_name, version=event.version, data=event.kwargs)

      self.send_events()
    else:
      from src.aggregates.agreement.services import agreement_type_service

      agreement_type_service.save_or_update(self)
