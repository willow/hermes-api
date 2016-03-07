from django.apps import AppConfig


class PotentialAgreementConfig(AppConfig):
  name = 'src.domain.potential_agreement'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.domain.potential_agreement.command_handlers
    import src.domain.potential_agreement.event_handlers
