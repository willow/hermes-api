from django.core.files.storage import default_storage

from django.conf import settings

constants = settings.CONSTANTS
assets_root = constants.ASSETS_ROOT


def save_file(file, name):
  name = "{0}/{1}".format(assets_root, name)
  return default_storage.save(name, file)
