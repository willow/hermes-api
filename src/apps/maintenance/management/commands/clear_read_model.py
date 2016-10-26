from django.core.management.base import NoArgsCommand

from src.apps.maintenance.database.service import clear_read_model


class Command(NoArgsCommand):
  def handle_noargs(self, **options):
    clear_read_model()
