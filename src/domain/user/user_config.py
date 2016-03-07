from django.apps import AppConfig


class UserConfig(AppConfig):
  name = 'src.domain.user'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.domain.user.command_handlers
    import src.domain.user.event_handlers
