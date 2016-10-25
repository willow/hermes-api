import logging

from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from src.apps.common import constants
from src.domain.user.commands import CreateUser
from src.libs.common_domain import dispatcher
from src.libs.python_utils.id.id_utils import generate_id

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes((AllowAny,))
def user_view(request, _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher
  try:
    user_id = generate_id()

    command = CreateUser(user_id, **request.data)
    _dispatcher.send_command(-1, command)

    user_data = {constants.ID: user_id}
  except Exception as e:
    logger.warn("Error creating user: {0}".format(request.data), exc_info=True)

    status_result = status.HTTP_409_CONFLICT if isinstance(e, IntegrityError) else status.HTTP_400_BAD_REQUEST
    response = Response("Error creating user %s " % e, status_result)
  else:
    response = Response(user_data, status.HTTP_201_CREATED)

  return response
