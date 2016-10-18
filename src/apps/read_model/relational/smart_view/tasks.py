import logging

from django.db import IntegrityError
from django_rq import job

from src.apps.read_model.relational.asset import service
from src.domain.prospect.events import duplicate_profile_discovered
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('default')
def save_profile_lookup_by_provider_task(profile_id, external_id, provider_type, prospect_id):
  log_message = (
    "profile_id: %s, external_id: %s, provider_type: %s",
    prospect_id, external_id, provider_type
  )

  with log_wrapper(logger.info, *log_message):
    try:
      service.save_profile_lookup_by_provider(profile_id, external_id, provider_type, prospect_id)
    except IntegrityError:
      # we tried adding a duplicate profile which means we have a duplicate prospect - they need to be merged
      duplicate_profile_discovered.send(None, duplicate_prospect_id=prospect_id,
                                        existing_external_id=external_id,
                                        existing_provider_type=provider_type)
    return profile_id


@job('default')
def save_eo_lookup_by_provider_task(eo_id, external_id, provider_type, prospect_id):
  log_message = (
    "eo_id: %s, external_id: %s, provider_type: %s",
    eo_id, external_id, provider_type
  )

  with log_wrapper(logger.info, *log_message):
    service.save_eo_lookup_by_provider(eo_id, external_id, provider_type, prospect_id)
    return eo_id


@job('default')
def delete_prospect_task(prospect_id):
  log_message = (
    "prospect_id: %s",
    prospect_id
  )

  with log_wrapper(logger.info, *log_message):
    service.delete_prospect(prospect_id)
    return prospect_id
