from src.apps.read_model.relational.user.models import AuthUser


def save_auth_user(id, email):
  user, _ = AuthUser.objects.update_or_create(
      id=id, email=email
  )
  return user
