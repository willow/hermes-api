from django.db import models

from src.apps.read_model.relational.models import ReadModel


class UserAgreementType(ReadModel):
  name = models.CharField(max_length=2400)
  user_id = models.CharField(max_length=8)
  system_created_date = models.DateTimeField()

  def __str__(self):
    return 'UserAgreementType {id}: {name}'.format(id=self.id, name=self.name)


class GlobalAgreementType(ReadModel):
  name = models.CharField(max_length=2400)
  system_created_date = models.DateTimeField()

  def __str__(self):
    return 'GlobalAgreementType {id}: {name}'.format(id=self.id, name=self.name)


class AgreementTypeLookup(ReadModel):
  name = models.CharField(max_length=2400)

  def __str__(self):
    return 'AgreementTypeLookup {id}: {name}'.format(id=self.id, name=self.name)
