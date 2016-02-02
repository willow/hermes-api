from django.apps import AppConfig


class AlertConfig(AppConfig):
  name = 'src.aggregates.alert'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.aggregates.alert.event_handlers
