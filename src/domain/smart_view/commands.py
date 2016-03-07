from src.libs.common_domain.command_signal import CommandSignal
from src.libs.python_utils.objects.object_utils import initializer


class CreateSmartView():
  command_signal = CommandSignal()

  @initializer
  def __init__(self, name, query, user_id):
    pass


class UpdateSmartViewAttrs():
  command_signal = CommandSignal()

  @initializer
  def __init__(self, name, query):
    pass
