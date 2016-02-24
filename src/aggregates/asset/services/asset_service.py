from django.conf import settings
from src.aggregates.asset.models import Asset

from src.libs.python_utils.files import file_utils
from src.libs.python_utils.id.id_utils import generate_id
from src.libs.django_utils.storage import storage_utils
from src.aggregates.asset.services import asset_factory

constants = settings.CONSTANTS
assets_root = constants.ASSETS_ROOT


def save_or_update(asset):
  asset.save(internal=True)


def get_asset(asset_id):
  asset = Asset.objects.get(id=asset_id)

  return asset


def get_assets(asset_ids):
  assets = Asset.objects.filter(id__in=asset_ids)

  return assets


def create_asset_from_file(original_path, file):
  original_name = file.name
  asset_id = generate_id()

  asset_id_with_ext = _generate_asset_id_from_filename(asset_id, original_name)
  path = "{0}/{1}".format(original_path, asset_id_with_ext)

  _save_file_to_storage(path, file)

  asset = asset_factory.create_asset(asset_id, path, file.content_type, original_name)
  save_or_update(asset)
  return asset


def _generate_asset_id_from_filename(asset_id, filename, _file_utils=None):
  if not _file_utils: _file_utils = file_utils

  asset_id_with_ext = "{0}.{1}".format(asset_id, _file_utils.get_file_extension(filename))

  return asset_id_with_ext


def _save_file_to_storage(path, file, _storage_utils=None):
  if not _storage_utils: _storage_utils = storage_utils

  asset_path = "{0}/{1}".format(assets_root, path)

  ret_val = _storage_utils.save_file(asset_path, file)

  return ret_val


def get_signed_asset_path(path, _storage_utils=None):
  if not _storage_utils: _storage_utils = storage_utils

  asset_path = "{0}/{1}".format(assets_root, path)

  ret_val = _storage_utils.get_file_path(asset_path)

  return ret_val
