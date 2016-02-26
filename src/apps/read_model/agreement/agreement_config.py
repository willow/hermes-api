from django.apps import AppConfig


class AgreementConfig(AppConfig):
  name = 'src.aggregates.agreement'
  label = 'agreement_read_model'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.apps.read_model.agreement.event_handlers
