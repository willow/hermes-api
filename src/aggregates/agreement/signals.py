from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=['agreement_id', 'agreement_name', 'agreement_system_created_date']
)
