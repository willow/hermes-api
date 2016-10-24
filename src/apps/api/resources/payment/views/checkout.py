import logging

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from src.domain.user.commands import SubscribeUser
from src.libs.common_domain import dispatcher

from src.apps.common import constants

logger = logging.getLogger(__name__)


@api_view(['POST'])
def checkout_view(request, _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher

  try:
    payment_token = request.data[constants.TOKEN]
    command = SubscribeUser(payment_token)
    _dispatcher.send_command(request.user.id, command)

  except Exception as e:
    logger.warn("Error subscribing user: {0}".format(request.data), exc_info=True)
    response = Response("Error subscribing user %s " % e, status.HTTP_400_BAD_REQUEST)

  else:
    response = Response(status=status.HTTP_201_CREATED)

  return response
