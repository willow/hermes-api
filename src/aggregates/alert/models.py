from jsonfield import JSONField

from django.db import models, transaction

from src.aggregates.alert.signals import created, updated_attrs
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import Event


class Alert(models.Model, AggregateBase):
  alert_id = models.CharField(max_length=8, unique=True)
  alert_name = models.CharField(max_length=2400)
  alert_query = JSONField()
  alert_user = models.ForeignKey('user.User', 'user_id', related_name='alerts')
  alert_system_created_date = models.DateTimeField()

  @classmethod
  def _from_attrs(cls, alert_id, alert_name, alert_query, alert_user_id,
                  alert_system_created_date):
    ret_val = cls()

    if not alert_id:
      raise TypeError("alert_id is required")

    if not alert_name:
      raise TypeError("alert_name is required")

    if not alert_query:
      raise TypeError("alert_query is required")

    if not alert_user_id:
      raise TypeError("alert_user_id is required")

    ret_val._raise_event(
      created,
      alert_id=alert_id,
      alert_name=alert_name,
      alert_query=alert_query,
      alert_user_id=alert_user_id,
      alert_system_created_date=alert_system_created_date
    )

    return ret_val

  def update_attrs(self, alert_name, alert_query):
    if not alert_name:
      raise TypeError("alert_name is required")

    if not alert_query:
      raise TypeError("alert_query is required")

    self._raise_event(
      updated_attrs,
      alert_id=self.alert_id,
      alert_name=alert_name,
      alert_query=alert_query
    )

  def _handle_created_event(self, **kwargs):
    self.alert_id = kwargs['alert_id']
    self.alert_name = kwargs['alert_name']
    self.alert_query = kwargs['alert_query']
    self.alert_user_id = kwargs['alert_user_id']
    self.alert_system_created_date = kwargs['alert_system_created_date']

  def _handle_updated_attrs_event(self, **kwargs):
    self.alert_name = kwargs['alert_name']
    self.alert_query = kwargs['alert_query']

  def __str__(self):
    return 'SmartView {id}: {name}'.format(id=self.alert_id, name=self.alert_name)

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)

        for event in self._uncommitted_events:
          Event.objects.create(name=event.event_fq_name, version=event.version, data=event.kwargs)

      self.send_events()
    else:
      from src.aggregates.alert.services import alert_service

      alert_service.save_or_update(self)
