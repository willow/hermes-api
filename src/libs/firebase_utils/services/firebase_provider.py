from calendar import timegm
import datetime
from firebase import firebase
from django.conf import settings

FIREBASE_SECRET = settings.FIREBASE_SECRET
FIREBASE_APP = settings.FIREBASE_APP
FIREBASE_DEBUG = settings.FIREBASE_DEBUG

# apparently firebase requires an exp claim even though they say they dont': https://www.firebase.com/docs/rest/gide/user-auth.html#section-tokens-without-helpers
# how to get epoch time https://github.com/jpadilla/pyjwt/blob/12791c7875dda323835b8e0b9c687d17ba0e641b/jwt/api_jwt.py#L47
# an auth token of 7 days should be good enough (famous last words...)
exp = timegm((datetime.datetime.utcnow() + datetime.timedelta(days=7)).utctimetuple())
authentication = firebase.FirebaseAuthentication(
  FIREBASE_SECRET, settings.DEV_EMAIL_ADDRESS, FIREBASE_DEBUG, True, {'exp': exp}
)

firebase_url = 'https://{firebase_app}.firebaseio.com'.format(firebase_app=FIREBASE_APP)
firebase = firebase.FirebaseApplication(firebase_url, authentication)


def get_firebase_client():
  return firebase
