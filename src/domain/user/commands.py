from src.libs.common_domain.command_signal import CommandSignal
from src.libs.python_utils.objects.object_utils import initializer


class CreateUser():
  command_signal = CommandSignal()

  @initializer
  def __init__(self, name, nickname, email, picture, meta):
    pass


class SubscribeUser():
  command_signal = CommandSignal()

  @initializer
  def __init__(self, payment_token):
    pass
