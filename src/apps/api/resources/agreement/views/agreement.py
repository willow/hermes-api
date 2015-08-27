import logging

from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FileUploadParser

from rest_framework.response import Response

from src.aggregates.user.services import user_service
from src.apps.api.resources.user.serializers.user import UserSerializer

logger = logging.getLogger(__name__)


@api_view(['POST'])
@parser_classes((FileUploadParser,))
def agreement_view(request):
  try:
    # this method should be considered internal and no public api call should be allowed to pass in a file for an agreement
    # refer to https://app.asana.com/0/10235149247655/46476660493804

    # get file and process it, validate it. capture info, like filename and other metadata.
    # if all goes well, submit to s3.

    user = user_service.create_user(**request.data)
    user_data = UserSerializer(user).data
  except Exception as e:
    logger.debug("Error creating user: {0}".format(request.data), exc_info=True)

    status_result = status.HTTP_409_CONFLICT if isinstance(e, IntegrityError) else status.HTTP_400_BAD_REQUEST
    response = Response("Error creating user %s " % e, status_result)
  else:
    response = Response(user_data, status.HTTP_201_CREATED)

  return response
