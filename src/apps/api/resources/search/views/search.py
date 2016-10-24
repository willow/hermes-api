import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from src.apps.common import constants
from src.apps.search.services import search_service

logger = logging.getLogger(__name__)

import time


@api_view(['GET'])
def federated_search_view(request, _search_service=None):
  if not _search_service: _search_service = search_service
  query = request.query_params.get('q')

  try:
    result_set = _search_service.federated_search(request.user, query)
  except Exception as e:
    logger.warn("Error searching: {0}".format(query), exc_info=True)

    response = Response("Error searching %s " % e, status.HTTP_400_BAD_REQUEST)
  else:
    response = Response(result_set, status.HTTP_200_OK)

  if query == 'test':
    time.sleep(2)
  return response


@api_view(['GET'])
def advanced_search_view(request, _search_service=None):
  if not _search_service: _search_service = search_service

  text = request.query_params.get(constants.TEXT)
  counterparty = request.query_params.get(constants.COUNTERPARTY)
  agreement_type_id = request.query_params.get(constants.TYPE_ID)

  try:

    if agreement_type_id:
      agreement_type_id = agreement_type_id.strip()

    result_set = _search_service.advanced_search(request.user.id, text, counterparty, agreement_type_id)
  except Exception as e:
    logger.warn("Error searching: {0}".format(request.data), exc_info=True)

    response = Response("Error searching %s " % e, status.HTTP_400_BAD_REQUEST)
  else:
    response = Response(result_set, status.HTTP_200_OK)

  return response
