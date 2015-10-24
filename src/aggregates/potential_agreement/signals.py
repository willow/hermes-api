from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=['potential_agreement_id', 'potential_agreement_name', 'potential_agreement_artifacts',
                  'potential_agreement_user_id', 'potential_agreement_system_created_date']
)

completed = EventSignal(
  'completed', __name__, 1,
  providing_args=['potential_agreement_id', 'potential_agreement_name', 'potential_agreement_counterparty',
                  'potential_agreement_description',
                  'potential_agreement_execution_date', 'potential_agreement_type',
                  'potential_agreement_term_length_amount', 'potential_agreement_term_length_type',
                  'potential_agreement_auto_renew', 'potential_agreement_renewal_notice_amount',
                  'potential_agreement_renewal_notice_type', 'potential_agreement_durations_details']
)
