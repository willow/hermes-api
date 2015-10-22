import logging

from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.conf import settings

from src.aggregates.potential_agreement.services import potential_agreement_service
from src.apps.asset.services import asset_service
from src.apps.agreement_translation.services import agreement_translation_service
from src.apps.api.resources.agreement.serializers.agreement import PotentialAgreementSerializer

constants = settings.CONSTANTS

logger = logging.getLogger(__name__)


@api_view(['POST', 'PUT'])
@parser_classes((FileUploadParser,))
def agreement_view(request, _agreement_translation_service=None, _asset_service=None):
  if not _agreement_translation_service: _agreement_translation_service = agreement_translation_service
  if not _asset_service: _asset_service = asset_service

  # this method should be considered internal and no public api call should be allowed to pass in a file for an agreement
  # refer to https://app.asana.com/0/10235149247655/46476660493804

  if request.method == 'POST':
    try:
      # get file and process it, validate it. capture info, like filename and other metadata.
      # if all goes well, submit to s3.
      contract_file = request.FILES['contract']

      # do this task first because persisting the asset will alter the file (name, etc.)
      agreement_data = _agreement_translation_service.get_agreement_info_from_file(contract_file)

      asset_information = _asset_service.persist_asset_from_file(contract_file, constants.ARTIFACTS_ROOT)

      potential_agreement_data = {
        'potential_agreement_name': agreement_data[constants.AGREEMENT_NAME],
        'potential_agreement_artifacts': [asset_information],  # put it in a list (could have multiple soon)
        'potential_agreement_user_id': request.user.user_id
      }

      potential_agreement = potential_agreement_service.create_potential_agreement(**potential_agreement_data)
      potential_agreement_serializer_data = PotentialAgreementSerializer(potential_agreement).data

    except Exception as e:
      logger.debug("Error creating agreement: {0}".format(request.data), exc_info=True)
      response = Response("Error creating agreement %s " % e, status.HTTP_400_BAD_REQUEST)

    else:
      response = Response(potential_agreement_serializer_data, status.HTTP_201_CREATED)

  else:
    response = Response("Error", status.HTTP_400_BAD_REQUEST)

  return response
