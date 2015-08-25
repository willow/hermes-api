from django.apps import AppConfig


class AgreementCreationConfig(AppConfig):
  name = 'src.apps.agreement_creation'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.apps.agreement_creation.event_handlers
