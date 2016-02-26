from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  providing_args=['agreement_type_id', 'agreement_type_name', 'agreement_type_global', 'agreement_type_user',
                  'agreement_type_system_created_date']
)
