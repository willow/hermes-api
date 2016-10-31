from django.contrib.auth.models import PermissionsMixin
from django.db import models

from src.apps.read_model.relational.models import ReadModel
from src.apps.read_model.relational.user.managers import AuthUserManager


class AuthUser(ReadModel, PermissionsMixin):
  # todo this is not really a read model, it's part of the app/domain i'd say.
  objects = AuthUserManager()

  email = models.EmailField(unique=True)

  REQUIRED_FIELDS = ()
  USERNAME_FIELD = 'id'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.is_anonymous = False
    self.is_staff = True

  @property
  def is_active(self):
    # https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#django.contrib.auth.models.CustomUser.is_active
    # this attr is checked by auth frameworks (DRF JWT for example)
    # but considering we're using 3rd party for auth, we probably don't need to store those attrs in this app right now.
    return True

  @property
  def is_authenticated(self):
    # https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser.is_authenticated
    return True

  def __str__(self):
    return 'AuthUser {id}: {email}'.format(id=self.id, email=self.email)
