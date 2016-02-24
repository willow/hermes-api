from src.aggregates.user.services import user_factory
from src.aggregates.user.models import User


def save_or_update(user):
  user.save(internal=True)


def get_user(id):
  return User.objects.get(id=id)


def get_user_from_email(email):
  return User.objects.get(email=email)


def create_user(name, nickname, email, picture, attrs):
  user = user_factory.create_user(name, nickname, email, picture, attrs)
  save_or_update(user)
  return user
