from django.conf import settings
from src.libs.python_utils.files import file_utils

constants = settings.CONSTANTS


def get_agreement_info_from_file(file, _file_utils=None):
  if not _file_utils: _file_utils = file_utils

  # validate file (not empty? valid file type?) delegate to file_utils
  return {constants.AGREEMENT_NAME: _file_utils.get_file_file_without_extension(file.name)}
