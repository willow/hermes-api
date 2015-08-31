from rest_framework import serializers

from src.apps.agreement_domain.models import PotentialAgreement


class PotentialAgreementSerializer(serializers.ModelSerializer):
  class Meta:
    model = PotentialAgreement
    exclude = ('id', 'system_created_date')
