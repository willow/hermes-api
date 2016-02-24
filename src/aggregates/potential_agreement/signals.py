from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=['id', 'name', 'artifacts',
                  'user_id', 'system_created_date']
)
completed = EventSignal(
  'completed', __name__, 1,
)
