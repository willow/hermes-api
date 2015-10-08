def get_user_id_from_jwt(jwt_payload):
  ret_val = jwt_payload['app_metadata']['hermes']['user_id']
  return ret_val
