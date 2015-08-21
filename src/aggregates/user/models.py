from django.db import models, transaction
from django.utils import timezone
from jsonfield import JSONField

from src.aggregates.user.signals import created
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import Event
from src.libs.python_utils.id.id_utils import generate_id


class User(models.Model, AggregateBase):
  user_id = models.CharField(max_length=6, unique=True)
  user_name = models.CharField(max_length=2400)
  user_nickname = models.CharField(max_length=2400)
  user_email = models.EmailField(unique=True)
  user_picture = models.URLField()
  user_attrs = JSONField()
  system_created_date = models.DateTimeField()

  @classmethod
  def _from_attrs(cls, user_name, user_nickname, user_email, user_picture, user_attrs):
    ret_val = cls()

    if not user_name:
      raise TypeError("user_name is required")

    if not user_nickname:
      raise TypeError("user_nickname is required")

    if not user_email:
      raise TypeError("user_email is required")

    if not user_picture:
      raise TypeError("user_picture is required")

    auth0_attrs = user_attrs.get('auth0', {})
    auth0_user_id = auth0_attrs.get('user_id')
    if not auth0_user_id:
      raise TypeError("auth0_user_id is required")

    ret_val._raise_event(
      created,
      user_id=generate_id(),
      user_name=user_name,
      user_nickname=user_nickname,
      user_email=user_email,
      user_picture=user_picture,
      user_attrs=user_attrs,
      system_created_date=timezone.now()
    )

    return ret_val

  def _handle_created_event(self, **kwargs):
    self.user_id = kwargs['user_id']
    self.user_name = kwargs['user_name']
    self.user_nickname = kwargs['user_nickname']
    self.user_email = kwargs['user_email']
    self.user_picture = kwargs['user_picture']
    self.user_attrs = kwargs['user_attrs']
    self.system_created_date = kwargs['system_created_date']

  def __str__(self):
    return 'User {uid}: {name}'.format(uid=self.user_id, name=self.user_name)

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)

        for event in self._uncommitted_events:
          Event.objects.create(name=event.event_fq_name, version=event.version, data=event.kwargs)

        self.send_events()
    else:
      from src.aggregates.user.services import user_service

      user_service.save_or_update(self)
