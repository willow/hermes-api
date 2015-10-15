from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=['potential_agreement_id', 'potential_agreement_name', 'potential_agreement_artifacts',
                  'user_id', 'system_created_date']
)
