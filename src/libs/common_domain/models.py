from django.db import models
from jsonfield import JSONField


class Event(models.Model):
  version = models.PositiveIntegerField()
  name = models.CharField(max_length=1024)
  data = JSONField()

  def __str__(self):
    return 'Event #' + str(self.pk) + ': ' + self.name
