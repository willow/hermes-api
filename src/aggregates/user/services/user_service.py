from src.aggregates.user.services import user_factory
from src.aggregates.user.models import User


def save_or_update(user):
  user.save(internal=True)


def get_user(user_id):
  return User.objects.get(user_id=user_id)


def get_user_from_email(user_email):
  return User.objects.get(user_email=user_email)


# this method should be considered internal and no public api call should be allowed to pass in the user_id
# refer to https://app.asana.com/0/10235149247655/46476660493804
def create_user(user_id, user_name, user_nickname, user_email, user_picture, user_attrs):
  user = user_factory.create_user(user_id, user_name, user_nickname, user_email, user_picture, user_attrs)
  save_or_update(user)
  return user
