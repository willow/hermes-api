from django.utils import timezone

from src.aggregates.asset.models import Asset


def create_asset(asset_id, asset_path, asset_content_type, asset_original_name):
  asset_system_created_date = timezone.now()

  asset = Asset._from_attrs(asset_id, asset_path, asset_content_type, asset_original_name, asset_system_created_date)

  return asset
