from src.aggregates.asset.services import asset_factory


def save_or_update(asset):
  asset.save(internal=True)


def create_asset(asset_path, asset_content_type, asset_original_name):
  asset = asset_factory.create_asset(asset_path, asset_content_type, asset_original_name)
  save_or_update(asset)
  return asset
