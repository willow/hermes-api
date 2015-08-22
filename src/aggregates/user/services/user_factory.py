from django.utils import timezone

from src.aggregates.user.models import User


def create_user(user_id, user_name, user_nickname, user_email, user_picture, user_attrs):
  system_created_date = timezone.now()

  user = User._from_attrs(user_id, user_name, user_nickname, user_email, user_picture, user_attrs, system_created_date)

  return user
