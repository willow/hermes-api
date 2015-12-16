from django.apps import AppConfig

class AgreementTypeConfig(AppConfig):
  name = 'src.aggregates.agreement_type'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.aggregates.agreement_type.event_handlers
