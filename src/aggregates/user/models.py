from django.db import models, transaction
from jsonfield import JSONField
from src.aggregates.agreement_type.services import agreement_type_service
from src.aggregates.user.managers import UserManager

from src.aggregates.user.signals import created
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import Event


class User(models.Model, AggregateBase):
  objects = UserManager()

  primary_key = models.AutoField(primary_key=True)

  id = models.CharField(max_length=8, unique=True)
  name = models.CharField(max_length=2400)
  nickname = models.CharField(max_length=2400)
  email = models.EmailField(unique=True)
  picture = models.URLField()
  attrs = JSONField()
  system_created_date = models.DateTimeField()

  @classmethod
  def _from_attrs(cls, id, name, nickname, email, picture, attrs, system_created_date):
    ret_val = cls()

    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    if not nickname:
      raise TypeError("nickname is required")

    if not email:
      raise TypeError("email is required")

    if not picture:
      raise TypeError("picture is required")

    auth0_attrs = attrs.get('auth0', {})
    auth0_user_id = auth0_attrs.get('user_id')
    if not auth0_user_id:
      raise TypeError("auth0_user_id is required")

    if not system_created_date:
      raise TypeError("system_created_date is required")

    ret_val._raise_event(
      created,
      id=id,
      name=name,
      nickname=nickname,
      email=email,
      picture=picture,
      attrs=attrs,
      system_created_date=system_created_date
    )

    return ret_val

  def _handle_created_event(self, **kwargs):
    self.id = kwargs['id']
    self.name = kwargs['name']
    self.nickname = kwargs['nickname']
    self.email = kwargs['email']
    self.picture = kwargs['picture']
    self.attrs = kwargs['attrs']
    self.system_created_date = kwargs['system_created_date']

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

    global_agreement_types = list(_agreement_type_service.get_global_agreement_types())
    agreement_types = list(self.user_agreement_types.all())

    ret_val = global_agreement_types + agreement_types

    return ret_val

  def __str__(self):
    return 'User {id}: {name}'.format(id=self.id, name=self.name)

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
      from src.aggregates.user.services import service

      service.save_or_update(self)
