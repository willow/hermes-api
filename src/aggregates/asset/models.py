from django.db import models, transaction
from django.conf import settings

from src.aggregates.asset.signals import created
from src.libs.common_domain.models import Event, AggregateModelBase

constants = settings.CONSTANTS
assets_root = constants.ASSETS_ROOT


class Asset(AggregateModelBase):
  path = models.CharField(max_length=2400)
  content_type = models.CharField(max_length=2400)
  original_name = models.CharField(max_length=2400)
  system_created_date = models.DateTimeField()

  @classmethod
  def _from_attrs(cls, id, path, content_type, original_name, system_created_date):
    ret_val = cls()

    if not id:
      raise TypeError("id is required")

    if not path:
      raise TypeError("path is required")

    if not content_type:
      raise TypeError("content_type is required")

    if not original_name:
      raise TypeError("original_name is required")

    if not path:
      raise TypeError("path is required")

    ret_val._raise_event(
      created,
      id=id, path=path, content_type=content_type,
      original_name=original_name, system_created_date=system_created_date
    )

    return ret_val

  @property
  def signed_path(self, _asset_service=None):
    # this model is assuming the responsibility of figuring out the signed path but handing off that responsibility
    # to the asset service, using the double dispatch pattern.
    # https://lostechies.com/jimmybogard/2010/03/30/strengthening-your-domain-the-double-dispatch-pattern/
    if not _asset_service:
      from src.aggregates.asset import services

      _asset_service = services

    ret_val = _asset_service.get_signed_asset_path(self.path)

    return ret_val

  def _handle_created_event(self, **kwargs):
    self.id = kwargs['id']
    self.path = kwargs['path']
    self.content_type = kwargs['content_type']
    self.original_name = kwargs['original_name']
    self.system_created_date = kwargs['system_created_date']

  def __str__(self):
    return 'Asset {id}: {name}'.format(id=self.id, name=self.name)

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
      from src.aggregates.asset.services import service

      service.save_or_update(self)
