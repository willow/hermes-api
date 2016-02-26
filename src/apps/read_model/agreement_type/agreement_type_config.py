from django.apps import AppConfig


class AgreementTypeConfig(AppConfig):
  name = 'src.apps.read_model.agreement_type'
  label = 'agreement_type_read_model'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.apps.read_model.agreement_type.event_handlers
