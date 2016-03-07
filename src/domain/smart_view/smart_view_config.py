from django.apps import AppConfig


class SmartViewConfig(AppConfig):
  name = 'src.domain.smart_view'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.domain.smart_view.command_handlers
    import src.domain.smart_view.event_handlers
