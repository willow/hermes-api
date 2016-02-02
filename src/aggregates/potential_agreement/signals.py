from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=['potential_agreement_id', 'potential_agreement_name', 'potential_agreement_artifacts',
                  'potential_agreement_user_id', 'potential_agreement_system_created_date']
)

updated_providing_args = ['potential_agreement_id',
                          'potential_agreement_name',
                          'potential_agreement_counterparty',
                          'potential_agreement_description',
                          'potential_agreement_execution_date',
                          'potential_agreement_type_id',
                          'potential_agreement_term_length_time_amount',
                          'potential_agreement_term_length_time_type',
                          'potential_agreement_auto_renew',
                          'potential_agreement_outcome_notice_time_amount',
                          'potential_agreement_outcome_notice_time_type',
                          'potential_agreement_durations_details']

completed = EventSignal(
  'completed', __name__, 1,
  updated_providing_args
)

updated_attrs = EventSignal(
  'updated_attrs', __name__, 1,
  updated_providing_args
)

expiration_alert_sent = EventSignal(
  'expiration_alert_sent', __name__, 1, ['potential_agreement_id', ]
)

outcome_notice_alert_sent = EventSignal(
  'outcome_notice_alert_sent', __name__, 1, ['potential_agreement_id', ]
)
