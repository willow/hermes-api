from django.apps import AppConfig


class SmartViewConfig(AppConfig):
  name = 'src.aggregates.smart_view'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.aggregates.smart_view.event_handlers
