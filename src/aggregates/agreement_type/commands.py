from src.libs.common_domain.command_signal import CommandSignal


class CreateAgreementType():
  command_signal = CommandSignal()

  def __init__(self, name, nickname, email, picture, meta):
    self.name = name
    self.nickname = nickname
    self.email = email
    self.picture = picture
    self.meta = meta
