from django.db import models

from src.apps.read_model.relational.models import ReadModel
from src.apps.read_model.relational.user.managers import AuthUserManager


class AuthUser(ReadModel):
  objects = AuthUserManager()

  email = models.EmailField(unique=True)
  system_created_date = models.DateTimeField()

  REQUIRED_FIELDS = ()
  USERNAME_FIELD = 'id'

  @property
  def is_active(self):
    # https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#django.contrib.auth.models.CustomUser.is_active
    # this attr is checked by auth frameworks (DRF JWT for example)
    # but considering we're using 3rd party for auth, we probably don't need to store those attrs in this app right now.
    return True

  def is_authenticated(self):
    # https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser.is_authenticated
    return True

  def __str__(self):
    return 'AuthUser {id}: {name}'.format(id=self.id, name=self.name)
