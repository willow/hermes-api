from django.utils import timezone

from src.aggregates.asset.models import Asset


def create_asset(asset_id, path, content_type, original_name):
  system_created_date = timezone.now()

  asset = Asset._from_attrs(asset_id, path, content_type, original_name, system_created_date)

  return asset
