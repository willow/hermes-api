from django.utils import timezone

from src.aggregates.agreement.models import Agreement


def create_agreement(**kwargs):
  # this method should be considered internal and no public api call should be allowed to pass in a id
  # refer to https://app.asana.com/0/10235149247655/46476660493804
  id = kwargs['id']
  system_created_date = timezone.now()

  data = dict({'id': id, 'system_created_date': system_created_date}, **kwargs)

  agreement = Agreement._from_attrs(**data)

  return agreement
