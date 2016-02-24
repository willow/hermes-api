from django.utils import timezone

from src.aggregates.user.models import User
from src.libs.python_utils.id.id_utils import generate_id


def create_user(name, nickname, email, picture, attrs):
  user_id = generate_id()
  system_created_date = timezone.now()

  user = User._from_attrs(user_id, name, nickname, email, picture, attrs, system_created_date)

  return user
