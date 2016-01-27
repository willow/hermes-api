from jsonfield import JSONField

from django.db import models, transaction

from src.aggregates.smart_view.signals import created, updated_attrs
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import Event


class SmartView(models.Model, AggregateBase):
  smart_view_id = models.CharField(max_length=8, unique=True)
  smart_view_name = models.CharField(max_length=2400)
  smart_view_query = JSONField()
  smart_view_user = models.ForeignKey('user.User', 'user_id', related_name='smart_views')
  smart_view_system_created_date = models.DateTimeField()

  @classmethod
  def _from_attrs(cls, smart_view_id, smart_view_name, smart_view_query, smart_view_user_id,
                  smart_view_system_created_date):
    ret_val = cls()

    if not smart_view_id:
      raise TypeError("smart_view_id is required")

    if not smart_view_name:
      raise TypeError("smart_view_name is required")

    if not smart_view_query:
      raise TypeError("smart_view_query is required")

    if not smart_view_user_id:
      raise TypeError("smart_view_user_id is required")

    ret_val._raise_event(
      created,
      smart_view_id=smart_view_id,
      smart_view_name=smart_view_name,
      smart_view_query=smart_view_query,
      smart_view_user_id=smart_view_user_id,
      smart_view_system_created_date=smart_view_system_created_date
    )

    return ret_val

  def update_attrs(self, smart_view_name, smart_view_query):
    if not smart_view_name:
      raise TypeError("smart_view_name is required")

    if not smart_view_query:
      raise TypeError("smart_view_query is required")

    self._raise_event(
      updated_attrs,
      smart_view_id=self.smart_view_id,
      smart_view_name=smart_view_name,
      smart_view_query=smart_view_query
    )

  def _handle_created_event(self, **kwargs):
    self.smart_view_id = kwargs['smart_view_id']
    self.smart_view_name = kwargs['smart_view_name']
    self.smart_view_query = kwargs['smart_view_query']
    self.smart_view_user_id = kwargs['smart_view_user_id']
    self.smart_view_system_created_date = kwargs['smart_view_system_created_date']

  def _handle_updated_attrs_event(self, **kwargs):
    self.smart_view_name = kwargs['smart_view_name']
    self.smart_view_query = kwargs['smart_view_query']

  def __str__(self):
    return 'SmartView {id}: {name}'.format(id=self.smart_view_id, name=self.smart_view_name)

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)

        for event in self._uncommitted_events:
          Event.objects.create(name=event.event_fq_name, version=event.version, data=event.kwargs)

      self.send_events()
    else:
      from src.aggregates.smart_view.services import smart_view_service

      smart_view_service.save_or_update(self)
