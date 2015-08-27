from django.db import models, transaction


class PotentialAgreement(models.Model):
  potential_agreement_id = models.CharField(max_length=6, unique=True)
  potential_agreement_name = models.CharField(max_length=2400)
  system_created_date = models.DateTimeField()

  completed = models.BooleanField()

  def __str__(self):
    return 'PotentialAgreement #' + str(self.potential_agreement_id) + ': ' + self.potential_agreement_name

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)
    else:
      from src.apps.agreement_domain.services import potential_agreement_service

      potential_agreement_service.save_or_update(self)
