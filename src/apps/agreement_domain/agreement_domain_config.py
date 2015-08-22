from django.apps import AppConfig


class AgreementDomainConfig(AppConfig):
  name = 'src.apps.agreement_domain'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.apps.agreement_domain.event_handlers
