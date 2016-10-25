from abc import ABC, abstractmethod
from src.libs.datetime_utils.datetime_utils import get_date_from_string


def normalize(k, v):
  value = v

  if v and k.endswith('_date'):
    value = get_date_from_string(v)

  return k, value


class DomainEvent(ABC):
  @property
  def data(self):
    return self.__dict__

  @classmethod
  def hydrate(cls, **kwargs):
    hydrated_data = dict([normalize(k, v) for k, v in kwargs.items()])
    return cls(**hydrated_data)
