from django.apps import AppConfig


class AgreementConfig(AppConfig):
  name = 'src.domain.agreement'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.domain.agreement.command_handlers
    import src.domain.agreement.event_handlers
