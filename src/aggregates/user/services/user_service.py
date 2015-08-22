from src.aggregates.user import factories
from src.aggregates.user.models import User


def save_or_update(user):
  user.save(internal=True)


def get_user(user_id):
  return User.objects.get(user_id=user_id)


def get_user_from_email(user_email):
  return User.objects.get(user_email=user_email)


def create_user(user_name, user_nickname, user_email, user_picture, user_attrs):
  user = factories.create_user(user_name, user_nickname, user_email, user_picture, user_attrs)
  save_or_update(user)
  return user
