from rest_framework import serializers
from src.aggregates.user.models import User


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    exclude = ('id', 'system_created_date')
