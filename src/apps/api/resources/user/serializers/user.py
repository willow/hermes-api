from rest_framework import serializers
from src.aggregates.user.models import User


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    exclude = ('id', 'user_system_created_date')
