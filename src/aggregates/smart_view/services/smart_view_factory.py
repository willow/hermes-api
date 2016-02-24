from django.utils import timezone
from src.aggregates.smart_view.models import SmartView

from src.libs.python_utils.id.id_utils import generate_id


def create_smart_view(name, query, user_id):
  smart_view_id = generate_id()
  system_created_date = timezone.now()

  smart_view = SmartView._from_attrs(smart_view_id, name, query, user_id, system_created_date)

  return smart_view
