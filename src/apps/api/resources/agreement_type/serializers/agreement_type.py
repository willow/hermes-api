from rest_framework import serializers

from src.aggregates.agreement_type.models import AgreementType


class AgreementTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = AgreementType
    fields = ('agreement_type_id', 'agreement_type_name')
