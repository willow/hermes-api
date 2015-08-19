from django.apps import AppConfig


class ReadModelConfig(AppConfig):
  name = 'src.apps.read_model'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.apps.read_model.models.user.event_handlers
