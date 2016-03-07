from django.apps import AppConfig

class AgreementTypeConfig(AppConfig):
  name = 'src.domain.agreement_type'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.domain.agreement_type.command_handlers
    import src.domain.agreement_type.event_handlers
