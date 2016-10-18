import json
from operator import itemgetter

from django.contrib import admin
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer

from src.apps.read_model.relational.agreement.models import DeliveredEa
from src.domain.common import constants


class DeliveredEaAdmin(admin.ModelAdmin):
  readonly_fields = ('score_attrs_pretty', 'engagement_opportunity')

  actions = None
  list_display = ('name', 'location', 'bio', 'engagement_opportunity', 'score', 'batch_id')

  def has_delete_permission(self, request, obj=None):
    return False

  def has_add_permission(self, request):
    return False

  # Allow viewing objects but not actually changing them
  # https://gist.github.com/aaugustin/1388243
  def has_change_permission(self, request, obj=None):
    if request.method not in ('GET', 'HEAD'):
      return False
    return super().has_change_permission(request, obj)

  # def get_readonly_fields(self, request, obj=None):
  #   return (self.fields or [f.name for f in self.model._meta.fields]) + list(DeliveredEaAdmin.readonly_fields)

  def score_attrs_pretty(self, instance):
    """Function to display pretty version of our data"""
    # Convert the data to sorted, indented JSON
    response = json.dumps(instance.score_attrs[constants.SCORE][constants.SCORE_ATTRS], sort_keys=True, indent=2)

    # Get the Pygments formatter
    formatter = HtmlFormatter(style='colorful')

    # Highlight the data
    response = highlight(response, JsonLexer(), formatter)

    # Get the stylesheet
    style = "<style>" + formatter.get_style_defs() + "</style><br>"

    # Safe the output
    return mark_safe(style + response)

  def engagement_opportunity(self, instance):
    """Function to display pretty version of our data"""
    # Convert the data to sorted, indented JSON
    aes = instance.score_attrs[constants.ASSIGNED_ENTITIES][constants.DATA]
    total_aes = len(aes)
    top_eos = sorted(aes, key=itemgetter('score'), reverse=True)[:3]
    top_eos_ids = [t[constants.ID] for t in top_eos]
    top_eos_text = [next(ae for ae in instance.assigned_entities if ae[constants.ID] == tid) for tid in
                    top_eos_ids]

    total_p = '<p>Total AE\'s: {0}</p>'.format(total_aes)
    return mark_safe(total_p + ''.join('<p><a href="{0}" target="_blank">{1}</a></p>'.format(t[constants.URL],
                                                                                             t[constants.TEXT]) for t
                                       in
                                       top_eos_text))

  score_attrs_pretty.short_description = 'Score Attrs'


admin.site.register(DeliveredEa, DeliveredEaAdmin)
