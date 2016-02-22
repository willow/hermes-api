from django.db import models, transaction

from src.aggregates.agreement.signals import created
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import Event


class Agreement(models.Model, AggregateBase):
  agreement_id = models.CharField(max_length=8, unique=True)
  agreement_name = models.CharField(max_length=2400)
  agreement_system_created_date = models.DateTimeField()

  @classmethod
  def _from_attrs(cls, agreement_id, agreement_name, agreement_system_created_date):
    ret_val = cls()

    if not agreement_id:
      raise TypeError("agreement_id is required")

    if not agreement_name:
      raise TypeError("agreement_name is required")

    if not agreement_system_created_date:
      raise TypeError("agreement_system_created_date is required")

    ret_val._raise_event(
      created,
      agreement_id=agreement_id,
      agreement_name=agreement_name,
      agreement_system_created_date=agreement_system_created_date,
    )

    return ret_val

  def _handle_created_event(self, **kwargs):
    self.agreement_id = kwargs['agreement_id']
    self.agreement_name = kwargs['agreement_name']
    self.agreement_system_created_date = kwargs['agreement_system_created_date']

  def __str__(self):
    return 'Agreement #' + str(self.agreement_id) + ': ' + self.agreement_name

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)

        for event in self._uncommitted_events:
          Event.objects.create(
            aggregate_name=self.__class__.__name__, aggregate_id=self.agreement_id,
            event_name=event.event_fq_name, event_version=event.version, event_data=event.kwargs
          )

      self.send_events()
    else:
      from src.aggregates.agreement.services import agreement_service

      agreement_service.save_or_update(self)
