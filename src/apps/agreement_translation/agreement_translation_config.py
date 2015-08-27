from django.apps import AppConfig


class AgreementTranslationConfig(AppConfig):
  name = 'src.apps.agreement_translation'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.apps.agreement_translation.event_handlers
