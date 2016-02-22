# from jsonfield import JSONField
#
# from django.db import models, transaction
#
# from src.aggregates.alert.signals import created, updated_attrs
# from src.libs.common_domain.aggregate_base import AggregateBase
# from src.libs.common_domain.models import Event
#
#
# class Alert(models.Model, AggregateBase):
#   uid = models.CharField(max_length=8, unique=True)
#   name = models.CharField(max_length=2400)
#   query = JSONField()
#   user = models.ForeignKey('user.User', 'uid', related_name='alerts')
#   system_created_date = models.DateTimeField()
#
#   @classmethod
#   def _from_attrs(cls, uid, name, query, user_id,
#                   system_created_date):
#     ret_val = cls()
#
#     if not uid:
#       raise TypeError("uid is required")
#
#     if not name:
#       raise TypeError("name is required")
#
#     if not query:
#       raise TypeError("query is required")
#
#     if not user_id:
#       raise TypeError("user_id is required")
#
#     ret_val._raise_event(
#       created,
#       uid=uid,
#       name=name,
#       query=query,
#       user_id=user_id,
#       system_created_date=system_created_date
#     )
#
#     return ret_val
#
#   def update_attrs(self, name, query):
#     if not name:
#       raise TypeError("name is required")
#
#     if not query:
#       raise TypeError("query is required")
#
#     self._raise_event(
#       updated_attrs,
#       uid=self.uid,
#       name=name,
#       query=query
#     )
#
#   def _handle_created_event(self, **kwargs):
#     self.uid = kwargs['uid']
#     self.name = kwargs['name']
#     self.query = kwargs['query']
#     self.user_id = kwargs['user_id']
#     self.system_created_date = kwargs['system_created_date']
#
#   def _handle_updated_attrs_event(self, **kwargs):
#     self.name = kwargs['name']
#     self.query = kwargs['query']
#
#   def __str__(self):
#     return 'Alert {id}: {name}'.format(id=self.uid, name=self.name)
#
#   def save(self, internal=False, *args, **kwargs):
#     if internal:
#       with transaction.atomic():
#         super().save(*args, **kwargs)
#
#         for event in self._uncommitted_events:
#
#           Event.objects.create(
#             aggregate_name=self.__class__.__name__, aggregate_id=self.uid,
#             event_name=event.event_fq_name, event_version=event.version, event_data=event.kwargs
#           )
#
#       self.send_events()
#     else:
#       from src.aggregates.alert.services import service
#
#       service.save_or_update(self)
