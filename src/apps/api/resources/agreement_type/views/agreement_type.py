import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

from src.aggregates.agreement_type.services import agreement_type_service
from src.apps.api.resources.agreement_type.serializers.agreement_type import AgreementTypeSerializer

constants = settings.CONSTANTS

logger = logging.getLogger(__name__)


@api_view(['POST'])
def agreement_type_create_view(request, _agreement_type_service=None):
  if not _agreement_type_service: _agreement_type_service = agreement_type_service

  try:

    name = request.data[constants.NAME]
    agreement_type_user_id = request.user.id

    agreement_type_data = {
      'name': name,
      'is_global': False,
      'user_id': agreement_type_user_id
    }

    agreement_type = _agreement_type_service.create_agreement_type(**agreement_type_data)
    agreement_type_serializer_data = AgreementTypeSerializer(agreement_type).data

  except Exception as e:
    logger.warn("Error creating agreement_type: {0}".format(request.data), exc_info=True)
    response = Response("Error creating agreement_type %s " % e, status.HTTP_400_BAD_REQUEST)

  else:
    response = Response(agreement_type_serializer_data, status.HTTP_201_CREATED)

  return response
