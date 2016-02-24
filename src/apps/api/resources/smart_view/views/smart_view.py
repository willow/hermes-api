import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

from src.aggregates.smart_view.services import smart_view_service
from src.apps.api.resources.smart_view.serializers.smart_view import SmartViewSerializer

constants = settings.CONSTANTS

logger = logging.getLogger(__name__)


@api_view(['POST'])
def smart_view_create_view(request, _smart_view_service=None):
  if not _smart_view_service: _smart_view_service = smart_view_service

  try:
    name = request.data[constants.NAME]
    query = request.data[constants.QUERY]
    smart_view_user_id = request.user.id
    smart_view_data = {
      'smart_view_name': name,
      'smart_view_query': query,
      'smart_view_user_id': smart_view_user_id
    }

    smart_view = _smart_view_service.create_smart_view(**smart_view_data)
    smart_view_serializer_data = SmartViewSerializer(smart_view).data

  except Exception as e:
    logger.warn("Error creating smart view: {0}".format(request.data), exc_info=True)
    response = Response("Error creating smart view %s " % e, status.HTTP_400_BAD_REQUEST)

  else:
    response = Response(smart_view_serializer_data, status.HTTP_201_CREATED)

  return response


@api_view(['PUT'])
def smart_view_update_view(request, smart_view_id, _smart_view_service=None):
  if not _smart_view_service: _smart_view_service = smart_view_service

  try:
    name = request.data[constants.NAME]
    query = request.data[constants.QUERY]

    smart_view = smart_view_service.get_smart_view(smart_view_id)

    smart_view.update_attrs(name, query)
    _smart_view_service.save_or_update(smart_view)
    smart_view_serializer_data = SmartViewSerializer(smart_view).data

  except Exception as e:
    logger.warn("Error updating smart view: {0}".format(request.data), exc_info=True)
    response = Response("Error updating smart view %s " % e, status.HTTP_400_BAD_REQUEST)

  else:
    response = Response(smart_view_serializer_data, status.HTTP_200_OK)

  return response
