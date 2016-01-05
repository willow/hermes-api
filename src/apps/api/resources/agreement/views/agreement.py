import logging

from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.conf import settings

from src.apps.realtime.agreement.services import agreement_service as realtime_agreement_service
from src.aggregates.potential_agreement.services import potential_agreement_service
from src.apps.agreement.enums import DurationTypeEnum
from src.aggregates.asset.services import asset_service
from src.apps.agreement_translation.services import agreement_translation_service
from src.apps.api.resources.agreement.serializers.agreement import PotentialAgreementSerializer
from src.libs.datetime_utils import datetime_utils

constants = settings.CONSTANTS

logger = logging.getLogger(__name__)


@api_view(['POST'])
@parser_classes((FileUploadParser,))
def agreement_create_view(request, _potential_agreement_service=None, _agreement_translation_service=None,
                          _asset_service=None,
                          _realtime_agreement_service=None):
  # this method should be considered internal and no public api call should be allowed to pass in a file for an agreement
  # refer to https://app.asana.com/0/10235149247655/46476660493804

  if not _agreement_translation_service: _agreement_translation_service = agreement_translation_service
  if not _asset_service: _asset_service = asset_service
  if not _realtime_agreement_service: _realtime_agreement_service = realtime_agreement_service
  if not _potential_agreement_service: _potential_agreement_service = potential_agreement_service

  try:
    # get file and process it, validate it. capture info, like filename and other metadata.
    # if all goes well, submit to s3.
    contract_file = request.FILES['contract']

    # do this task first because persisting the asset will alter the file (name, etc.)
    agreement_data = _agreement_translation_service.get_agreement_info_from_file(contract_file)

    asset = _asset_service.create_asset_from_file(constants.ARTIFACTS_ROOT, contract_file)

    potential_agreement_data = {
      'potential_agreement_name': agreement_data[constants.AGREEMENT_NAME],
      'potential_agreement_artifacts': [asset.asset_id],  # put it in a list (could have multiple soon)
      'potential_agreement_user_id': request.user.user_id
    }

    potential_agreement = _potential_agreement_service.create_potential_agreement(**potential_agreement_data)
    potential_agreement_serializer_data = PotentialAgreementSerializer(potential_agreement).data

    # doing this here and not in an event handler because the UI goes immediately to this firebase uri and runs into
    # a permission error because the resource doesn't exist. in the future it'd be good to have this api resource
    # stub out in firebase that the agreement is processing and have the event handler pick up the remaining work and
    # fill out the remaining details (agreement translation stuff).
    _realtime_agreement_service.save_agreement_edit_in_firebase(potential_agreement.potential_agreement_id)

  except Exception as e:
    logger.warn("Error creating agreement: {0}".format(request.data), exc_info=True)
    response = Response("Error creating agreement %s " % e, status.HTTP_400_BAD_REQUEST)

  else:
    response = Response(potential_agreement_serializer_data, status.HTTP_201_CREATED)

  return response


@api_view(['PUT'])
def agreement_update_view(request, agreement_id, _potential_agreement_service=None, _datetime_utils=None):
  # this method should be considered internal and no public api call should be allowed to pass in a file for an agreement
  # refer to https://app.asana.com/0/10235149247655/46476660493804

  if not _potential_agreement_service: _potential_agreement_service = potential_agreement_service
  if not _datetime_utils: _datetime_utils = datetime_utils

  try:

    potential_agreement = _potential_agreement_service.get_potential_agreement(agreement_id)

    agreement_type = request.data[constants.TYPE_ID]

    name = request.data[constants.NAME]
    counterparty = request.data[constants.COUNTERPARTY]
    description = request.data[constants.DESCRIPTION]
    execution_date = _datetime_utils.get_utc_from_timestamp(request.data[constants.EXECUTION_DATE])
    term_length_amount = request.data[constants.TERM_LENGTH_AMOUNT]
    term_length_type = DurationTypeEnum[request.data[constants.TERM_LENGTH_TYPE]]
    auto_renew = request.data[constants.AUTO_RENEW]
    renewal_notice_amount = request.data[constants.RENEWAL_NOTICE_AMOUNT]
    renewal_notice_type = DurationTypeEnum[request.data[constants.RENEWAL_NOTICE_TYPE]]
    duration_details = request.data[constants.DURATION_DETAILS]

    potential_agreement_data = {
      'potential_agreement_name': name,
      'potential_agreement_counterparty': counterparty,
      'potential_agreement_description': description,
      'potential_agreement_execution_date': execution_date,
      'potential_agreement_type_id': agreement_type,
      'potential_agreement_term_length_amount': term_length_amount,
      'potential_agreement_term_length_type': term_length_type,
      'potential_agreement_auto_renew': auto_renew,
      'potential_agreement_renewal_notice_amount': renewal_notice_amount,
      'potential_agreement_renewal_notice_type': renewal_notice_type,
      'potential_agreement_duration_details': duration_details,
    }

    potential_agreement.complete(**potential_agreement_data)
    _potential_agreement_service.save_or_update(potential_agreement)

  except Exception as e:
    logger.warn("Error saving agreement: {0}".format(request.data), exc_info=True)
    response = Response("Error saving agreement %s " % e, status.HTTP_400_BAD_REQUEST)

  else:
    response = Response(status=status.HTTP_200_OK)

  return response
