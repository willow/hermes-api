import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from src.domain.asset import services

logger = logging.getLogger(__name__)


@api_view(['GET'])
def asset_view(request, asset_id, _asset_service=None):
  # this method should be considered internal and no public api call should be allowed to pass in a file for an agreement
  # refer to https://app.asana.com/0/10235149247655/46476660493804
  if not _asset_service: _asset_service = services

  try:
    asset_lookup = _asset_service.get_asset_lookup(asset_id)

    asset_path = _asset_service.get_signed_asset_path(asset_lookup.path)

  except Exception as e:
    logger.warn("Error retrieving asset path: {0}".format(asset_id), exc_info=True)
    response = Response("Error retrieving asset path %s " % e, status.HTTP_400_BAD_REQUEST)

  else:
    response = Response({'url': asset_path}, status=status.HTTP_200_OK)

  return response
