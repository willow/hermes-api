from django.conf import settings

constants = settings.CONSTANTS


def get_agreement_info_from_file(file):
  # validate file (not empty? valid file type?) delegate to file_utils
  return {constants.AGREEMENT_NAME: file.name}
