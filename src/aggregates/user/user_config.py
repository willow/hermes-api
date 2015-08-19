from django.apps import AppConfig

class UserConfig(AppConfig):
  name = 'src.aggregates.user'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.aggregates.user.event_handlers
