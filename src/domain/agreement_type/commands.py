from src.libs.common_domain.command_signal import CommandSignal
from src.libs.common_domain.domain_command import DomainCommand
from src.libs.python_utils.objects.object_utils import initializer


class CreateAgreementType(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, name, is_global, user_id):
    pass
