from django.apps import AppConfig

class SearchConfig(AppConfig):
  name = 'src.aggregates.search'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.aggregates.search.event_handlers
