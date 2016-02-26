from django.apps import AppConfig


class UserConfig(AppConfig):
  name = 'src.apps.read_model.user'
  label = 'user_read_model'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.apps.read_model.user.event_handlers
