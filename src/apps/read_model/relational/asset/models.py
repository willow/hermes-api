from django.db import models

from src.apps.read_model.relational.models import ReadModel

class AssetLookup(ReadModel):
  name = models.CharField(max_length=2400)
  path = models.CharField(max_length=2400)

  def __str__(self):
    return 'AssetLookup {id}: {name}'.format(id=self.id, name=self.name)


