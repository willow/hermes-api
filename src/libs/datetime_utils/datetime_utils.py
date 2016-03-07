import datetime
import time

from pytz import UTC
from dateutil import parser


def get_date_from_string(string_time):
  return parser.parse(string_time)


def get_utc_from_timestamp(timestamp):
  return datetime.datetime.fromtimestamp(timestamp, tz=UTC)


# http://stackoverflow.com/a/27914405/173957
def get_timestamp_from_datetime(datetime):
  return int(time.mktime(datetime.timetuple()))
