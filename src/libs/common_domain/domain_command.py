from abc import ABC


class DomainCommand(ABC):
  @property
  def data(self):
    return self.__dict__
