from django.apps import AppConfig


class ReadModelConfig(AppConfig):
  name = 'src.apps.read_model'

  # noinspection PyUnresolvedReferences
  def ready(self):
    from src.apps.read_model.relational.event_handlers import import_handlers as  import_relation_handlers
    import_relation_handlers()

    from src.apps.read_model.realtime.event_handlers import import_handlers as import_realtime_handlers
    import_realtime_handlers()
