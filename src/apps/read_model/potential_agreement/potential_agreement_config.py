from django.apps import AppConfig


class PotentialAgreementConfig(AppConfig):
  name = 'src.aggregates.potential_agreement'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.aggregates.potential_agreement.event_handlers
