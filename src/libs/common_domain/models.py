from django.db import models
from django.utils import timezone
from jsonfield import JSONField


class Event(models.Model):
  stream_id = models.CharField(max_length=255)
  event_sequence = models.PositiveIntegerField()
  event_name = models.CharField(max_length=1024)
  event_data = JSONField()
  system_created_date = models.DateTimeField(default=timezone.now)

  class Meta:
    unique_together = ("stream_id", "event_sequence")

  def __str__(self):
    return '{0}:{1}:{2}'.format(self.stream_id, self.event_sequence, self.event_name)
