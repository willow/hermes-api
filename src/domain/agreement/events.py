from src.libs.common_domain.domain_event import DomainEvent
from src.libs.common_domain.event_signal import EventSignal
from src.libs.python_utils.objects.object_utils import initializer


class AgreementCreated1(DomainEvent):
  event_func_name = 'created_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self,
               id,
               name,
               counterparty,
               description,
               user_id,
               artifact_ids,
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
               outcome_notice_alert_created,
               outcome_notice_alert_expired,
               expiration_alert_enabled,
               expiration_alert_time_amount,
               expiration_alert_time_type,
               expiration_alert_date,
               expiration_alert_created,
               expiration_alert_expired,
               system_created_date):
    super().__init__()


class AgreementAttrsUpdated1(DomainEvent):
  event_func_name = 'attrs_updated_1'
  event_signal = EventSignal()

  # https://app.asana.com/0/10235149247655/100075573324021
  @initializer
  def __init__(self,
               name,
               counterparty,
               description,
               user_id,
               artifact_ids,
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
               outcome_notice_alert_created,
               outcome_notice_alert_expired,
               expiration_alert_enabled,
               expiration_alert_time_amount,
               expiration_alert_time_type,
               expiration_alert_date,
               expiration_alert_created,
               expiration_alert_expired,
               ):
    super().__init__()


class AgreementExpirationAlertSent1(DomainEvent):
  event_func_name = 'expiration_alert_sent_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, name, user_id, outcome_date, outcome_notice_alert_created, outcome_notice_date,
               expiration_alert_created, ):
    super().__init__()


class AgreementOutcomeNoticeAlertSent1(DomainEvent):
  event_func_name = 'outcome_notice_alert_sent_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, name, user_id, outcome_date, outcome_notice_alert_created,
               outcome_notice_date, expiration_alert_created, ):
    super().__init__()


class AgreementDeleted1(DomainEvent):
  event_func_name = 'deleted_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, user_id, ):
    super().__init__()


class ArtifactDeleted1(DomainEvent):
  event_func_name = 'artifact_deleted_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, artifact_id):
    super().__init__()
