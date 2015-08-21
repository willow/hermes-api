import logging

from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.response import Response

from src.aggregates.user.services import user_service
from src.apps.api.resources.user.serializers.user import UserSerializer

logger = logging.getLogger(__name__)


@api_view(['POST'])
def user_view(request):
  # from rest_framework import serializers
  # raise serializers.ValidationError('Value was invalid')
  try:
    user = user_service.create_user(**request.data)
    user_data = UserSerializer(user).data
  except Exception as e:
    logger.debug("Error creating user: {0}".format(request.data), exc_info=True)

    status_result = status.HTTP_409_CONFLICT if isinstance(e, IntegrityError) else status.HTTP_400_BAD_REQUEST
    response = Response("Error creating user %s " % e, status_result)
  else:
    response = Response(user_data, status.HTTP_201_CREATED)

  return response
