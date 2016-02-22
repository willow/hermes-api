from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=['agreement_id', 'agreement_name', 'agreement_system_created_date']
)

from src.libs.common_domain.event_signal import EventSignal

updated_providing_args = ['uid',
                          'name',
                          'counterparty',
                          'description',
                          'execution_date',
                          'type_id',
                          'term_length_time_amount',
                          'term_length_time_type',
                          'auto_renew',
                          'outcome_notice_time_amount',
                          'outcome_notice_time_type',
                          'durations_details']

updated_attrs = EventSignal(
  'updated_attrs', __name__, 1,
  updated_providing_args
)

expiration_alert_sent = EventSignal(
  'expiration_alert_sent', __name__, 1, ['id', ]
)

outcome_notice_alert_sent = EventSignal(
  'outcome_notice_alert_sent', __name__, 1, ['id', ]
)
