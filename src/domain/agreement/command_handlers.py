from django.dispatch import receiver
from django.utils import timezone

from src.domain.agreement.commands import CreateAgreementFromPotentialAgreement, UpdateAgreementAttrs, \
  SendAgreementAlerts, DeleteAgreement, DeleteArtifact, CreateArtifact
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

  ag.send_outcome_alert_if_due()
  ag.send_outcome_notice_alert_if_due()

  _aggregate_repository.save(ag, version)


@receiver(DeleteAgreement.command_signal)
def delete_agreement(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  id = kwargs['aggregate_id']

  ag = _aggregate_repository.get(Agreement, id)

  version = ag.version

  ag.mark_deleted()

  _aggregate_repository.save(ag, version)


@receiver(DeleteArtifact.command_signal)
def delete_artifact(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  id = kwargs['aggregate_id']

  command = kwargs['command']

  ag = _aggregate_repository.get(Agreement, id)

  version = ag.version

  ag.delete_artifact(command.artifact_id)

  _aggregate_repository.save(ag, version)


@receiver(CreateArtifact.command_signal)
def add_artifact(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  id = kwargs['aggregate_id']

  command = kwargs['command']

  ag = _aggregate_repository.get(Agreement, id)

  version = ag.version

  ag.create_artifact(command.artifact_id)

  _aggregate_repository.save(ag, version)
