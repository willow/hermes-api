from django.apps import AppConfig


class RealtimeConfig(AppConfig):
  name = 'src.apps.read_model.realtime'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.apps.read_model.realtime.agreement_type.event_handlers
    import src.apps.read_model.realtime.agreement.event_handlers
    import src.apps.read_model.realtime.counterparty.event_handlers
    import src.apps.read_model.realtime.user.event_handlers
    import src.apps.read_model.realtime.smart_view.event_handlers
