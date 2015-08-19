from django.apps import AppConfig

class AgreementConfig(AppConfig):
  name = 'src.aggregates.agreement'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.aggregates.agreement.event_handlers
