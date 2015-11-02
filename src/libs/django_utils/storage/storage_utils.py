from django.core.files.storage import default_storage


def save_file(name, file):
  return default_storage.save(name, file)


def get_file_path(path):
  return default_storage.url(path)
