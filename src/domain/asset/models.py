from django.db import models

from src.domain.common.models import ReadModel


class AssetLookup(ReadModel):
  name = models.CharField(max_length=2400)
  path = models.CharField(max_length=2400)

  def __str__(self):
    return 'AssetLookup {id}: {name}'.format(id=self.id, name=self.name)
