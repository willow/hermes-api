from django.conf import settings
import requests
import json

client = requests.Session()

# Just store the token: https://ask.auth0.com/t/creating-a-valid-jwt-token-in-go/1037
# For some reason, we can only use tokens generated from: https://ask.auth0.com/t/creating-user-using-api-v2-client-is-not-global-response/1032
# because that is how you access a global client id. wtf!?
AUTH0_SECRET = settings.AUTH0_SECRET
AUTH0_APP = settings.AUTH0_APP

APP_NAME = settings.APP_NAME


def save_user_id_in_auth0(auth0_user_id, user_uid):
  url = 'https://{auth0_app}.auth0.com/api/v2/users/{user_id}'.format(
    auth0_app=AUTH0_APP,
    user_id=auth0_user_id
  )

  data = {'app_metadata': {APP_NAME: {'uid': user_uid}}}

  # http://stackoverflow.com/questions/9746303/how-do-i-send-a-post-request-as-a-json
  headers = {
    'Authorization': 'Bearer {0}'.format(AUTH0_SECRET),
    'content-type': 'application/json'
  }

  resp = client.patch(url, data=json.dumps(data), headers=headers, timeout=settings.HTTP_TIMEOUT)
  resp.raise_for_status()

  result = resp.json()

  return result
