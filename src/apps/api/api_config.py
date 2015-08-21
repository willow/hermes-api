from django.apps import AppConfig


class ApiConfig(AppConfig):
  name = 'src.apps.api'

  # noinspection PyUnresolvedReferences
  def ready(self):
    pass
