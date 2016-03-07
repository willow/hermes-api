from django.dispatch import receiver
from django.utils import timezone

from src.domain.agreement.commands import CreateAgreementFromPotentialAgreement, UpdateAgreementAttrs, \
  SendAgreementAlerts
from src.domain.agreement.entities import Agreement
from src.libs.common_domain import aggregate_repository


@receiver(CreateAgreementFromPotentialAgreement.command_signal)
def create_agreement(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  system_created_date = timezone.now()
  data = dict({'system_created_date': system_created_date}, **command.__dict__)

  agreement = Agreement.from_attrs(**data)
  _aggregate_repository.save(agreement, -1)


@receiver(UpdateAgreementAttrs.command_signal)
def update_agreement(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  command = kwargs['command']
  id = kwargs['aggregate_id']

  data = command.__dict__

  ag = _aggregate_repository.get(Agreement, id)

  version = ag.version

  ag.update_attrs(**data)

  _aggregate_repository.save(ag, version)


@receiver(SendAgreementAlerts.command_signal)
def send_agreement_alerts(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  id = kwargs['aggregate_id']

  ag = _aggregate_repository.get(Agreement, id)

  version = ag.version

  ag.send_outcome_notice_alert_if_due()
  ag.send_expiration_alert_if_due()

  _aggregate_repository.save(ag, version)
