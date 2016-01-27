from src.aggregates.smart_view.models import SmartView
from src.aggregates.smart_view.services import smart_view_factory


def get_smart_view(smart_view_id):
  return SmartView.objects.get(smart_view_id=smart_view_id)


def save_or_update(smart_view):
  smart_view.save(internal=True)


def create_smart_view(smart_view_name, smart_view_query, smart_view_user_id):
  smart_view = smart_view_factory.create_smart_view(smart_view_name, smart_view_query, smart_view_user_id)
  save_or_update(smart_view)
  return smart_view
