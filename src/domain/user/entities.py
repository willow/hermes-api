from src.domain.user.events import UserCreated1, UserSubscribed1
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.payment_utils.services import payment_service
from django.conf import settings


class User(AggregateBase):
  @classmethod
  def from_attrs(cls, id, name, nickname, email, picture, meta):
    ret_val = cls()
    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    if not nickname:
      raise TypeError("nickname is required")

    if not email:
      raise TypeError("email is required")

    if not picture:
      raise TypeError("picture is required")

    auth0_attrs = meta.get('auth0', {})
    auth0_user_id = auth0_attrs.get('user_id')
    if not auth0_user_id:
      raise TypeError("auth0_user_id is required")

    ret_val._raise_event(UserCreated1(id, name, nickname, email, picture, meta))

    return ret_val

  def subscribe(self, payment_token, _payment_service=None):
    if not _payment_service: _payment_service = payment_service

    if self.subscribed:
      raise Exception("{0} already subscribed".format(self))

    plan_name = settings.SUBSCRIPTION_PLAN_NAME
    customer = _payment_service.create_customer(
        self.email,
        plan_name,
        payment_token
    )

    charged_amount = customer['subscriptions']['data'][0]['plan']['amount']

    self._raise_event(UserSubscribed1(plan_name, charged_amount))

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name
    self.nickname = event.nickname
    self.email = event.email
    self.picture = event.picture
    self.meta = event.meta

    self.subscribed = False

  def _handle_subscribed_1_event(self, event):
    self.subscribed = True

  def __str__(self):
    return 'User {id}: {name}'.format(id=self.id, name=self.name)
