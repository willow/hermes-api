import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

from src.domain.smart_view import command_handlers
from src.domain.smart_view.commands import CreateSmartView, UpdateSmartViewAttrs
from src.libs.common_domain import dispatcher

from src.apps.common import constants

logger = logging.getLogger(__name__)


@api_view(['POST'])
def smart_view_create_view(request, _command_handler=None):
  if not _command_handler: _command_handler = command_handlers

  try:
    name = request.data[constants.NAME]
    query = request.data[constants.QUERY]
    smart_view_user_id = request.user.id
    smart_view_data = {
      'name': name,
      'query': query,
      'user_id': smart_view_user_id
    }

    command = CreateSmartView(**smart_view_data)
    smart_view = _command_handler.create_smart_view(**{'command': command})
    smart_view_data = {'id': smart_view.id}
  except Exception as e:
    logger.warn("Error creating smart view: {0}".format(request.data), exc_info=True)
    response = Response("Error creating smart view %s " % e, status.HTTP_400_BAD_REQUEST)

  else:
    response = Response(smart_view_data, status.HTTP_201_CREATED)

  return response


@api_view(['PUT'])
def smart_view_update_view(request, smart_view_id, _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher

  try:
    name = request.data[constants.NAME]
    query = request.data[constants.QUERY]

    command = UpdateSmartViewAttrs(name, query)
    _dispatcher.send_command(smart_view_id, command)
  except Exception as e:
    logger.warn("Error updating smart view: {0}".format(request.data), exc_info=True)
    response = Response("Error updating smart view %s " % e, status.HTTP_400_BAD_REQUEST)
  else:
    response = Response(status=status.HTTP_200_OK)

  return response
