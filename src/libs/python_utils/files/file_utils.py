import os


def get_file_extension(filename):
  _, file_extension = os.path.splitext(filename)
  # remove leading period
  file_extension = file_extension[1:]
  return file_extension


def get_file_file_without_extension(filename):
  ret_val, _ = os.path.splitext(filename)
  return ret_val
