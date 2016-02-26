from django.db import models


class ReadModel(models.Model):
  primary_key = models.AutoField(primary_key=True)
  id = models.CharField(max_length=8, unique=True)

  class Meta:
    abstract = True


class VersionedReadModel(ReadModel):
  version = models.PositiveSmallIntegerField(blank=True, null=True)

  class Meta:
    abstract = True
