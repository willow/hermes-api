from src.aggregates.user.models import User


def create_user(user_name, user_nickname, user_email, user_picture, user_attrs):
  user = User._from_attrs(user_name, user_nickname, user_email, user_picture, user_attrs)

  return user
