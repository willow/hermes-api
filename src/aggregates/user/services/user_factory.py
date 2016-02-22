from django.utils import timezone

from src.aggregates.user.models import User


def create_user(id, name, nickname, email, picture, attrs):
  system_created_date = timezone.now()

  user = User._from_attrs(id, name, nickname, email, picture, attrs, system_created_date)

  return user
