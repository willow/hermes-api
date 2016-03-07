from django.apps import AppConfig

class AssetConfig(AppConfig):
  name = 'src.domain.asset'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.domain.asset.command_handlers
    import src.domain.asset.event_handlers
