from src.libs.common_domain.domain_event import DomainEvent
from src.libs.common_domain.event_signal import EventSignal
from src.libs.python_utils.objects.object_utils import initializer


class PotentialAgreementCreated1(DomainEvent):
  event_func_name = 'created_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self,
               id,
               name,
               counterparty,
               description,
               user_id,
               artifacts,
               execution_date,
               outcome_date,
               agreement_type_id,
               term_length_time_amount,
               term_length_time_type,
               auto_renew,
               outcome_notice_time_amount,
               outcome_notice_time_type,
               outcome_notice_date,
               duration_details,
               outcome_notice_alert_enabled,
               outcome_notice_alert_time_amount,
               outcome_notice_alert_time_type,
               outcome_notice_alert_date,
               expiration_alert_enabled,
               expiration_alert_time_amount,
               expiration_alert_time_type,
               expiration_alert_date,
               system_created_date):
    super().__init__()
