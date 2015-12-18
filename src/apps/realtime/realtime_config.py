from django.apps import AppConfig


class RealtimeConfig(AppConfig):
  name = 'src.apps.realtime'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.apps.realtime.agreement_type.event_handlers
    import src.apps.realtime.agreement.event_handlers
    import src.apps.realtime.user.event_handlers
