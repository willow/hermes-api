import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from src.apps.common import constants
from src.domain.agreement_type import command_handlers
from src.domain.agreement_type.commands import CreateAgreementType

logger = logging.getLogger(__name__)


@api_view(['POST'])
def agreement_type_create_view(request, _command_handler=None):
  if not _command_handler: _command_handler = command_handlers

  try:

    name = request.data[constants.NAME]

    agreement_type_user_id = request.user.id

    agreement_type_data = {
      'name': name,
      'is_global': False,
      'user_id': agreement_type_user_id
    }

    command = CreateAgreementType(**agreement_type_data)

    at = _command_handler.create_agreement_type(**{'command': command})

    at_data = {'id': at.id}

  except Exception as e:
    logger.warn("Error creating agreement_type: {0}".format(request.data), exc_info=True)
    response = Response("Error creating agreement_type %s " % e, status.HTTP_400_BAD_REQUEST)

  else:
    response = Response(at_data, status.HTTP_201_CREATED)

  return response
