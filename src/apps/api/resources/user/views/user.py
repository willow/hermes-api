import logging

from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from src.domain.user import command_handlers
from src.domain.user.commands import CreateUser

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes((AllowAny,))
def user_view(request, _command_handler=None):
  if not _command_handler: _command_handler = command_handlers
  try:
    command = CreateUser(**request.data)
    user = _command_handler.create_user(**{'command': command})
    user_data = {'id': user.id}
  except Exception as e:
    logger.warn("Error creating user: {0}".format(request.data), exc_info=True)

    status_result = status.HTTP_409_CONFLICT if isinstance(e, IntegrityError) else status.HTTP_400_BAD_REQUEST
    response = Response("Error creating user %s " % e, status_result)
  else:
    response = Response(user_data, status.HTTP_201_CREATED)

  return response
