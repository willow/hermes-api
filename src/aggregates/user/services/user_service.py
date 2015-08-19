from src.aggregates.user import factories


def save_or_update(user):
  user.save(internal=True)


def create_user(user_name, user_nickname, user_email, user_picture, user_attrs):
  user = factories.create_user(user_name, user_nickname, user_email, user_picture, user_attrs)
  save_or_update(user)
  return user
