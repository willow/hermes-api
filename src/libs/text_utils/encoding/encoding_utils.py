import base64


# https://github.com/auth0/auth0-python/blob/master/examples/flask-api/server.py
def base64decode(string_input):
  ret_val = base64.b64decode(string_input.replace("_", "/").replace("-", "+"))
  return ret_val
