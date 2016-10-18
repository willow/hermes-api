from django.db import models

from src.apps.read_model.relational.models import ReadModel


class AgreementSearch(ReadModel):
  name = models.CharField(max_length=2400)
  user_id = models.CharField(max_length=8)
  counterparty = models.CharField(max_length=2400, blank=True, null=True)
  agreement_type_id = models.CharField(max_length=8, blank=True, null=True)


def __str__(self):
  return 'AgreementSearch {id}: {name}'.format(id=self.id, name=self.name)


class AgreementAlert(ReadModel):
  outcome_alert_date = models.DateTimeField(blank=True, null=True)
  outcome_alert_enabled = models.BooleanField()
  outcome_alert_created = models.BooleanField()
  outcome_notice_alert_date = models.DateTimeField(blank=True, null=True)
  outcome_notice_alert_enabled = models.BooleanField()
  outcome_notice_alert_created = models.BooleanField()

  def __str__(self):
    return 'AgreementAlert {id}: {name}'.format(id=self.id)
