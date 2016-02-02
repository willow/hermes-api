from django.utils import timezone
from src.aggregates.alert.models import Alert

from src.libs.python_utils.id.id_utils import generate_id


def create_alert(alert_name, alert_query, alert_user_id):
  alert_id = generate_id()
  alert_system_created_date = timezone.now()

  alert = Alert._from_attrs(alert_id, alert_name, alert_query, alert_user_id, alert_system_created_date)

  return alert
