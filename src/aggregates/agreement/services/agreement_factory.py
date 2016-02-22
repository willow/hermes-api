from django.utils import timezone

from src.libs.python_utils.id.id_utils import generate_id

from src.aggregates.agreement.models import Agreement


def create_agreement(**kwargs):
  # this method should be considered internal and no public api call should be allowed to pass in a uid
  # refer to https://app.asana.com/0/10235149247655/46476660493804
  uid = kwargs['uid']
  system_created_date = timezone.now()

  data = dict({'uid': uid, 'system_created_date': system_created_date}, **kwargs)

  agreement = Agreement._from_attrs(**data)

  return agreement
