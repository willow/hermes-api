from src.apps.common import constants
from src.libs.python_utils.files import file_utils


def get_agreement_info_from_files(files, _file_utils=None):
  if not _file_utils: _file_utils = file_utils

  file = files[0]  # take first file
  # validate file (not empty? valid file type?) delegate to file_utils
  return {constants.AGREEMENT_NAME: _file_utils.get_file_file_without_extension(file.name)}
