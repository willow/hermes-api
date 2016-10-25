from django.core.management.base import BaseCommand

from src.apps.maintenance.database.service import clear_rq_jobs
from src.libs.common_domain import event_store


class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument('event_names', nargs='*', default=None)

  def handle(self, *args, **options):
    clear_rq_jobs()
    event_store.clear_events(options['event_names'])
