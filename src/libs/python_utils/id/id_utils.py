import shortuuid


def generate_id(length=8):
  ret_val = shortuuid.uuid()[:length]
  return ret_val
