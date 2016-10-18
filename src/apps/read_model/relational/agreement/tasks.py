import logging

from django_rq import job

from src.apps.read_model.relational.agreement import service
from src.domain.prospect.service import prospect_is_deleted
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def save_active_ta_topic_option_task(id, option_name, option_type, option_attrs, ta_topic_id,
                                     ta_topic_relevance, topic_id, client_id):
  log_message = ("Save ta topic option task for ta_topic_option_id: %s", id)

  with log_wrapper(logger.info, *log_message):
    return service.save_active_ta_topic_option(
        id, option_name, option_type, option_attrs, ta_topic_id, ta_topic_relevance
        , topic_id, client_id
    ).id


@job('high')
def save_client_ea_lookup_task(id, ta_attrs):
  log_message = ("id: %s", id)

  with log_wrapper(logger.info, *log_message):
    return service.save_client_ea_lookup(id, ta_attrs).id


@job('high')
def save_topic_to_client_ea_lookup_task(client_id, relevance, topic_id):
  log_message = ("client_id: %s topic_id: %s", client_id, topic_id)

  with log_wrapper(logger.info, *log_message):
    return service.save_topic_to_client_ea_lookup(client_id, relevance, topic_id)


@job('default')
def save_prospect_ea_lookup_task(id, attrs):
  log_message = ("id: %s", id)

  with log_wrapper(logger.info, *log_message):
    return service.save_prospect_ea_lookup(id, attrs).id


@job('default')
def save_topics_to_prospect_ea_lookup_task(prospect_id, topic_ids):
  log_message = ("id: %s", prospect_id)

  with log_wrapper(logger.info, *log_message):
    if prospect_is_deleted(prospect_id):
      logger.info('prospect %s is deleted. aborting task', prospect_id)
    else:
      return service.save_topics_to_prospect_ea_lookup(prospect_id, topic_ids).id


@job('default')
def save_profile_ea_lookup_task(id, profile_attrs, provider_type, prospect_id):
  log_message = ("id: %s", id)

  with log_wrapper(logger.info, *log_message):
    return service.save_profile_ea_lookup(id, profile_attrs, provider_type, prospect_id).id


@job('default')
def save_eo_ea_lookup_task(id, eo_attrs, topic_ids, provider_type, profile_id, prospect_id):
  log_message = ("id: %s", id)

  with log_wrapper(logger.info, *log_message):
    return service.save_eo_ea_lookup(id, eo_attrs, topic_ids, provider_type, profile_id, prospect_id).id


@job('default')
def delete_prospect_task(prospect_id):
  log_message = (
    "prospect_id: %s",
    prospect_id
  )

  with log_wrapper(logger.info, *log_message):
    service.delete_prospect(prospect_id)
    return prospect_id


@job('default')
def delete_batch_ea_task(client_id, batch_id):
  service.delete_batch_ea(client_id, batch_id)
