from src.domain.agreement_type.events import AgreementTypeCreated1

from src.libs.common_domain.aggregate_base import AggregateBase


class AgreementType(AggregateBase):
  @classmethod
  def from_attrs(cls, id, name, is_global, user_id, system_created_date):
    ret_val = cls()
    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    if is_global is None:
      raise TypeError("is_global is required")

    if not system_created_date:
      raise TypeError("system_created_date is required")

    if not is_global and not user_id:
      raise TypeError("a user is required if the agreement type is not global.")

    ret_val._raise_event(AgreementTypeCreated1(id, name, is_global, user_id, system_created_date))

    return ret_val

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name

  def __str__(self):
    return 'AgreementType {id}: {name}'.format(id=self.id, name=self.name)
