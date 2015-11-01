from django.apps import AppConfig

class AssetConfig(AppConfig):
  name = 'src.aggregates.asset'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.aggregates.asset.event_handlers
