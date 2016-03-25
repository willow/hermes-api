from src.libs.common_domain.command_signal import CommandSignal
from src.libs.python_utils.objects.object_utils import initializer


class CreateAgreementFromPotentialAgreement():
  command_signal = CommandSignal()

  @initializer
  def __init__(self,
               id,
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
    pass


class UpdateAgreementAttrs():
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


class SendAgreementAlerts():
  command_signal = CommandSignal()


class DeleteAgreement():
  command_signal = CommandSignal()


class DeleteArtifact():
  command_signal = CommandSignal()

  @initializer
  def __init__(self, artifact_id):
    pass


class CreateArtifact():
  command_signal = CommandSignal()

  @initializer
  def __init__(self, artifact_id):
    pass
