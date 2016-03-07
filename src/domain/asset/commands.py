from src.libs.common_domain.command_signal import CommandSignal
from src.libs.python_utils.objects.object_utils import initializer


class CreateAssetFromFile():
  command_signal = CommandSignal()

  @initializer
  def __init__(self, destination_path, file):
    pass
