from src.libs.common_domain.domain_event import DomainEvent
from src.libs.common_domain.event_signal import EventSignal
from src.libs.datetime_utils.datetime_utils import get_date_from_string
from src.libs.python_utils.objects.object_utils import initializer


class PotentialAgreementCreated1(DomainEvent):
  event_func_name = 'created_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, name, artifact_ids, user_id, system_created_date):
    super().__init__()


class PotentialAgreementCompleted1(DomainEvent):
  event_func_name = 'completed_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self,
               name,
               user_id,
               artifact_ids,
               counterparty,
               description,
               execution_date,
               agreement_type_id,
               term_length_time_amount,
               term_length_time_type,
               auto_renew,
               outcome_notice_time_amount,
               outcome_notice_time_type,
               duration_details,
               outcome_alert_enabled,
               outcome_alert_time_amount,
               outcome_alert_time_type,
               outcome_notice_alert_enabled,
               outcome_notice_alert_time_amount,
               outcome_notice_alert_time_type,
               ):
    super().__init__()
