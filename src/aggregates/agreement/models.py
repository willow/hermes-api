from django.db import models, transaction

from src.aggregates.agreement.signals import created
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import Event
from src.libs.python_utils.id.id_utils import generate_id


class Agreement(models.Model, AggregateBase):
  agreement_id = models.CharField(max_length=6, unique=True)
  agreement_name = models.CharField(max_length=2400)

  @classmethod
  def _from_attrs(cls, agreement_name):
    ret_val = cls()

    if not agreement_name:
      raise TypeError("agreement name is required")

    ret_val._raise_event(
      created,
      agreement_id=generate_id(),
      agreement_name=agreement_name,
    )

    return ret_val

  def _handle_created_event(self, **kwargs):
    self.agreement_id = kwargs['agreement_id']
    self.agreement_name = kwargs['agreement_name']

  def __str__(self):
    return 'Agreement #' + str(self.pk) + ': ' + self.agreement_name

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)

        for event in self._uncommitted_events:
          Event.objects.create(name=event.event_fq_name, version=event.version, data=event.kwargs)

        self.send_events()
    else:
      from src.aggregates.agreement.services import agreement_service

      agreement_service.save_or_update(self)
