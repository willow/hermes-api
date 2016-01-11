from django.db import models, transaction
from jsonfield import JSONField
from src.aggregates.agreement_type.services import agreement_type_service
from src.aggregates.user.managers import UserManager

from src.aggregates.user.signals import created
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import Event


class User(models.Model, AggregateBase):
  objects = UserManager()

  user_id = models.CharField(max_length=8, unique=True)
  user_name = models.CharField(max_length=2400)
  user_nickname = models.CharField(max_length=2400)
  user_email = models.EmailField(unique=True)
  user_picture = models.URLField()
  user_attrs = JSONField()
  user_system_created_date = models.DateTimeField()

  @classmethod
  def _from_attrs(cls, user_id, user_name, user_nickname, user_email, user_picture, user_attrs,
                  user_system_created_date):
    ret_val = cls()

    if not user_id:
      raise TypeError("user_id is required")

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

    if not user_system_created_date:
      raise TypeError("user_system_created_date is required")

    ret_val._raise_event(
      created,
      user_id=user_id,
      user_name=user_name,
      user_nickname=user_nickname,
      user_email=user_email,
      user_picture=user_picture,
      user_attrs=user_attrs,
      user_system_created_date=user_system_created_date
    )

    return ret_val

  def _handle_created_event(self, **kwargs):
    self.user_id = kwargs['user_id']
    self.user_name = kwargs['user_name']
    self.user_nickname = kwargs['user_nickname']
    self.user_email = kwargs['user_email']
    self.user_picture = kwargs['user_picture']
    self.user_attrs = kwargs['user_attrs']
    self.user_system_created_date = kwargs['user_system_created_date']

  @property
  def is_active(self):
    # https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#django.contrib.auth.models.CustomUser.is_active
    # this attr is checked by auth frameworks (DRF JWT for example)
    # but considering we're using 3rd party for auth, we probably don't need to store those attrs in this app right now.
    return True

  def is_authenticated(self):
    # https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser.is_authenticated
    return True

  @property
  def agreement_types(self, _agreement_type_service=None):

    if not _agreement_type_service: _agreement_type_service = agreement_type_service
    ret_val = list(_agreement_type_service.get_global_agreement_types())

    return ret_val

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
