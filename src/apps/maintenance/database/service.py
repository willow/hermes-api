from django.contrib.contenttypes.models import ContentType

from src.libs.key_value_utils.key_value_provider import get_key_value_client


def clear_read_model():
  kdb = get_key_value_client()
  read_model_keys = kdb.keys('read_model:*')
  for r in read_model_keys:
    kdb.delete(r)

  read_model_types = ContentType.objects.filter(app_label='read_model')
  for read_model_type in read_model_types:
    read_model_type.model_class().objects.all().delete()


def clear_rq_jobs():
  kdb = get_key_value_client()
  read_model_keys = kdb.keys('rq:*')
  for r in read_model_keys:
    kdb.delete(r)
