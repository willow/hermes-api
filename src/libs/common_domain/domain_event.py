from abc import ABC


class DomainEvent(ABC):
  @property
  def data(self):
    return self.__dict__
