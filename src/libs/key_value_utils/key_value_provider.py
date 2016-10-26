from django_redis import get_redis_connection


def get_key_value_client():
  con = get_redis_connection("default")
  return con
