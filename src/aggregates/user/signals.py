from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=['uid', 'name', 'nickname', 'email', 'picture', 'attrs', 'system_created_date']
)
