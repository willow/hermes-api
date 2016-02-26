from src.libs.common_domain.command_signal import CommandSignal
from src.libs.python_utils.objects.object_utils import initializer


class CreateAsset():
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, name, nickname, email, picture, meta, system_created_date):
    pass
