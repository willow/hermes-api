from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=['potential_agreement_id', 'potential_agreement_name', 'potential_agreement_artifacts',
                  'potential_agreement_user_id', 'potential_agreement_system_created_date']
)
