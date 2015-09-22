import shortuuid

import string

chars = string.ascii_letters + string.digits

# just stick to base62 for now
shortuuid.set_alphabet(chars)


def generate_id(length=8):
  ret_val = shortuuid.uuid()[:length]
  return ret_val
