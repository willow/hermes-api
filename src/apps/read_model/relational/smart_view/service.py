from src.apps.read_model.relational.asset.models import ProfileLookupByProvider, EoLookupByProvider


def save_profile_lookup_by_provider(profile_id, external_id, provider_type, prospect_id):
  profile, _ = ProfileLookupByProvider.objects.update_or_create(
      id=profile_id, defaults=dict(
          external_id=external_id, provider_type=provider_type, prospect_id=prospect_id
      )
  )

  return profile


def save_eo_lookup_by_provider(eo_id, external_id, provider_type, prospect_id):
  eo, _ = EoLookupByProvider.objects.update_or_create(
      id=eo_id, defaults=dict(
          external_id=external_id, provider_type=provider_type, prospect_id=prospect_id
      )
  )

  return eo


def get_profile_lookup_from_provider_info(external_id, provider_type):
  return ProfileLookupByProvider.objects.get(external_id=external_id, provider_type=provider_type)


def get_profile_lookup(profile_id):
  return ProfileLookupByProvider.objects.get(id=profile_id)


def get_engagement_opportunity_lookup_from_provider_info(external_id, provider_type, prospect_id):
  return EoLookupByProvider.objects.get(
      external_id=external_id, provider_type=provider_type, prospect_id=prospect_id)


def delete_prospect(prospect_id):
  EoLookupByProvider.objects.filter(prospect_id=prospect_id).delete()
