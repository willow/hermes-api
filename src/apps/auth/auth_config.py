from django.apps import AppConfig

class AuthConfig(AppConfig):
  name = 'src.apps.auth'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.apps.auth.providers.auth0.event_handlers
