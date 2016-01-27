from rest_framework import serializers

from src.aggregates.smart_view.models import SmartView


class SmartViewSerializer(serializers.ModelSerializer):
  class Meta:
    model = SmartView
    fields = ('smart_view_id', 'smart_view_name')
