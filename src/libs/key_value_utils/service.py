from src.libs.key_value_utils.key_value_provider import get_key_value_client


# http://redis.io/commands/INCR#pattern-rate-limiter-2
def record_rate_limit(key_name, expiration):
  kdb = get_key_value_client()
  if kdb.exists(key_name):
    # The RPUSHX command only pushes the element if the key already exists. Prevents leaked keys.
    ret_val = kdb.rpushx(key_name, True)
  else:
    with kdb.pipeline() as pipe:
      pipe.rpush(key_name, True)
      pipe.expire(key_name, expiration)
      ret_val = pipe.execute()

  return ret_val


def get_rate_limit_count(key_name):
  kdb = get_key_value_client()

  ret_val = kdb.llen(key_name)

  return ret_val


# http://redis.io/commands/LTRIM
# http://stackoverflow.com/questions/16641011/redis-capped-sorted-set-list-or-queue
# http://highscalability.com/blog/2011/7/6/11-common-web-use-cases-solved-in-redis.html
def push_latest(key_name, key_value, length_limit):
  kdb = get_key_value_client()

  with kdb.pipeline() as pipe:
    pipe.lpush(key_name, key_value)
    pipe.ltrim(key_name, 0, length_limit)
    ret_val = pipe.execute()

  return ret_val
