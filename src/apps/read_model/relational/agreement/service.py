import json
import logging

from django.db import transaction

from src.apps.read_model.relational.agreement.models import ActiveTaTopicOption, ClientLookupForEa, EoLookupForEa, \
  ProspectLookupForEa, ProfileLookupForEa, BatchEa, DeliveredEa
from src.apps.read_model.relational.agreement_type.service import get_topic_lookup
from src.domain.common import constants

logger = logging.getLogger(__name__)


def get_active_ta_topic_options():
  active_topics = ActiveTaTopicOption.objects.all()
  return active_topics


def get_ta_topic_option(ta_topic_option_id):
  return ActiveTaTopicOption.objects.get(id=ta_topic_option_id)


def save_active_ta_topic_option(id, option_name, option_type, option_attrs, ta_topic_id, ta_topic_relevance,
                                topic_id, client_id):
  at, _ = ActiveTaTopicOption.objects.update_or_create(
      id=id, defaults=dict(
          option_name=option_name, option_type=option_type,
          option_attrs=option_attrs, ta_topic_id=ta_topic_id, ta_topic_relevance=ta_topic_relevance,
          topic_id=topic_id, client_id=client_id
      )
  )
  return at


def save_client_ea_lookup(id, ta_attrs):
  client, _ = ClientLookupForEa.objects.update_or_create(
      id=id, defaults=dict(
          ta_attrs=ta_attrs
      )
  )
  return client


def save_topic_to_client_ea_lookup(client_id, relevance, topic_id):
  with transaction.atomic():
    client = get_client_ea_lookup(client_id)
    topic = get_topic_lookup(topic_id)
    client.ta_topics[topic_id] = {
      constants.NAME: topic.name,
      constants.RELEVANCE: relevance
    }

    client.save()

  return client


def save_prospect_ea_lookup(id, attrs):
  prospect, _ = ProspectLookupForEa.objects.update_or_create(
      id=id, defaults=dict(
          attrs=attrs
      )
  )
  return prospect


def save_topics_to_prospect_ea_lookup(prospect_id, topic_ids):
  with transaction.atomic():
    prospect = get_prospect_ea_lookup(prospect_id)
    prospect.topic_ids.extend(topic_ids)
    prospect.save()

  return prospect


def save_profile_ea_lookup(id, profile_attrs, provider_type, prospect_id):
  profile, _ = ProfileLookupForEa.objects.update_or_create(
      id=id, defaults=dict(
          provider_type=provider_type, profile_attrs=profile_attrs, prospect_id=prospect_id
      )
  )
  return profile


def save_eo_ea_lookup(id, eo_attrs, topic_ids, provider_type, profile_id, prospect_id):
  eo, _ = EoLookupForEa.objects.update_or_create(
      id=id, defaults=dict(
          eo_attrs=eo_attrs, topic_ids=topic_ids,
          provider_type=provider_type, profile_id=profile_id,
          prospect_id=prospect_id
      )
  )
  return eo


def get_client_ea_lookup(id):
  return ClientLookupForEa.objects.get(id=id)


def get_prospect_ea_lookup(id):
  return ProspectLookupForEa.objects.get(id=id)


def get_profile_ea_lookups_by_prospect_id(prospect_id):
  return ProfileLookupForEa.objects.filter(prospect_id=prospect_id)


def get_eo_ea_lookup(id):
  return EoLookupForEa.objects.get(id=id)


def delete_prospect(prospect_id):
  ProfileLookupForEa.objects.filter(prospect_id=prospect_id).delete()
  EoLookupForEa.objects.filter(prospect_id=prospect_id).delete()
  ProspectLookupForEa.objects.filter(id=prospect_id).delete()


def save_batch_ea(ea_id, attrs, score_attrs, client_id, batch_id, counter, prospect_id):
  ea, _ = BatchEa.objects.update_or_create(
      id=ea_id, defaults=dict(
          attrs=attrs, score_attrs=score_attrs, client_id=client_id, batch_id=batch_id, counter=counter,
          prospect_id=prospect_id,
      )
  )
  return ea


def save_delivered_ea(ea_id, name, bio, location, url, score, batch_id, score_attrs, assigned_entities, prospect_id):
  ea, _ = DeliveredEa.objects.update_or_create(
      id=ea_id, defaults=dict(
          name=name, bio=bio, location=location, url=url, score=score, batch_id=batch_id,
          score_attrs=score_attrs,
          assigned_entities=assigned_entities,
          prospect_id=prospect_id,
      )
  )
  return ea


def delete_batch_ea(client_id, batch_id):
  return get_batch_ea(client_id, batch_id).delete()


def get_batch_ea(client_id, batch_id):
  return BatchEa.objects.filter(client_id=client_id, batch_id=batch_id)


def get_assignment_batch_processed_count(client_id, batch_id):
  ret_val = get_batch_ea(client_id, batch_id).count()

  return ret_val


def get_assignment_batch(client_id, batch_id):
  ret_val = get_batch_ea(client_id, batch_id).values(constants.ID, constants.ATTRS, constants.SCORE_ATTRS,
                                                     constants.PROSPECT_ID)

  loaded = [_process_batch(r) for r in ret_val]

  return loaded


def _process_batch(attrs):
  ret_val = dict(**attrs)

  ret_val[constants.ATTRS] = json.loads(ret_val[constants.ATTRS])
  ret_val[constants.SCORE_ATTRS] = json.loads(ret_val[constants.SCORE_ATTRS])

  return ret_val
