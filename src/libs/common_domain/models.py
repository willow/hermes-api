from django.db import models
from django.utils import timezone
from jsonfield import JSONField


class Event(models.Model):
  stream_id = models.CharField(max_length=255)
  event_sequence = models.PositiveIntegerField()
  event_type = models.CharField(max_length=1024)
  event_name = models.CharField(max_length=1024)
  event_data = JSONField()
  system_created_date = models.DateTimeField(default=timezone.now)

  class Meta:
    unique_together = ("stream_id", "event_type", "event_sequence")

  def __str__(self):
    return '{0}:{1}:{2}:{3}'.format(self.event_type, self.stream_id, self.event_sequence, self.event_name)
