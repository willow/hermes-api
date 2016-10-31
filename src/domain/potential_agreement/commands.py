from src.libs.common_domain.command_signal import CommandSignal
from src.libs.common_domain.domain_command import DomainCommand
from src.libs.python_utils.objects.object_utils import initializer


class CreatePotentialAgreement(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, name, artifact_ids, user_id):
    pass


class CompletePotentialAgreement(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self,
               name,
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
    pass
