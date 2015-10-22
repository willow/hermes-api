from django.db import models, transaction
from jsonfield import JSONField
from src.aggregates.potential_agreement.signals import created
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import Event
from simplejson.encoder import JSONEncoder


class PotentialAgreement(models.Model, AggregateBase):
  potential_agreement_id = models.CharField(max_length=8, unique=True)
  potential_agreement_name = models.CharField(max_length=2400)
  potential_agreement_artifacts = JSONField(default=list,
                                            dump_kwargs={'cls': JSONEncoder})  # simplejson encodes namedtuples
  potential_agreement_user = models.ForeignKey('user.User', 'user_id', related_name='potential_agreements')
  potential_agreement_system_created_date = models.DateTimeField()

  @classmethod
  def _from_attrs(cls, potential_agreement_id, potential_agreement_name, potential_agreement_artifacts,
                  potential_agreement_user_id, potential_agreement_system_created_date):
    ret_val = cls()

    if not potential_agreement_id:
      raise TypeError("potential_agreement_id is required")

    if not potential_agreement_name:
      raise TypeError("potential_agreement_name is required")

    if not potential_agreement_artifacts:
      raise TypeError("potential_agreement_artifacts is required")

    if not potential_agreement_user_id:
      raise TypeError("potential_agreement_user_id is required")

    if not potential_agreement_system_created_date:
      raise TypeError("potential_agreement_system_created_date is required")

    ret_val._raise_event(
      created,
      potential_agreement_id=potential_agreement_id,
      potential_agreement_name=potential_agreement_name,
      potential_agreement_artifacts=potential_agreement_artifacts,
      potential_agreement_user_id=potential_agreement_user_id,
      potential_agreement_system_created_date=potential_agreement_system_created_date,
    )

    return ret_val

  def _handle_created_event(self, **kwargs):
    self.potential_agreement_id = kwargs['potential_agreement_id']
    self.potential_agreement_name = kwargs['potential_agreement_name']
    self.potential_agreement_artifacts = kwargs['potential_agreement_artifacts']
    self.potential_agreement_user_id = kwargs['potential_agreement_user_id']
    self.potential_agreement_system_created_date = kwargs['potential_agreement_system_created_date']

  def __str__(self):
    return 'PotentialAgreement #' + str(self.potential_agreement_id) + ': ' + self.potential_agreement_name

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)

        for event in self._uncommitted_events:
          Event.objects.create(name=event.event_fq_name, version=event.version, data=event.kwargs)

        self.send_events()
    else:
      from src.aggregates.potential_agreement.services import potential_agreement_service

      potential_agreement_service.save_or_update(self)
