from src.libs.python_utils.files import file_utils
from src.libs.python_utils.id.id_utils import generate_id
from src.libs.django_utils.storage import storage_utils

from src.apps.asset.asset_value_object import AssetValueObject


def _generate_asset_id_from_filename(filename, _file_utils=None):
  if not _file_utils: _file_utils = file_utils

  asset_id = generate_id()
  asset_id_with_ext = "{0}.{1}".format(asset_id, _file_utils.get_file_extension(filename))

  return asset_id_with_ext


def _get_extension_from_filename(filename, _file_utils=None):
  if not _file_utils: _file_utils = file_utils

  ret_val = _file_utils.get_file_extension(filename)

  return ret_val


def _save_file_to_storage(file, path, _storage_utils=None):
  if not _storage_utils: _storage_utils = storage_utils

  ret_val = _storage_utils.save_file(file, path)

  return ret_val


def persist_asset_from_file(file, path):
  asset_id = _generate_asset_id_from_filename(file.name)
  path = "{0}/{1}".format(path, asset_id)
  extension = _get_extension_from_filename(file.name)

  _save_file_to_storage(file, path)

  ret_val = AssetValueObject(path, extension, file.content_type)

  return ret_val
