from django.core.management.base import BaseCommand

from src.libs.common_domain import event_store
from django.apps import apps


class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument('-en', '--event-names', nargs='*', default=None)
    parser.add_argument('-an', '--app-names', nargs='*', default=None)

  def handle(self, *args, **options):
    event_names = options['event_names']

    app_names = options['app_names']
    if app_names:
      for a in app_names:
        a = a.split('.')[0]
        # just ensure this app exists and works
        apps.get_app_config(a)

    event_store.replay_events(event_names, app_names)
