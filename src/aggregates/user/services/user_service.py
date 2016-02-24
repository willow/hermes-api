from src.aggregates.user.services import user_factory
from src.aggregates.user.models import User


def save_or_update(user):
  user.save(internal=True)


def get_user(id):
  return User.objects.get(id=id)


def get_user_from_email(email):
  return User.objects.get(email=email)


# this method should be considered internal and no public api call should be allowed to pass in the user_id
# refer to https://app.asana.com/0/10235149247655/46476660493804
def create_user(id, name, nickname, email, picture, attrs):
  user = user_factory.create_user(id, name, nickname, email, picture, attrs)
  save_or_update(user)
  return user
