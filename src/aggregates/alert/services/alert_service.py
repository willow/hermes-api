from src.aggregates.alert.models import Alert
from src.aggregates.alert.services import alert_factory


def get_alert(alert_id):
  return Alert.objects.get(alert_id=alert_id)


def save_or_update(alert):
  alert.save(internal=True)


def create_alert(alert_name, alert_query, alert_user_id):
  alert = alert_factory.create_alert(alert_name, alert_query, alert_user_id)
  save_or_update(alert)
  return alert
