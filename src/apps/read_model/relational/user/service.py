from src.apps.read_model.relational.user.models import AuthUser


def save_auth_user(id, email, system_created_date):
  user, _ = AuthUser.objects.update_or_create(
      id=id, email=email, system_created_date=system_created_date
  )
  return user
