from django.db import models
from jsonfield import JSONField


class Event(models.Model):
  aggregate_id = models.CharField(max_length=255)
  aggregate_name = models.CharField(max_length=255)
  event_version = models.PositiveIntegerField()
  event_name = models.CharField(max_length=1024)
  event_data = JSONField()

  def __str__(self):
    return '{0}:{1}:{2}'.format(self.aggregate_name, self.aggregate_id, self.event_name)
