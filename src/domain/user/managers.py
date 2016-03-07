from django.db import models


class AuthUserManager(models.Manager):
  def get_by_natural_key(self, user_id):
    return self.get(id=user_id)
