from django.core.management.base import NoArgsCommand
from src.libs.common_domain import event_store


class Command(NoArgsCommand):
  def handle_noargs(self, **options):
    event_store.replay_events()
