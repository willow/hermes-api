import datetime
import time
from pytz import UTC


def get_utc_from_timestamp(timestamp):
  return datetime.datetime.fromtimestamp(timestamp, tz=UTC)


# http://stackoverflow.com/a/27914405/173957
def get_timestamp_from_datetime(datetime):
  return int(time.mktime(datetime.timetuple()))
