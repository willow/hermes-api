from django.conf import settings
from django.db import transaction
from django.dispatch import receiver
from django.utils import timezone

from src.domain.asset.commands import CreateAssetFromFile
from src.domain.asset.entities import Asset
from src.libs.common_domain import aggregate_repository
from src.libs.django_utils.storage import storage_utils
from src.libs.python_utils.files import file_utils
from src.libs.python_utils.id.id_utils import generate_id

constants = settings.CONSTANTS
assets_root = constants.ASSETS_ROOT


@receiver(CreateAssetFromFile.command_signal)
def create_asset_from_file(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  command = kwargs['command']
  destination_path = command.destination_path
  file = command.file
  file_name = file.name

  asset_id = generate_id()
  system_created_date = timezone.now()

  asset_id_with_ext = _generate_asset_id_from_filename(asset_id, file_name)
  path = "{0}/{1}".format(destination_path, asset_id_with_ext)

  data = {
    'id': asset_id, 'path': path, 'content_type': file.content_type,
    'original_name': file_name, 'system_created_date': system_created_date,
  }

  asset = Asset.from_attrs(**data)

  with transaction.atomic():
    _aggregate_repository.save(asset, -1)
    _save_file_to_storage(path, file)

  # commands typically shouldn't return an object but we're explicitly calling this function from the API
  # and need the return aggregate
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
