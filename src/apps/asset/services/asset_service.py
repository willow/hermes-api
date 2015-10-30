from src.libs.python_utils.files import file_utils
from src.libs.python_utils.id.id_utils import generate_id
from src.libs.django_utils.storage import storage_utils

from src.apps.asset.asset_value_object import AssetValueObject


def _generate_asset_id_from_filename(asset_id, filename, _file_utils=None):
  if not _file_utils: _file_utils = file_utils

  asset_id_with_ext = "{0}.{1}".format(asset_id, _file_utils.get_file_extension(filename))

  return asset_id_with_ext


def _save_file_to_storage(file, path, _storage_utils=None):
  if not _storage_utils: _storage_utils = storage_utils

  ret_val = _storage_utils.save_file(file, path)

  return ret_val


def persist_asset_from_file(file, path):
  original_name = file.name
  asset_id = generate_id()

  asset_id_with_ext = _generate_asset_id_from_filename(asset_id, original_name)
  path = "{0}/{1}".format(path, asset_id_with_ext)

  _save_file_to_storage(file, path)

  ret_val = AssetValueObject(asset_id, path, file.content_type, original_name)

  return ret_val
