from django.conf import settings

from src.apps.read_model.relational.asset.models import AssetLookup
from src.libs.django_utils.storage import storage_utils

from src.apps.common import constants

assets_root = constants.ASSETS_ROOT


def get_asset_lookup(asset_id):
  return AssetLookup.objects.get(id=asset_id)


def create_asset_lookup(asset_id, name, path):
  ret_val = AssetLookup(id=asset_id, name=name, path=path)
  ret_val.save()
  return ret_val


def get_signed_asset_path(path, _storage_utils=None):
  if not _storage_utils: _storage_utils = storage_utils

  asset_path = "{0}/{1}".format(assets_root, path)

  ret_val = _storage_utils.get_file_path(asset_path)

  return ret_val
