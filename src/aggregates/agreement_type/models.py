from django.db import models, transaction

from src.aggregates.agreement_type.signals import created
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import Event


class AgreementType(models.Model, AggregateBase):
  primary_key = models.AutoField(primary_key=True)

  id = models.CharField(max_length=8, unique=True)
  name = models.CharField(max_length=2400)
  is_global = models.BooleanField()
  user = models.ForeignKey('user.User', 'id', related_name='user_agreement_types', blank=True, null=True)
  system_created_date = models.DateTimeField()

  class Meta:
    unique_together = ("name", "user")

  @classmethod
  def _from_attrs(cls, id, name, is_global, user_id, system_created_date):
    ret_val = cls()

    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    if is_global is None:
      raise TypeError("is_global is required")

    if not system_created_date:
      raise TypeError("system_created_date is required")

    if not is_global and not user_id:
      raise TypeError("a user is required if the agreement type is not global.")

    ret_val._raise_event(
      created,
      id=id,
      name=name,
      is_global=is_global,
      user_id=user_id,
      system_created_date=system_created_date,
    )

    return ret_val

  def _handle_created_event(self, **kwargs):
    self.id = kwargs['id']
    self.name = kwargs['name']
    self.is_global = kwargs['is_global']
    self.user_id = kwargs['user_id']
    self.system_created_date = kwargs['system_created_date']

  def __str__(self):
    return 'Agreement Type#' + self.id + ': ' + self.name

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)

        for event in self._uncommitted_events:
          Event.objects.create(
            aggregate_name=self.__class__.__name__, aggregate_id=self.id,
            event_name=event.event_fq_name, event_version=event.version, event_data=event.kwargs
          )

      self.send_events()
    else:
      from src.aggregates.agreement.services import service

      service.save_or_update(self)
