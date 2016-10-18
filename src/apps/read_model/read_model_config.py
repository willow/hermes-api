from django.apps import AppConfig


class ReadModelConfig(AppConfig):
  name = 'src.apps.read_model'

  # noinspection PyUnresolvedReferences
  def ready(self):
    from src.apps.read_model.relational.event_handlers import import_handlers as  import_relation_handlers
    import_relation_handlers()

    from src.apps.read_model.key_value.event_handlers import import_handlers as import_kv_handlers
    import_kv_handlers()

    from src.apps.read_model.graph.event_handlers import import_handlers as import_graph_handlers
    import_graph_handlers()
